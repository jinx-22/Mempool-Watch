"""Typed runtime data for the Mempool Watch integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from homeassistant.config_entries import ConfigEntry

from .api import MempoolApiClient
from .coordinator import MempoolDataUpdateCoordinator


@dataclass
class MempoolData:
    """Runtime data stored in the config entry."""

    client: MempoolApiClient
    coordinator: MempoolDataUpdateCoordinator


MempoolConfigEntry: TypeAlias = ConfigEntry[MempoolData]
