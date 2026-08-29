"""DataUpdateCoordinator for the Mempool Watch integration."""

from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import Any, Awaitable, Callable

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import MempoolApiClient, MempoolApiError
from .const import DEFAULT_UPDATE_INTERVAL, DOMAIN, LOGGER

_SATS = 1e8

# Temporäre Netzwerk-/Gateway-Fehler (Router-Disconnect, Umbrel-Neustart, …)
_TRANSIENT_MARKERS = (
    "502",
    "503",
    "504",
    "connection",
    "connect",
    "timeout",
    "temporarily unavailable",
    "bad gateway",
    "gateway timeout",
)

_MAX_RETRIES = 3
_RETRY_DELAYS = (2.0, 5.0)  # etwas großzügiger für Router-Reconnects


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


def _short_err(err: BaseException) -> str:
    """Kurze, lesbare Fehlermeldung fürs Log."""
    text = str(err)
    lower = text.lower()

    if "503" in text:
        return "Mempool temporarily unavailable (HTTP 503)"
    if "502" in text:
        return "Mempool bad gateway (HTTP 502)"
    if "504" in text:
        return "Mempool gateway timeout (HTTP 504)"
    if "connect" in lower:
        return "Cannot connect to Mempool instance"
    if "timeout" in lower:
        return "Timeout talking to Mempool instance"
    if "ssl" in lower or "certificate" in lower:
        return "SSL/certificate error"

    return text if len(text) <= 160 else text[:157] + "…"


def _is_transient(err: BaseException) -> bool:
    """True bei typischen kurzzeitigen Ausfällen."""
    text = str(err).lower()
    return any(marker in text for marker in _TRANSIENT_MARKERS)


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
        # Endpoints, die gerade temporär offline sind (kein Log-Spam)
        self._degraded: set[str] = set()

    async def _fetch_with_retry(
        self,
        name: str,
        request: Callable[[], Awaitable[Any]],
    ) -> Any:
        """Ein Endpoint mit Retry bei transienten Fehlern."""
        last_error: Exception | None = None

        for attempt in range(_MAX_RETRIES):
            try:
                result = await request()

                if name in self._degraded:
                    LOGGER.info("Mempool endpoint '%s' recovered", name)
                    self._degraded.discard(name)

                return result

            except Exception as err:
                last_error = err

                if not _is_transient(err):
                    raise

                if attempt < _MAX_RETRIES - 1:
                    await asyncio.sleep(_RETRY_DELAYS[attempt])
                    continue

                # Alle Retries fehlgeschlagen → nur einmal warnen
                if name not in self._degraded:
                    LOGGER.warning(
                        "Mempool endpoint '%s' temporarily unavailable: %s "
                        "– using last known data if available",
                        name,
                        _short_err(err),
                    )
                    self._degraded.add(name)

        if last_error is not None:
            raise last_error

        raise MempoolApiError(f"Unknown error fetching '{name}'")

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch network endpoints and configured address balances."""

        endpoints: dict[str, Callable[[], Awaitable[Any]]] = {
            "fees": self.client.async_get_fees_recommended,
            "mempool": self.client.async_get_mempool,
            "tip_hash": self.client.async_get_tip_hash,
            "difficulty": self.client.async_get_difficulty_adjustment,
            "hashrate": self.client.async_get_hashrate,
            "reward_stats": self.client.async_get_reward_stats,
            "prices": self.client.async_get_prices,
        }

        results = await asyncio.gather(
            *[self._fetch_with_retry(name, req) for name, req in endpoints.items()],
            return_exceptions=True,
        )

        data: dict[str, Any] = {}
        for name, result in zip(endpoints.keys(), results):
            if isinstance(result, Exception):
                if not _is_transient(result):
                    LOGGER.warning(
                        "Mempool endpoint '%s' failed: %s "
                        "– using last known data if available",
                        name,
                        result,
                    )
            else:
                data[name] = result

        # Noch nie Daten bekommen → Coordinator muss fehlschlagen
        if not data and self.data is None:
            raise UpdateFailed("No mempool data could be fetched")

        # Vorherige gültige Werte weiterverwenden
        if self.data:
            for key in (
                "fees",
                "mempool",
                "tip_hash",
                "difficulty",
                "hashrate",
                "reward_stats",
                "prices",
            ):
                if key not in data:
                    data[key] = self.data.get(key)

        # Latest block (abhängt von tip_hash)
        tip_hash = data.get("tip_hash")
        if tip_hash is None and self.data:
            tip_hash = self.data.get("tip_hash")

        latest_block = None
        if tip_hash:
            try:
                latest_block = await self._fetch_with_retry(
                    "block",
                    lambda: self.client.async_get_block(tip_hash),
                )
            except Exception as err:
                if not _is_transient(err):
                    LOGGER.warning(
                        "Mempool endpoint 'block' failed: %s "
                        "– using last known data if available",
                        err,
                    )
                if self.data:
                    latest_block = self.data.get("latest_block")

        price_data = data.get("prices") or {}
        price = {k: v for k, v in price_data.items() if k != "time"}

        # Adressen – Fehler bleiben isoliert
        address_data: dict[str, dict[str, Any] | None] = {}
        if self.addresses:
            addr_results = await asyncio.gather(
                *[
                    self._fetch_with_retry(
                        f"address:{item['address']}",
                        lambda item=item: self.client.async_get_address(
                            item["address"]
                        ),
                    )
                    for item in self.addresses
                ],
                return_exceptions=True,
            )

            for item, result in zip(self.addresses, addr_results):
                key = item["address"]
                previous = (self.data or {}).get("address_data", {}).get(key)

                if isinstance(result, Exception):
                    if not _is_transient(result):
                        LOGGER.warning(
                            "Failed to fetch address %s: %s", key, result
                        )
                    address_data[key] = previous
                else:
                    try:
                        address_data[key] = _parse_address(result)
                    except (KeyError, TypeError, ValueError) as err:
                        LOGGER.warning(
                            "Failed to parse address %s: %s", key, err
                        )
                        address_data[key] = previous

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
