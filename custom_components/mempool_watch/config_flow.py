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
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
)

from .api import MempoolApiClient, MempoolApiConnectionError, MempoolApiError
from .const import (
    CONF_ADDRESSES,
    CONF_BASE_URL,
    CONF_SECONDARY_CURRENCY,
    CONF_UPDATE_INTERVAL,
    CURRENCY_CHOICES,
    DEFAULT_BASE_URL,
    DEFAULT_SECONDARY_CURRENCY,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
    LOGGER,
    MAX_UPDATE_INTERVAL,
    MIN_UPDATE_INTERVAL,
)


def _settings_schema(defaults: dict[str, Any] | None = None) -> vol.Schema:
    d = defaults or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_BASE_URL,
                default=d.get(CONF_BASE_URL, DEFAULT_BASE_URL),
            ): str,
            vol.Optional(
                CONF_UPDATE_INTERVAL,
                default=d.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
            ): vol.All(
                vol.Coerce(int),
                vol.Range(min=MIN_UPDATE_INTERVAL, max=MAX_UPDATE_INTERVAL),
            ),
            vol.Optional(
                CONF_SECONDARY_CURRENCY,
                default=d.get(CONF_SECONDARY_CURRENCY, DEFAULT_SECONDARY_CURRENCY),
            ): SelectSelector(
                SelectSelectorConfig(
                    options=CURRENCY_CHOICES,
                    mode="dropdown",
                    translation_key="secondary_currency",
                )
            ),
        }
    )


class MempoolFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle initial setup."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Initial config step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            base_url = user_input[CONF_BASE_URL].strip().rstrip("/")
            update_interval = user_input.get(
                CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
            )
            secondary = user_input.get(
                CONF_SECONDARY_CURRENCY, DEFAULT_SECONDARY_CURRENCY
            )

            parsed = urlparse(base_url)
            if parsed.scheme not in ("http", "https") or not parsed.hostname:
                errors["base"] = "invalid_url"
            else:
                unique_id = parsed.hostname
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

                session = async_get_clientsession(self.hass)
                try:
                    client = MempoolApiClient(base_url, session)
                    await client.async_get_backend_info()
                except MempoolApiConnectionError:
                    errors["base"] = "cannot_connect"
                except MempoolApiError:
                    errors["base"] = "cannot_connect"
                except Exception:
                    LOGGER.exception("Unexpected error during config flow")
                    errors["base"] = "unknown"

                if not errors:
                    return self.async_create_entry(
                        title=parsed.hostname or base_url,
                        data={
                            CONF_BASE_URL: base_url,
                            CONF_UPDATE_INTERVAL: update_interval,
                            CONF_SECONDARY_CURRENCY: secondary,
                            CONF_ADDRESSES: [],
                        },
                    )

        return self.async_show_form(
            step_id="user",
            data_schema=_settings_schema(),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Return the options flow (gear icon)."""
        return MempoolOptionsFlowHandler()


class MempoolOptionsFlowHandler(OptionsFlow):
    """Options: settings, add/remove BTC addresses."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Show options menu."""
        return self.async_show_menu(
            step_id="init",
            menu_options=["settings", "add_address", "remove_address"],
        )

    async def async_step_settings(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Edit URL, interval, secondary currency."""
        errors: dict[str, str] = {}
        current = {**self.config_entry.data, **self.config_entry.options}

        if user_input is not None:
            base_url = user_input[CONF_BASE_URL].strip().rstrip("/")
            update_interval = user_input.get(
                CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
            )
            secondary = user_input.get(
                CONF_SECONDARY_CURRENCY, DEFAULT_SECONDARY_CURRENCY
            )

            parsed = urlparse(base_url)
            if parsed.scheme not in ("http", "https") or not parsed.hostname:
                errors["base"] = "invalid_url"
            else:
                session = async_get_clientsession(self.hass)
                try:
                    client = MempoolApiClient(base_url, session)
                    await client.async_get_backend_info()
                except MempoolApiConnectionError:
                    errors["base"] = "cannot_connect"
                except MempoolApiError:
                    errors["base"] = "cannot_connect"
                except Exception:
                    LOGGER.exception("Unexpected error during options flow")
                    errors["base"] = "unknown"

                if not errors:
                    addresses = current.get(CONF_ADDRESSES, [])
                    new_data = {
                        CONF_BASE_URL: base_url,
                        CONF_UPDATE_INTERVAL: update_interval,
                        CONF_SECONDARY_CURRENCY: secondary,
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

    async def async_step_add_address(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Add a named BTC address as entity."""
        errors: dict[str, str] = {}
        current = {**self.config_entry.data, **self.config_entry.options}
        addresses: list[dict[str, str]] = list(current.get(CONF_ADDRESSES, []))

        if user_input is not None:
            name = user_input["name"].strip()
            address = user_input["address"].strip()

            if not name:
                errors["name"] = "invalid_name"
            elif not address:
                errors["address"] = "invalid_address"
            elif any(a["address"] == address for a in addresses):
                errors["address"] = "address_exists"
            else:
                # Quick validation against the API
                base_url = current[CONF_BASE_URL]
                session = async_get_clientsession(self.hass)
                try:
                    client = MempoolApiClient(base_url, session)
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

        schema = vol.Schema(
            {
                vol.Required("name"): str,
                vol.Required("address"): str,
            }
        )
        return self.async_show_form(
            step_id="add_address",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_remove_address(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Remove a previously added BTC address."""
        current = {**self.config_entry.data, **self.config_entry.options}
        addresses: list[dict[str, str]] = list(current.get(CONF_ADDRESSES, []))

        if not addresses:
            return self.async_abort(reason="no_addresses")

        # Options for select: "name (shortaddr)" -> address
        choices = {
            a["address"]: f"{a['name']} ({a['address'][:8]}…{a['address'][-4:]})"
            for a in addresses
        }

        if user_input is not None:
            to_remove = user_input["address"]
            addresses = [a for a in addresses if a["address"] != to_remove]
            new_data = {**current, CONF_ADDRESSES: addresses}
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=new_data
            )
            await self.hass.config_entries.async_reload(self.config_entry.entry_id)
            return self.async_create_entry(title="", data={})

        schema = vol.Schema(
            {
                vol.Required("address"): SelectSelector(
                    SelectSelectorConfig(
                        options=list(choices.keys()),
                        mode="dropdown",
                    )
                ),
            }
        )
        # Show friendly labels via description is limited; use options as values
        # Better: pass option labels via SelectOptionDict if available
        from homeassistant.helpers.selector import SelectOptionDict

        schema = vol.Schema(
            {
                vol.Required("address"): SelectSelector(
                    SelectSelectorConfig(
                        options=[
                            SelectOptionDict(value=addr, label=label)
                            for addr, label in choices.items()
                        ],
                        mode="dropdown",
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="remove_address",
            data_schema=schema,
        )
