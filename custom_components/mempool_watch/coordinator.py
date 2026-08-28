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
_CRITICAL = frozenset({"fees", "mempool", "tip_hash", "difficulty"})


def _sats_to_btc(sats: int) -> float:
    """Convert satoshis to BTC."""
    return round(int(sats) / _SATS, 8)


def _parse_address(addr_data: dict[str, Any]) -> dict[str, Any]:
    """Parse /api/address into balance fields."""
    chain = addr_data.get("chain_stats") or {}
    mem = addr_data.get("mempool_stats") or {}
    funded_c, spent_c = int(chain.get("funded_txo_sum", 0)), int(chain.get("spent_txo_sum", 0))
    funded_m, spent_m = int(mem.get("funded_txo_sum", 0)), int(mem.get("spent_txo_sum", 0))
    return {
        "confirmed_balance": _sats_to_btc(funded_c - spent_c),
        "pending_incoming": _sats_to_btc(funded_m),
        "pending_outgoing": _sats_to_btc(spent_m),
        "pending_change": _sats_to_btc(funded_m - spent_m),
        "unconfirmed_count": int(mem.get("tx_count", 0)),
    }


def _short_err(err: BaseException) -> str:
    """One-line error for logs / UpdateFailed."""
    t = str(err)
    if "503" in t:
        return "Mempool temporarily unavailable (HTTP 503)"
    if "502" in t:
        return "Mempool bad gateway (HTTP 502)"
    if "504" in t:
        return "Mempool gateway timeout (HTTP 504)"
    if "connect" in t.lower() or "Connection" in t:
        return "Cannot connect to Mempool instance"
    if "timeout" in t.lower() or "Timeout" in t:
        return "Timeout talking to Mempool instance"
    if "SSL" in t or "certificate" in t.lower():
        return "SSL/certificate error"
    return t if len(t) <= 160 else t[:157] + "…"


class MempoolDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator that polls the configured mempool instance."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: MempoolApiClient,
        update_interval: int = DEFAULT_UPDATE_INTERVAL,
        addresses: list[dict[str, str]] | None = None,
    ) -> None:
        super().__init__(
            hass, LOGGER, name=DOMAIN, update_interval=timedelta(seconds=update_interval)
        )
        self.client = client
        self.addresses = addresses or []

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch network endpoints and configured address balances."""
        endpoints = {
            "fees": self.client.async_get_fees_recommended(),
            "mempool": self.client.async_get_mempool(),
            "tip_hash": self.client.async_get_tip_hash(),
            "difficulty": self.client.async_get_difficulty_adjustment(),
            "hashrate": self.client.async_get_hashrate(),
            "reward_stats": self.client.async_get_reward_stats(),
            "prices": self.client.async_get_prices(),
        }
    
        results = await asyncio.gather(
            *endpoints.values(),
            return_exceptions=True,
        )
    
        data: dict[str, Any] = {}
        failed = []
    
        for name, result in zip(endpoints.keys(), results):
            if isinstance(result, Exception):
                failed.append(name)
                LOGGER.warning(
                    "Mempool endpoint '%s' failed: %s – using last known data if available",
                    name,
                    result,
                )
            else:
                data[name] = result
    
        # Wenn zu viele Endpunkte fehlschlagen, als Fehler behandeln
        if len(failed) >= 4:
            raise UpdateFailed(
                f"Too many mempool endpoints failed: {', '.join(failed)}"
            )
    
        # Wenn kritische Daten fehlen und wir noch keine alten Daten haben
        if not data and self.data is None:
            raise UpdateFailed("No mempool data could be fetched")
    
        # Vorherige Daten beibehalten, wo neue fehlen
        if self.data:
            for key in ("fees", "mempool", "difficulty", "hashrate", "reward_stats", "prices"):
                if key not in data:
                    data[key] = self.data.get(key)
    
        # Latest block separat holen (braucht tip_hash)
        tip_hash = data.get("tip_hash")
        if tip_hash is None and self.data:
            tip_hash = self.data.get("tip_hash")
    
        latest_block = None
        if tip_hash:
            try:
                latest_block = await self.client.async_get_block(tip_hash)
            except MempoolApiError as err:
                LOGGER.warning(
                    "Mempool endpoint 'block' failed: %s – using last known data if available",
                    err,
                )
                if self.data:
                    latest_block = self.data.get("latest_block")
    
        price_data = data.get("prices") or {}
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
            "fees": data.get("fees"),
            "mempool": data.get("mempool"),
            "tip_height": latest_block.get("height") if latest_block else None,
            "tip_hash": tip_hash,
            "difficulty_adjustment": data.get("difficulty"),
            "hashrate": data.get("hashrate"),
            "reward_stats": data.get("reward_stats"),
            "latest_block": latest_block,
            "price": price,
            "address_data": address_data,
        }    
