"""Constants for the Mempool Watch integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "mempool_watch"
ATTRIBUTION = "Data provided by mempool instance"

CONF_BASE_URL = "base_url"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_CURRENCIES = "currencies"
CONF_ADDRESSES = "addresses"  # list[{"name": str, "address": str}]
CONF_VERIFY_SSL = "verify_ssl"
CONF_CA_CERT = "ca_cert"  # optional PEM content of a custom CA (e.g. Start9 Root)

DEFAULT_BASE_URL = "http://192.168.1.1:8999"
DEFAULT_UPDATE_INTERVAL = 60
DEFAULT_VERIFY_SSL = True
MIN_UPDATE_INTERVAL = 5
MAX_UPDATE_INTERVAL = 600

# All fiat currencies supported by the integration.
SUPPORTED_CURRENCIES = [
    "eur",
    "gbp",
    "cad",
    "chf",
    "aud",
    "jpy",
    "cny",
    "inr",
    "brl",
    "krw",
    "try",
    "pln",
    "sek",
    "nok",
    "dkk",
    "czk",
    "huf",
    "ils",
    "mxn",
    "sgd",
    "hkd",
    "nzd",
    "zar",
    "rub",
    "thb",
    "twd",
    "php",
    "idr",
    "myr",
    "vnd",
]

# Currency options displayed in the config flow.
CURRENCY_CHOICES = SUPPORTED_CURRENCIES

# Default currency for a new installation.
DEFAULT_CURRENCIES = ["eur"]
