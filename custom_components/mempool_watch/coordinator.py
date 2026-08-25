"""DataUpdateCoordinator for the Mempool Watch integration."""

from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MempoolApiClient, MempoolApiError
from .const import DEFAULT_UPDATE_INTERVAL, DOMAIN, LOGGER

_SATS = 1e8


def _sats_to_btc(sats: int) -> float:
    """Convert satoshis to BTC, 8 decimal places."""
    return round(int(sats) / _SATS, 8)


def _parse_address(addr_data: dict[str, Any]) -> dict[str, Any]:
    """Parse /api/address into confirmed balance + unconfirmed extras."""
    chain = addr_data.get("chain_stats") or {}
    mempool = addr_data.get("mempool_stats") or {}

    funded_chain = int(chain.get("funded_txo_sum", 0))
    spent_chain = int(chain.get("spent_txo_sum", 0))
    funded_mem = int(mempool.get("funded_txo_sum", 0))
    spent_mem = int(mempool.get("spent_txo_sum", 0))

    return {
        "confirmed_balance": _sats_to_btc(funded_chain - spent_chain),
        "pending_incoming": _sats_to_btc(funded_mem),
        "pending_outgoing": _sats_to_btc(spent_mem),
        "pending_change": _sats_to_btc(funded_mem - spent_mem),
        "unconfirmed_count": int(mempool.get("tx_count", 0)),
    }


class MempoolDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator that polls the configured mempool instance."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: MempoolApiClient,
        update_interval: int = DEFAULT_UPDATE_INTERVAL,
        addresses: list[dict[str, str]] | None = None,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )
        self.client = client
        self.addresses = addresses or []

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch network endpoints and configured address balances."""
        try:
            results = await asyncio.gather(
                self.client.async_get_fees_recommended(),
                self.client.async_get_mempool(),
                self.client.async_get_tip_hash(),
                self.client.async_get_difficulty_adjustment(),
                self.client.async_get_hashrate(),
                self.client.async_get_reward_stats(),
                self.client.async_get_prices(),
            )
        except MempoolApiError as err:
            raise UpdateFailed(f"Error fetching mempool data: {err}") from err

        (
            fees,
            mempool,
            tip_hash,
            difficulty,
            hashrate,
            reward_stats,
            price_data,
        ) = results

        try:
            latest_block = await self.client.async_get_block(tip_hash)
        except MempoolApiError as err:
            raise UpdateFailed(f"Error fetching latest block: {err}") from err

        price = {k: v for k, v in price_data.items() if k != "time"}

        # Address stats (failures for single addresses are isolated)
        address_data: dict[str, dict[str, Any] | None] = {}
        if self.addresses:
            addr_results = await asyncio.gather(
                *[
                    self.client.async_get_address(item["address"])
                    for item in self.addresses
                ],
                return_exceptions=True,
            )
            for item, result in zip(self.addresses, addr_results):
                key = item["address"]
                if isinstance(result, Exception):
                    LOGGER.warning(
                        "Failed to fetch address %s: %s", key, result
                    )
                    address_data[key] = None
                else:
                    try:
                        address_data[key] = _parse_address(result)
                    except (KeyError, TypeError, ValueError) as err:
                        LOGGER.warning(
                            "Failed to parse address %s: %s", key, err
                        )
                        address_data[key] = None

        return {
            "fees": fees,
            "mempool": mempool,
            "tip_height": latest_block.get("height"),
            "difficulty_adjustment": difficulty,
            "hashrate": hashrate,
            "reward_stats": reward_stats,
            "latest_block": latest_block,
            "price": price,
            "address_data": address_data,
        }
