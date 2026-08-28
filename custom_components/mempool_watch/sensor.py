from __future__ import annotations

from collections.abc import Callable
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_ADDRESSES,
    CONF_CURRENCIES,
    DEFAULT_CURRENCIES,
)
from .data import MempoolConfigEntry
from .entity import MempoolEntity


def _safe(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    """Nested dict get with fallback."""
    cur: Any = data
    for key in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(key)
        if cur is None:
            return default
    return cur


def _next_block(data: dict[str, Any]) -> dict[str, Any]:
    """First projected mempool block or empty."""
    blocks = data.get("mempool_blocks") or []
    return blocks[0] if blocks else {}


SENSOR_DATA_MAP: dict[str, Callable[[dict[str, Any]], Any]] = {
    "fastest_fee": lambda data: data["fees"]["fastestFee"],
    "half_hour_fee": lambda data: data["fees"]["halfHourFee"],
    "hour_fee": lambda data: data["fees"]["hourFee"],
    "economy_fee": lambda data: data["fees"]["economyFee"],
    "minimum_fee": lambda data: data["fees"]["minimumFee"],
    "mempool_tx_count": lambda data: data["mempool"]["count"],
    "mempool_size": lambda data: data["mempool"]["vsize"],
    "mempool_total_fee": lambda data: round(
        int(data["mempool"].get("total_fee", 0)) / 1e8, 8
    ),
    "block_height": lambda data: data["tip_height"],
    "difficulty_progress": lambda data: data["difficulty_adjustment"][
        "progressPercent"
    ],
    "difficulty_change": lambda data: data["difficulty_adjustment"][
        "difficultyChange"
    ],
    "remaining_blocks": lambda data: data["difficulty_adjustment"][
        "remainingBlocks"
    ],
    "remaining_time": lambda data: round(
        int(data["difficulty_adjustment"].get("remainingTime", 0)) / 3600, 1
    ),
    "previous_retarget": lambda data: data["difficulty_adjustment"].get(
        "previousRetarget"
    ),
    "next_retarget_height": lambda data: data["difficulty_adjustment"].get(
        "nextRetargetHeight"
    ),
    "avg_block_time": lambda data: round(
        int(data["difficulty_adjustment"].get("timeAvg", 0)) / 1000 / 60, 1
    ),
    "network_hashrate": lambda data: round(
        data["hashrate"]["currentHashrate"] / 1e18,
        2,
    ),
    "network_difficulty": lambda data: data["hashrate"][
        "currentDifficulty"
    ],
    "total_miners_reward": lambda data: round(
        int(data["reward_stats"]["totalReward"]) / 1e8,
        4,
    ),
    "avg_block_fees": lambda data: round(
        int(data["reward_stats"]["totalFee"]) / 144 / 1e8,
        8,
    ),
    "avg_tx_fee": lambda data: round(
        int(data["reward_stats"]["totalFee"])
        / max(int(data["reward_stats"]["totalTx"]), 1),
        0,
    ),
    "latest_block_miner": lambda data: _safe(
        data, "latest_block", "extras", "pool", "name"
    ),
    "latest_block_tx_count": lambda data: data["latest_block"].get("tx_count"),
    "latest_block_size": lambda data: data["latest_block"].get("size"),
    "latest_block_weight": lambda data: data["latest_block"].get("weight"),
    "latest_block_median_fee": lambda data: _safe(
        data, "latest_block", "extras", "medianFee"
    ),
    "latest_block_total_fees": lambda data: round(
        int(_safe(data, "latest_block", "extras", "totalFees", default=0) or 0)
        / 1e8,
        8,
    ),
    "latest_block_reward": lambda data: round(
        int(_safe(data, "latest_block", "extras", "reward", default=0) or 0)
        / 1e8,
        8,
    ),
    "next_block_median_fee": lambda data: round(
        float(_next_block(data).get("medianFee") or 0), 1
    ),
    "next_block_n_tx": lambda data: _next_block(data).get("nTx"),
    "projected_blocks": lambda data: len(data.get("mempool_blocks") or []),
    "btc_price": lambda data: data["price"].get("USD"),
}


SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    # --- Core (enabled by default) ---
    SensorEntityDescription(
        key="fastest_fee",
        name="Fastest fee",
        icon="mdi:speedometer",
        native_unit_of_measurement="sat/vB",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="half_hour_fee",
        name="Half hour fee",
        icon="mdi:speedometer-medium",
        native_unit_of_measurement="sat/vB",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="hour_fee",
        name="Hour fee",
        icon="mdi:speedometer-slow",
        native_unit_of_measurement="sat/vB",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="economy_fee",
        name="Economy fee",
        icon="mdi:cash",
        native_unit_of_measurement="sat/vB",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="minimum_fee",
        name="Minimum fee",
        icon="mdi:cash-minus",
        native_unit_of_measurement="sat/vB",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="mempool_tx_count",
        name="Mempool TX count",
        icon="mdi:counter",
        native_unit_of_measurement="transactions",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="mempool_size",
        name="Mempool size",
        icon="mdi:database",
        native_unit_of_measurement="vB",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="block_height",
        name="Block height",
        icon="mdi:cube",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="difficulty_progress",
        name="Difficulty adjustment progress",
        icon="mdi:progress-clock",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="difficulty_change",
        name="Difficulty adjustment estimate",
        icon="mdi:chart-timeline-variant",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="remaining_blocks",
        name="Difficulty adjustment remaining blocks",
        icon="mdi:cube-unfolded",
        native_unit_of_measurement="blocks",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="network_hashrate",
        name="Network hashrate",
        icon="mdi:flash",
        native_unit_of_measurement="EH/s",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="network_difficulty",
        name="Network difficulty",
        icon="mdi:gauge",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
    ),
    SensorEntityDescription(
        key="total_miners_reward",
        name="Total miners reward (144 blocks)",
        icon="mdi:bitcoin",
        native_unit_of_measurement="BTC",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=4,
    ),
    SensorEntityDescription(
        key="avg_block_fees",
        name="Avg block fees (144 blocks)",
        icon="mdi:cash-multiple",
        native_unit_of_measurement="BTC",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=8,
    ),
    SensorEntityDescription(
        key="avg_tx_fee",
        name="Avg TX fee (144 blocks)",
        icon="mdi:cash",
        native_unit_of_measurement="sats",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
    ),
    SensorEntityDescription(
        key="latest_block_miner",
        name="Latest block miner",
        icon="mdi:pickaxe",
    ),
    SensorEntityDescription(
        key="btc_price",
        name="BTC price",
        icon="mdi:currency-usd",
        native_unit_of_measurement="USD",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
    ),
    # --- Optional (disabled by default) ---
    SensorEntityDescription(
        key="mempool_total_fee",
        name="Mempool total fees",
        icon="mdi:cash-multiple",
        native_unit_of_measurement="BTC",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=8,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="remaining_time",
        name="Difficulty adjustment remaining time",
        icon="mdi:timer-sand",
        native_unit_of_measurement="h",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="previous_retarget",
        name="Previous difficulty retarget",
        icon="mdi:history",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="next_retarget_height",
        name="Next retarget height",
        icon="mdi:flag-checkered",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="avg_block_time",
        name="Average block time",
        icon="mdi:clock-outline",
        native_unit_of_measurement="min",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="latest_block_tx_count",
        name="Latest block TX count",
        icon="mdi:counter",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="latest_block_size",
        name="Latest block size",
        icon="mdi:file-cabinet",
        native_unit_of_measurement="B",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="latest_block_weight",
        name="Latest block weight",
        icon="mdi:weight",
        native_unit_of_measurement="WU",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="latest_block_median_fee",
        name="Latest block median fee",
        icon="mdi:cash",
        native_unit_of_measurement="sat/vB",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="latest_block_total_fees",
        name="Latest block total fees",
        icon="mdi:cash-multiple",
        native_unit_of_measurement="BTC",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=8,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="latest_block_reward",
        name="Latest block reward",
        icon="mdi:bitcoin",
        native_unit_of_measurement="BTC",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=8,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="next_block_median_fee",
        name="Next block median fee",
        icon="mdi:timeline-clock",
        native_unit_of_measurement="sat/vB",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="next_block_n_tx",
        name="Next block TX count",
        icon="mdi:counter",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="projected_blocks",
        name="Projected mempool blocks",
        icon="mdi:view-week",
        native_unit_of_measurement="blocks",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: MempoolConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Mempool Watch sensors from a config entry."""
    coordinator = entry.runtime_data.coordinator
    conf = {**entry.data, **entry.options}

    # Configured fiat currencies.
    #
    # Configuration values are stored as lowercase ISO codes:
    # eur, gbp, chf, ...
    currencies: list[str] = list(
        dict.fromkeys(
            str(currency).lower()
            for currency in conf.get(
                CONF_CURRENCIES,
                DEFAULT_CURRENCIES,
            )
            if currency
        )
    )

    addresses: list[dict[str, str]] = conf.get(
        CONF_ADDRESSES,
        []
    ) or []

    entities: list[SensorEntity] = []

    # ------------------------------------------------------------------
    # Standard sensors
    # ------------------------------------------------------------------

    for description in SENSOR_DESCRIPTIONS:
        if description.key == "btc_price":
            entities.append(
                MempoolPriceSensor(
                    coordinator,
                    description,
                )
            )
        elif description.key == "latest_block_miner":
            entities.append(
                MempoolLatestBlockMinerSensor(
                    coordinator,
                    description,
                )
            )
        else:
            entities.append(
                MempoolSensor(
                    coordinator,
                    description,
                )
            )

    # ------------------------------------------------------------------
    # Configured BTC fiat price sensors
    # ------------------------------------------------------------------
    #
    # Every selected currency gets its own entity:
    #
    # sensor.btc_price_eur
    # sensor.btc_price_gbp
    # sensor.btc_price_chf
    # ...
    #
    # USD is already provided by the main BTC price sensor.
    # ------------------------------------------------------------------

    for currency in currencies:
        currency_code = currency.upper()

        if currency_code == "USD":
            continue

        description = SensorEntityDescription(
            key=f"btc_price_{currency}",
            name=f"BTC price ({currency_code})",
            icon=(
                "mdi:currency-eur"
                if currency_code == "EUR"
                else "mdi:cash"
            ),
            native_unit_of_measurement=currency_code,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_display_precision=0,
        )

        entities.append(
            MempoolCurrencyPriceSensor(
                coordinator,
                description,
                currency_code,
            )
        )

    # ------------------------------------------------------------------
    # BTC address sensors
    # ------------------------------------------------------------------

    for item in addresses:
        name = item.get("name") or item["address"][:12]
        address = item["address"]

        description = SensorEntityDescription(
            key=f"address_{address}",
            name=name,
            icon="mdi:bitcoin",
            native_unit_of_measurement="BTC",
            state_class=SensorStateClass.TOTAL,
            suggested_display_precision=8,
            entity_category=EntityCategory.DIAGNOSTIC,
        )

        entities.append(
            MempoolAddressSensor(
                coordinator,
                description,
                address,
            )
        )

    async_add_entities(entities)


class MempoolSensor(MempoolEntity, SensorEntity):
    """Representation of a Mempool Watch sensor."""

    @property
    def native_value(self) -> Any | None:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None

        try:
            return SENSOR_DATA_MAP[
                self.entity_description.key
            ](self.coordinator.data)
        except (KeyError, TypeError, ValueError):
            return None


class MempoolLatestBlockMinerSensor(MempoolSensor):
    """Latest block miner sensor with pool attributes."""

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return pool slug and miner names as attributes."""
        if self.coordinator.data is None:
            return None

        try:
            pool = self.coordinator.data["latest_block"]["extras"][
                "pool"
            ]

            return {
                "slug": pool.get("slug"),
                "miner_names": pool.get("minerNames"),
            }
        except (KeyError, TypeError):
            return None


class MempoolPriceSensor(MempoolSensor):
    """BTC price in USD with other currencies as attributes."""

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return other available currencies as attributes."""
        if self.coordinator.data is None:
            return None

        price = self.coordinator.data.get("price", {})

        return {
            key.lower(): value
            for key, value in price.items()
            if key.upper() != "USD"
        }


class MempoolCurrencyPriceSensor(MempoolEntity, SensorEntity):
    """BTC price sensor for a configured fiat currency."""

    def __init__(
        self,
        coordinator,
        description: SensorEntityDescription,
        currency: str,
    ) -> None:
        """Initialize the currency price sensor."""
        super().__init__(coordinator, description)

        self._currency = currency.upper()

        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_price_"
            f"{self._currency.lower()}"
        )

    @property
    def native_value(self) -> Any | None:
        """Return the BTC price in the selected currency."""
        if self.coordinator.data is None:
            return None

        price = self.coordinator.data.get("price", {})

        # Mempool normally returns uppercase ISO currency keys.
        # The fallback makes this robust against lowercase keys.
        value = price.get(self._currency)

        if value is None:
            value = price.get(self._currency.lower())

        return value


class MempoolAddressSensor(MempoolEntity, SensorEntity):
    """BTC address sensor."""

    def __init__(
        self,
        coordinator,
        description: SensorEntityDescription,
        address: str,
    ) -> None:
        """Initialize with the on-chain address."""
        super().__init__(coordinator, description)

        self._address = address

        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_addr_{address}"
        )

    def _stats(self) -> dict[str, Any] | None:
        """Return parsed stats for this address."""
        if self.coordinator.data is None:
            return None

        data = self.coordinator.data.get("address_data") or {}

        return data.get(self._address)

    @property
    def native_value(self) -> float | None:
        """Return confirmed on-chain balance in BTC."""
        stats = self._stats()

        if not stats:
            return None

        return stats.get("confirmed_balance")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose unconfirmed values and the full address."""
        attrs: dict[str, Any] = {
            "address": self._address,
        }

        stats = self._stats()

        if not stats:
            return attrs

        attrs.update(
            {
                "pending_change": stats.get("pending_change"),
                "pending_incoming": stats.get("pending_incoming"),
                "pending_outgoing": stats.get("pending_outgoing"),
                "unconfirmed_count": stats.get("unconfirmed_count"),
                "confirmed_balance": stats.get("confirmed_balance"),
            }
        )

        return attrs
