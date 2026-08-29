"""Mempool Watch integration for Home Assistant."""

from __future__ import annotations

from pathlib import Path

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MempoolApiClient, async_build_ssl
from .const import (
    CONF_ADDRESSES,
    CONF_BASE_URL,
    CONF_CA_CERT,
    CONF_UPDATE_INTERVAL,
    CONF_VERIFY_SSL,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_VERIFY_SSL,
)
from .coordinator import MempoolDataUpdateCoordinator
from .data import MempoolConfigEntry, MempoolData

PLATFORMS: list[Platform] = [Platform.SENSOR]

CARD_FILENAME = "btc-address-card.js"
CARD_URL = f"/mempool_watch/{CARD_FILENAME}"


async def _async_register_card_resource(
    hass: HomeAssistant,
) -> None:
    """Register the BTC Address Card as a Lovelace resource."""
    card_path = Path(__file__).parent / "frontend" / CARD_FILENAME

    if not card_path.is_file():
        return

    from homeassistant.components.http import StaticPathConfig

    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                CARD_URL,
                str(card_path),
                False,
            )
        ]
    )

    lovelace = hass.data.get("lovelace")

    if lovelace is None:
        return

    resources = lovelace.resources

    if resources is None:
        return

    await resources.async_get_info()

    for resource in resources.async_items():
        if resource.get("url", "").split("?")[0] == CARD_URL:
            return

    await resources.async_create_item(
        {
            "res_type": "module",
            "url": CARD_URL,
        }
    )


async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    """Set up Mempool Watch."""
    await _async_register_card_resource(hass)
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MempoolConfigEntry,
) -> bool:
    """Set up Mempool Watch from a config entry."""
    conf = {**entry.data, **entry.options}

    session = async_get_clientsession(hass)

    ssl_arg = await async_build_ssl(
        hass,
        conf.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL),
        conf.get(CONF_CA_CERT) or None,
    )

    client = MempoolApiClient(
        conf[CONF_BASE_URL],
        session,
        ssl=ssl_arg,
    )

    update_interval = conf.get(
        CONF_UPDATE_INTERVAL,
        DEFAULT_UPDATE_INTERVAL,
    )

    addresses = conf.get(
        CONF_ADDRESSES,
        [],
    ) or []

    coordinator = MempoolDataUpdateCoordinator(
        hass,
        client,
        update_interval,
        addresses,
    )

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = MempoolData(
        client=client,
        coordinator=coordinator,
    )

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: MempoolConfigEntry,
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )
