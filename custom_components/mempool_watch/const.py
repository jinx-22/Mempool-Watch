"""Constants for the Mempool Watch integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "mempool_watch"
ATTRIBUTION = "Data provided by mempool instance"

CONF_BASE_URL = "base_url"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_SECONDARY_CURRENCY = "secondary_currency"
CONF_ADDRESSES = "addresses"  # list[{"name": str, "address": str}]

DEFAULT_BASE_URL = "http://127.0.0.1:8999"
DEFAULT_UPDATE_INTERVAL = 60
MIN_UPDATE_INTERVAL = 5
MAX_UPDATE_INTERVAL = 600

DEFAULT_SECONDARY_CURRENCY = "none"
CURRENCY_CHOICES = [
    "none",
    "EUR",
    "GBP",
    "CAD",
    "CHF",
    "AUD",
    "JPY",
    "CNY",
    "INR",
    "BRL",
    "KRW",
    "TRY",
    "PLN",
    "SEK",
    "NOK",
    "DKK",
    "CZK",
    "HUF",
    "ILS",
    "MXN",
    "SGD",
    "HKD",
    "NZD",
    "ZAR",
    "RUB",
    "THB",
    "TWD",
    "PHP",
    "IDR",
    "MYR",
    "VND",
]
