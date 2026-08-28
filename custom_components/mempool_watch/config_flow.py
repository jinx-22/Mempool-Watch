"""Config flow and options flow for Mempool Watch."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    BooleanSelector,
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    TextSelector,
    TextSelectorConfig,
)

from .api import (
    MempoolApiClient,
    MempoolApiConnectionError,
    MempoolApiError,
    async_build_ssl,
)
from .const import (
    CONF_ADDRESSES,
    CONF_BASE_URL,
    CONF_CA_CERT,
    CONF_CURRENCIES,
    CONF_UPDATE_INTERVAL,
    CONF_VERIFY_SSL,
    CURRENCY_CHOICES,
    DEFAULT_BASE_URL,
    DEFAULT_CURRENCIES,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_VERIFY_SSL,
    DOMAIN,
    LOGGER,
    MAX_UPDATE_INTERVAL,
    MIN_UPDATE_INTERVAL,
)


def _settings_schema(
    defaults: dict[str, Any] | None = None,
) -> vol.Schema:
    """Return the general settings schema."""
    d = defaults or {}

    return vol.Schema(
        {
            vol.Required(
                CONF_BASE_URL,
                default=d.get(CONF_BASE_URL, DEFAULT_BASE_URL),
            ): str,
            vol.Optional(
                CONF_UPDATE_INTERVAL,
                default=d.get(
                    CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                ),
            ): vol.All(
                vol.Coerce(int),
                vol.Range(
                    min=MIN_UPDATE_INTERVAL,
                    max=MAX_UPDATE_INTERVAL,
                ),
            ),
            vol.Optional(
                CONF_VERIFY_SSL,
                default=d.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL),
            ): BooleanSelector(),
            vol.Optional(
                CONF_CA_CERT,
                default=d.get(CONF_CA_CERT, ""),
            ): TextSelector(
                TextSelectorConfig(
                    multiline=True,
                    type="text",
                )
            ),
        }
    )


def _available_currencies_from_prices(
    price_data: dict[str, Any],
) -> list[str]:
    """Return lowercase ISO codes that the instance actually provides.

    Mempool marks unavailable fiat rates with -1.
    """
    available: list[str] = []
    for key, value in price_data.items():
        if key.lower() == "time":
            continue
        code = str(key).lower()
        if code not in CURRENCY_CHOICES and code != "usd":
            # Still allow any real rate the instance returns
            pass
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            continue
        if numeric < 0:
            continue
        if code not in available:
            available.append(code)
    # Prefer stable order: known choices first, then extras
    ordered = [c for c in CURRENCY_CHOICES if c in available]
    for c in available:
        if c not in ordered and c != "usd":
            ordered.append(c)
    return ordered


def _currency_options(
    available: list[str] | None = None,
) -> list[SelectOptionDict]:
    """Return currency selector options (only available ones if given)."""
    codes = available if available is not None else list(CURRENCY_CHOICES)
    return [
        SelectOptionDict(
            value=currency,
            label=currency.upper(),
        )
        for currency in codes
    ]


def _normalize_currencies(
    currencies: list[str] | tuple[str, ...] | None,
    available: list[str] | None = None,
) -> list[str]:
    """Normalize and validate selected currencies."""
    if not currencies:
        return []

    allowed = set(available) if available is not None else set(CURRENCY_CHOICES)
    # Always accept known choices even if available list is partial
    allowed |= set(CURRENCY_CHOICES)

    normalized: list[str] = []
    for currency in currencies:
        value = str(currency).lower()
        if value in allowed and value not in normalized:
            if available is not None and value not in available:
                continue
            normalized.append(value)
    return normalized


def _currency_schema(
    defaults: list[str] | None = None,
    available: list[str] | None = None,
) -> vol.Schema:
    """Return the currency selection schema."""
    codes = available if available is not None else list(CURRENCY_CHOICES)
    selected = _normalize_currencies(
        defaults if defaults is not None else DEFAULT_CURRENCIES,
        available=codes,
    )
    # Empty selection is valid (USD-only)

    return vol.Schema(
        {
            vol.Required(
                CONF_CURRENCIES,
                default=selected,
            ): SelectSelector(
                SelectSelectorConfig(
                    options=_currency_options(codes),
                    multiple=True,
                    mode="list",
                    translation_key="currencies",
                )
            ),
        }
    )


def _remove_currency_entities(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    currencies: set[str],
) -> None:
    """Remove entity registry entries for deselected currencies."""
    if not currencies:
        return

    registry = er.async_get(hass)
    for currency in currencies:
        unique_id = f"{config_entry.entry_id}_price_{currency.lower()}"
        entity_id = registry.async_get_entity_id("sensor", DOMAIN, unique_id)
        if entity_id is not None:
            LOGGER.debug(
                "Removing deselected currency entity: %s (unique_id=%s)",
                entity_id,
                unique_id,
            )
            registry.async_remove(entity_id)


async def _async_client_from_input(
    hass: HomeAssistant,
    base_url: str,
    verify_ssl: bool,
    ca_cert: str | None,
) -> MempoolApiClient:
    """Create API client from form values (SSL built off the event loop)."""
    session = async_get_clientsession(hass)
    ssl_arg = await async_build_ssl(hass, verify_ssl, ca_cert or None)
    return MempoolApiClient(base_url, session, ssl=ssl_arg)


async def _async_fetch_available_currencies(
    client: MempoolApiClient,
) -> list[str]:
    """Fetch /api/v1/prices and return currencies with a real rate."""
    try:
        price_data = await client.async_get_prices()
    except MempoolApiError as err:
        LOGGER.warning("Could not fetch prices for currency list: %s", err)
        return list(CURRENCY_CHOICES)

    available = _available_currencies_from_prices(price_data)
    if not available:
        LOGGER.warning(
            "Price endpoint returned no usable currencies, falling back to full list"
        )
        return list(CURRENCY_CHOICES)
    return available


class MempoolFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle initial setup."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._base_url = DEFAULT_BASE_URL
        self._update_interval = DEFAULT_UPDATE_INTERVAL
        self._verify_ssl = DEFAULT_VERIFY_SSL
        self._ca_cert = ""
        self._available_currencies: list[str] = list(CURRENCY_CHOICES)

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle the initial configuration step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            base_url = user_input[CONF_BASE_URL].strip().rstrip("/")
            update_interval = user_input.get(
                CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
            )
            verify_ssl = user_input.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL)
            ca_cert = (user_input.get(CONF_CA_CERT) or "").strip()

            parsed = urlparse(base_url)

            if parsed.scheme not in ("http", "https") or not parsed.hostname:
                errors["base"] = "invalid_url"
            else:
                unique_id = parsed.hostname
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

                try:
                    client = await _async_client_from_input(
                        self.hass, base_url, verify_ssl, ca_cert
                    )
                    await client.async_get_backend_info()
                    self._available_currencies = (
                        await _async_fetch_available_currencies(client)
                    )
                except MempoolApiConnectionError:
                    errors["base"] = "cannot_connect"
                except MempoolApiError as err:
                    if "Invalid CA certificate" in str(err):
                        errors[CONF_CA_CERT] = "invalid_ca_cert"
                    else:
                        errors["base"] = "cannot_connect"
                except Exception:
                    LOGGER.exception("Unexpected error during config flow")
                    errors["base"] = "unknown"

                if not errors:
                    self._base_url = base_url
                    self._update_interval = update_interval
                    self._verify_ssl = verify_ssl
                    self._ca_cert = ca_cert
                    return await self.async_step_currencies()

        return self.async_show_form(
            step_id="user",
            data_schema=_settings_schema(),
            errors=errors,
        )

    async def async_step_currencies(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Select currencies during initial setup."""
        available = self._available_currencies

        if user_input is not None:
            currencies = _normalize_currencies(
                user_input.get(CONF_CURRENCIES, []),
                available=available,
            )
            # Empty list is allowed → only the built-in USD BTC price sensor

            hostname = urlparse(self._base_url).hostname or self._base_url
            return self.async_create_entry(
                title=hostname,
                data={
                    CONF_BASE_URL: self._base_url,
                    CONF_UPDATE_INTERVAL: self._update_interval,
                    CONF_VERIFY_SSL: self._verify_ssl,
                    CONF_CA_CERT: self._ca_cert,
                    CONF_CURRENCIES: currencies,
                    CONF_ADDRESSES: [],
                },
            )

        return self.async_show_form(
            step_id="currencies",
            data_schema=_currency_schema(None, available),
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> OptionsFlow:
        """Return the options flow."""
        return MempoolOptionsFlowHandler()


class MempoolOptionsFlowHandler(OptionsFlow):
    """Handle configuration changes."""

    def __init__(self) -> None:
        """Initialize options flow."""
        self._available_currencies: list[str] = list(CURRENCY_CHOICES)

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Show the options menu."""
        return self.async_show_menu(
            step_id="init",
            menu_options=[
                "settings",
                "currencies",
                "add_address",
                "remove_address",
            ],
        )

    async def async_step_settings(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Edit URL, interval, SSL and optional CA."""
        errors: dict[str, str] = {}
        current = {**self.config_entry.data, **self.config_entry.options}

        if user_input is not None:
            base_url = user_input[CONF_BASE_URL].strip().rstrip("/")
            update_interval = user_input.get(
                CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
            )
            verify_ssl = user_input.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL)
            ca_cert = (user_input.get(CONF_CA_CERT) or "").strip()
            parsed = urlparse(base_url)

            if parsed.scheme not in ("http", "https") or not parsed.hostname:
                errors["base"] = "invalid_url"
            else:
                try:
                    client = await _async_client_from_input(
                        self.hass, base_url, verify_ssl, ca_cert
                    )
                    await client.async_get_backend_info()
                except MempoolApiConnectionError:
                    errors["base"] = "cannot_connect"
                except MempoolApiError as err:
                    if "Invalid CA certificate" in str(err):
                        errors[CONF_CA_CERT] = "invalid_ca_cert"
                    else:
                        errors["base"] = "cannot_connect"
                except Exception:
                    LOGGER.exception("Unexpected error during options flow")
                    errors["base"] = "unknown"

                if not errors:
                    currencies = _normalize_currencies(
                        current.get(CONF_CURRENCIES, DEFAULT_CURRENCIES)
                    )
                    addresses = list(current.get(CONF_ADDRESSES, []))
                    new_data = {
                        **current,
                        CONF_BASE_URL: base_url,
                        CONF_UPDATE_INTERVAL: update_interval,
                        CONF_VERIFY_SSL: verify_ssl,
                        CONF_CA_CERT: ca_cert,
                        CONF_CURRENCIES: currencies,
                        CONF_ADDRESSES: addresses,
                    }
                    self.hass.config_entries.async_update_entry(
                        self.config_entry,
                        data=new_data,
                        title=parsed.hostname or base_url,
                    )
                    await self.hass.config_entries.async_reload(
                        self.config_entry.entry_id
                    )
                    return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="settings",
            data_schema=_settings_schema(current),
            errors=errors,
        )

    async def async_step_currencies(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Edit enabled currencies (only rates the instance provides)."""
        current = {**self.config_entry.data, **self.config_entry.options}
        current_currencies = _normalize_currencies(
            current.get(CONF_CURRENCIES, DEFAULT_CURRENCIES)
        )

        # Fetch live price list when opening the step
        if user_input is None:
            try:
                client = await _async_client_from_input(
                    self.hass,
                    current[CONF_BASE_URL],
                    current.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL),
                    current.get(CONF_CA_CERT) or None,
                )
                self._available_currencies = (
                    await _async_fetch_available_currencies(client)
                )
            except Exception:
                LOGGER.exception("Failed to refresh available currencies")
                self._available_currencies = list(CURRENCY_CHOICES)

        available = self._available_currencies

        if user_input is not None:
            currencies = _normalize_currencies(
                user_input.get(CONF_CURRENCIES, []),
                available=available,
            )
            # Empty list is allowed → only the built-in USD BTC price sensor

            removed = set(current_currencies) - set(currencies)
            _remove_currency_entities(self.hass, self.config_entry, removed)

            new_data = {**current, CONF_CURRENCIES: currencies}
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=new_data
            )
            await self.hass.config_entries.async_reload(
                self.config_entry.entry_id
            )
            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="currencies",
            data_schema=_currency_schema(current_currencies, available),
        )

    async def async_step_add_address(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Add a named BTC address."""
        errors: dict[str, str] = {}
        current = {**self.config_entry.data, **self.config_entry.options}
        addresses: list[dict[str, str]] = list(
            current.get(CONF_ADDRESSES, [])
        )

        if user_input is not None:
            name = user_input["name"].strip()
            address = user_input["address"].strip()

            if not name:
                errors["name"] = "invalid_name"
            elif not address:
                errors["address"] = "invalid_address"
            elif any(item.get("address") == address for item in addresses):
                errors["address"] = "address_exists"
            else:
                try:
                    client = await _async_client_from_input(
                        self.hass,
                        current[CONF_BASE_URL],
                        current.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL),
                        current.get(CONF_CA_CERT) or None,
                    )
                    await client.async_get_address(address)
                except MempoolApiError:
                    errors["address"] = "invalid_address"
                except Exception:
                    LOGGER.exception("Error validating address")
                    errors["address"] = "invalid_address"

                if not errors:
                    addresses.append({"name": name, "address": address})
                    new_data = {**current, CONF_ADDRESSES: addresses}
                    self.hass.config_entries.async_update_entry(
                        self.config_entry, data=new_data
                    )
                    await self.hass.config_entries.async_reload(
                        self.config_entry.entry_id
                    )
                    return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="add_address",
            data_schema=vol.Schema(
                {
                    vol.Required("name"): str,
                    vol.Required("address"): str,
                }
            ),
            errors=errors,
        )

    async def async_step_remove_address(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Remove a previously added BTC address."""
        current = {**self.config_entry.data, **self.config_entry.options}
        addresses: list[dict[str, str]] = list(
            current.get(CONF_ADDRESSES, [])
        )

        if not addresses:
            return self.async_abort(reason="no_addresses")

        choices = {
            item["address"]: (
                f"{item['name']} "
                f"({item['address'][:8]}…{item['address'][-4:]})"
            )
            for item in addresses
        }

        if user_input is not None:
            to_remove = user_input["address"]
            addresses = [
                item for item in addresses if item["address"] != to_remove
            ]
            new_data = {**current, CONF_ADDRESSES: addresses}
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=new_data
            )
            await self.hass.config_entries.async_reload(
                self.config_entry.entry_id
            )
            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="remove_address",
            data_schema=vol.Schema(
                {
                    vol.Required("address"): SelectSelector(
                        SelectSelectorConfig(
                            options=[
                                SelectOptionDict(value=a, label=l)
                                for a, l in choices.items()
                            ],
                            mode="dropdown",
                        )
                    ),
                }
            ),
        )
