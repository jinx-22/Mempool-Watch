"""Async API client for a mempool instance (local or remote)."""

from __future__ import annotations

import asyncio
import ssl
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant


class MempoolApiError(Exception):
    """Base exception for Mempool API errors."""


class MempoolApiConnectionError(MempoolApiError):
    """Exception for connection errors."""


def _build_ssl_with_ca(ca_cert: str) -> ssl.SSLContext:
    """Build SSL context that trusts an extra CA (blocking – run in executor)."""
    pem = ca_cert.strip()
    if "BEGIN CERTIFICATE" not in pem:
        pem = (
            "-----BEGIN CERTIFICATE-----\n"
            + pem
            + "\n-----END CERTIFICATE-----"
        )

    # create_default_context + load_verify_locations do disk I/O → executor only
    ctx = ssl.create_default_context()
    try:
        ctx.load_verify_locations(cadata=pem)
    except ssl.SSLError as err:
        raise MempoolApiError(f"Invalid CA certificate: {err}") from err
    return ctx


async def async_build_ssl(
    hass: HomeAssistant,
    verify_ssl: bool,
    ca_cert: str | None,
) -> bool | ssl.SSLContext:
    """Return aiohttp ssl= argument without blocking the event loop.

    - verify_ssl=False → False (skip verification)
    - no custom CA → True (system / HA default trust store)
    - custom CA → SSLContext built in executor
    """
    if not verify_ssl:
        return False

    pem = (ca_cert or "").strip()
    if not pem:
        return True

    return await hass.async_add_executor_job(_build_ssl_with_ca, pem)


class MempoolApiClient:
    """Lightweight async client for a configured mempool base URL."""

    def __init__(
        self,
        base_url: str,
        session: aiohttp.ClientSession,
        ssl: bool | ssl.SSLContext = True,
    ) -> None:
        """Initialize the API client.

        Args:
            base_url: Base URL of the mempool instance.
            session: Shared aiohttp ClientSession from Home Assistant.
            ssl: Passed to aiohttp (True / False / SSLContext).
                Build with async_build_ssl() before creating the client.
        """
        self._base_url = base_url.rstrip("/")
        self._session = session
        self._ssl = ssl

    async def _get(self, path: str) -> Any:
        """Make a GET request with short timeout and return parsed response."""
        url = f"{self._base_url}{path}"

        try:
            timeout = aiohttp.ClientTimeout(total=12, connect=5)
            async with self._session.get(
                url, ssl=self._ssl, timeout=timeout
            ) as resp:
                resp.raise_for_status()
                if resp.content_type == "text/plain":
                    return await resp.text()
                return await resp.json(content_type=None)
        except (
            aiohttp.ClientConnectionError,
            TimeoutError,
            asyncio.TimeoutError,
        ) as err:
            raise MempoolApiConnectionError(
                f"Error connecting to {url}"
            ) from err
        except aiohttp.ClientResponseError as err:
            raise MempoolApiError(
                f"Error response {err.status} from {url}"
            ) from err
        except Exception as err:
            raise MempoolApiError(
                f"Unexpected error fetching {url}"
            ) from err

    async def async_get_backend_info(self) -> dict[str, Any]:
        """Connection-test endpoint."""
        return await self._get("/api/v1/backend-info")

    async def async_get_fees_recommended(self) -> dict[str, Any]:
        """Recommended fees."""
        return await self._get("/api/v1/fees/recommended")

    async def async_get_mempool(self) -> dict[str, Any]:
        """Mempool statistics."""
        return await self._get("/api/mempool")

    async def async_get_tip_hash(self) -> str:
        """Current tip block hash."""
        return await self._get("/api/blocks/tip/hash")

    async def async_get_block(self, block_hash: str) -> dict[str, Any]:
        """Block details by hash."""
        return await self._get(f"/api/v1/block/{block_hash}")

    async def async_get_difficulty_adjustment(self) -> dict[str, Any]:
        """Difficulty adjustment info."""
        return await self._get("/api/v1/difficulty-adjustment")

    async def async_get_hashrate(self) -> dict[str, Any]:
        """Network hashrate (1 month window)."""
        return await self._get("/api/v1/mining/hashrate/1m")

    async def async_get_reward_stats(self) -> dict[str, Any]:
        """Mining reward stats for last 144 blocks."""
        return await self._get("/api/v1/mining/reward-stats/144")

    async def async_get_prices(self) -> dict[str, Any]:
        """Current prices."""
        return await self._get("/api/v1/prices")

    async def async_get_mempool_blocks(self) -> list[dict[str, Any]]:
        """Projected next blocks from the mempool (fee estimates)."""
        return await self._get("/api/v1/fees/mempool-blocks")

    async def async_get_address(self, address: str) -> dict[str, Any]:
        """Address stats (balance via chain_stats / mempool_stats)."""
        return await self._get(f"/api/address/{address}")
