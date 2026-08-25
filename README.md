<h1>
  <img height="96" alt="logo" src="https://github.com/user-attachments/assets/16cc0d73-6adc-4495-9808-d2ee54aa495e" />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Home Assistant Integration
</h1>

---

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-blue?style=flat-square)](https://www.home-assistant.io/)
[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=flat-square)](https://github.com/hacs/integration)
[![Release](https://img.shields.io/github/v/release/jinx-22/mempool_watch?sort=semver&style=flat-square)](https://github.com/jinx-22/mempool_watch/releases)
[![License](https://img.shields.io/github/license/jinx-22/mempool_watch?style=flat-square)](LICENSE)
[![Usage](https://img.shields.io/badge/dynamic/json?style=flat-square&logo=home-assistant&logoColor=white&label=Usage&suffix=%20installs&color=dc3545&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.mempool_watch.total)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jinx-22&repository=mempool_watch&category=integration)
[![stars](https://img.shields.io/github/stars/jinx-22/mempool_watch)](https://github.com/jinx-22/mempool_watch/stargazers)
[![Donate Bitcoin](https://img.shields.io/badge/₿-Bitcoin-F7931A?style=flat-square)](#bitcoin)
[![Donate Lightning](https://img.shields.io/badge/⚡-Lightning-FFD700?style=flat-square)](#lightning)

🇩🇪 **[Deutsche Beschreibung](README_DE.md)**

---

## 📖 About Mempool Watch

**Mempool Watch** is a custom Home Assistant integration for monitoring the Bitcoin network using data from your locally hosted Mempool instance!

The publicly available [mempool.space](https://mempool.space/) can also be used! However, please note that entering BTC addresses when using a public Mempool instance can compromise your privacy!!!

The integration provides detailed Bitcoin network information directly as native Home Assistant entities.

Mempool Watch currently provides **18+1 Bitcoin network sensors** covering blockchain statistics, transaction fees, mempool activity, mining information, network difficulty, network hashrate, difficulty adjustments and Bitcoin price.

Mempool Watch also supports:

- An optional second BTC price entity
- An unlimited number of Bitcoin addresses
- Confirmed and unconfirmed Bitcoin address information
- The optional `btc-address-card.js` Lovelace Card

---

# 🚀 Features/Sensors

### ₿ Bitcoin Network

Monitor important Bitcoin network metrics directly in Home Assistant:

- Current block height
- Network difficulty
- Network hashrate
- Estimated difficulty adjustment
- Difficulty adjustment progress
- Remaining blocks until the next difficulty adjustment
- Latest block miner
- Average block fees
- Average transaction fees
- Total miner rewards

### 📊 Mempool

Monitor the current Bitcoin mempool:

- Mempool size
- Number of mempool transactions
- Minimum fee
- Economy fee
- Hour fee
- Half-hour fee
- Fastest fee

### 💱 Bitcoin Price

Mempool Watch provides the current BTC price and can optionally create a second BTC price entity in another currency.

### ₿ Bitcoin Addresses

Monitor an **unlimited number of Bitcoin addresses** as individual Home Assistant entities:

- Confirmed balance
- Unconfirmed incoming
- Unconfirmed outgoing
- Net pending amount
- Number of unconfirmed transactions
- Full Bitcoin address

---

# 📊 Sensors

Mempool Watch currently provides the following **18 Bitcoin network sensors**:

| Sensor | Description | Example |
|---|---|---:|
| **Avg block fees (144 blocks)** | Average block fees over the last 144 blocks | 0.02134933 BTC |
| **Avg TX fee (144 blocks)** | Average transaction fee over the last 144 blocks | 496 sats |
| **Block height** | Current Bitcoin blockchain height | 964019 |
| **BTC price** | Current Bitcoin price | 79,296 USD |
| **Difficulty adjustment estimate** | Estimated change at the next difficulty adjustment | -0.79 % |
| **Difficulty adjustment progress** | Progress toward the next difficulty adjustment | 18.4 % |
| **Difficulty adjustment remaining blocks** | Blocks remaining until the next difficulty adjustment | 1,645 blocks |
| **Economy fee** | Recommended low-priority fee rate | 1 sat/vB |
| **Fastest fee** | Recommended fee for the fastest confirmation | 3 sat/vB |
| **Half hour fee** | Recommended fee for confirmation within approximately 30 minutes | 3 sat/vB |
| **Hour fee** | Recommended fee for confirmation within approximately 1 hour | 1 sat/vB |
| **Latest block miner** | Miner or mining pool of the latest block | ViaBTC |
| **Mempool size** | Current Bitcoin mempool size | 42,485,511 vB |
| **Mempool TX count** | Number of unconfirmed transactions | 84,930 |
| **Minimum fee** | Currently lowest fee represented in the mempool | 1 sat/vB |
| **Network difficulty** | Current Bitcoin network difficulty | 125,807,076,547,198 |
| **Network hashrate** | Estimated Bitcoin network hashrate | 872.60 EH/s |
| **Total miners reward (144 blocks)** | Total miner rewards over the last 144 blocks | 453.0743 BTC |

---

# 💱 Additional BTC Price Entity

An optional **second BTC price entity** can be configured.

This allows Bitcoin to be monitored simultaneously in two different currencies.

For example:

**BTC/USD + BTC/EUR**

If no second price entity is required, **None** can be selected.

### Supported currencies

| Code | Currency |
|---|---|
| `none` | None |
| `EUR` | Euro |
| `GBP` | British Pound |
| `CAD` | Canadian Dollar |
| `CHF` | Swiss Franc |
| `AUD` | Australian Dollar |
| `JPY` | Japanese Yen |
| `CNY` | Chinese Yuan |
| `INR` | Indian Rupee |
| `BRL` | Brazilian Real |
| `KRW` | South Korean Won |
| `TRY` | Turkish Lira |
| `PLN` | Polish Złoty |
| `SEK` | Swedish Krona |
| `NOK` | Norwegian Krone |
| `DKK` | Danish Krone |
| `CZK` | Czech Koruna |
| `HUF` | Hungarian Forint |
| `ILS` | Israeli New Shekel |
| `MXN` | Mexican Peso |
| `SGD` | Singapore Dollar |
| `HKD` | Hong Kong Dollar |
| `NZD` | New Zealand Dollar |
| `ZAR` | South African Rand |
| `RUB` | Russian Ruble |
| `THB` | Thai Baht |
| `TWD` | New Taiwan Dollar |
| `PHP` | Philippine Peso |
| `IDR` | Indonesian Rupiah |
| `MYR` | Malaysian Ringgit |
| `VND` | Vietnamese Đồng |

---

# ₿ Bitcoin Address Monitoring

Mempool Watch can monitor individual Bitcoin addresses directly in Home Assistant.

There is **no fixed limit on the number of Bitcoin addresses** that can be added.

Each Bitcoin address is created as its own Home Assistant entity.

### Available attributes

| Attribute | Description |
|---|---|
| `chain_stats` | Confirmed on-chain balance |
| `pending_incoming` | Unconfirmed incoming amount |
| `pending_outgoing` | Unconfirmed outgoing amount |
| `pending_change` | Net pending amount: incoming − outgoing |
| `unconfirmed_count` | Number of unconfirmed transactions |
| `confirmed_balance` | Confirmed balance |
| `address` | Full Bitcoin address |

### Pending Change

The `pending_change` attribute represents the current unconfirmed net amount:

**Incoming − Outgoing**

A positive value means that more Bitcoin is currently pending incoming.

A negative value means that more Bitcoin is currently pending outgoing.

This allows both the confirmed balance and the current **unconfirmed activity** of a Bitcoin address to be monitored.

---

# 🖼️ Optional Bitcoin Address Card

An additional custom Lovelace card can be used as a dedicated Bitcoin Address Card.

### `btc-address-card.js`

The card can display:

- Confirmed balance
- Unconfirmed incoming
- Unconfirmed outgoing
- Pending Change
- Number of unconfirmed transactions
- Bitcoin address

<img width="485" height="310" alt="btc-address-card" src="https://github.com/user-attachments/assets/ff4caa01-b19b-418c-9c71-8f789c671f44" />

The card is **completely optional** and is not required for the Mempool Watch integration.

### Repository

[btc-address-card.js Repository](https://github.com/jinx-22/btc-address-card)

---

# 📦 Installation

## HACS (coming → approximately 2 weeks)

The recommended installation method is **HACS**.

(It is currently being worked on and still needs to be added. This may take approximately 2 weeks!)

1. Open **HACS**
2. Select **Integrations**
3. Search for **Mempool Watch**
4. Install the integration
5. Restart Home Assistant
6. Open **Settings → Devices & services**
7. Select **Add Integration**
8. Search for **Mempool Watch**
9. Complete the configuration

### Direct HACS link

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jinx-22&repository=mempool_watch&category=integration)

---

## Manual Installation

Download the latest version and copy the `mempool_watch` directory to:

`/config/custom_components/`

Restart Home Assistant after copying the files.

Then go to:

**Settings → Devices & services → Add Integration**

and search for:

**Mempool Watch**

---

# ⚙️ Configuration

Mempool Watch is fully configured through the Home Assistant interface.

No YAML configuration is required.

After installation:

**Settings → Devices & services → Add Integration → Mempool Watch**

The integration allows you to configure the available options, optionally select a second BTC price currency and add Bitcoin addresses.

---

# 🌐 Data Source

Mempool Watch uses data from the entered/connected Mempool instance.

The Bitcoin network data is converted by the integration into native Home Assistant entities.

These entities can be used for:

- Dashboards
- Automations
- Scripts
- Templates
- Notifications
- Statistics
- Mining dashboards

---

# 🐛 Bugs & Feature Requests

If you find a bug, please create an issue in this repository.

When reporting a problem, please provide:

- Home Assistant version
- Mempool Watch version
- Relevant log output
- Steps to reproduce
- Screenshots where useful

---

# 🧡 Support & Donations

If you like this project and find it useful, I greatly appreciate a small donation.

Every contribution helps support further development 🚀

## Lightning

<p align="center">
⚡ <b>Address:</b>
<br><br>
<code>usefulplay52@walletofsatoshi.com</code>
<br>

<img height="450" alt="Self_Wallet of Satoshi" src="https://github.com/user-attachments/assets/65cc18d9-05d1-4a00-8ccc-9922fdb54baf" />
<br><br>
or:
<br><br></p>

## Bitcoin

<div align="center">
<img width="100" height="100" alt="Bitcoin_100px" src="https://github.com/user-attachments/assets/f74cad36-8c05-4a33-89cd-b998075af33b" />
<br><br>

<code>bc1qkz7mtp23cmshxnru96lzgeayu0urlysvqk5vry</code>
<br>

<img height="500" alt="Donations_240px" src="https://github.com/user-attachments/assets/196f68e4-b0e8-4f27-bded-8c4fe13b9d45" />
<br><br>
</div>

Thank you very much for your support!

And please leave a free ⭐ on GitHub so others can discover the project too.

---

# 📜 License

This project is licensed under the **Apache License 2.0**.

See [LICENSE](LICENSE) for the complete license text.

---

# ⚠️ Disclaimer

Mempool Watch is an independent open-source project.

It is **not an official product of mempool.space, Home Assistant or any other third-party organization**.

The integration uses data provided by external Bitcoin services.

Use this integration at your own risk.
