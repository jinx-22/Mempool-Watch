"""Async API client for a mempool instance (local or remote)."""

from __future__ import annotations

import asyncio
from typing import Any
from urllib.parse import urlparse

import aiohttp


class MempoolApiError(Exception):
    """Base exception for Mempool API errors."""


class MempoolApiConnectionError(MempoolApiError):
    """Exception for connection errors."""


class MempoolApiClient:
    """Lightweight async client for a configured mempool base URL."""

    def __init__(self, base_url: str, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._base_url = base_url.rstrip("/")
        self._session = session

    async def _get(self, path: str) -> Any:
        """Make a GET request with short timeout and return parsed response."""
        url = f"{self._base_url}{path}"
        parsed = urlparse(url)

        ssl_verify: bool | None = True
        if parsed.scheme == "https" and parsed.hostname:
            host = parsed.hostname.lower()
            if (
                host.endswith(".local")
                or host in ("localhost", "127.0.0.1", "::1")
                or host.startswith("192.168.")
                or host.startswith("10.")
                or host.startswith("172.")
            ):
                ssl_verify = False

        try:
            timeout = aiohttp.ClientTimeout(total=12, connect=5)
            async with self._session.get(url, ssl=ssl_verify, timeout=timeout) as resp:
                resp.raise_for_status()
                if resp.content_type == "text/plain":
                    return await resp.text()
                return await resp.json(content_type=None)
        except (aiohttp.ClientConnectionError, TimeoutError, asyncio.TimeoutError) as err:
            raise MempoolApiConnectionError(f"Error connecting to {url}") from err
        except aiohttp.ClientResponseError as err:
            raise MempoolApiError(f"Error response {err.status} from {url}") from err
        except Exception as err:
            raise MempoolApiError(f"Unexpected error fetching {url}") from err

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

    async def async_get_address(self, address: str) -> dict[str, Any]:
        """Address stats (balance via chain_stats / mempool_stats)."""
        return await self._get(f"/api/address/{address}")
