<h1>
<img alt="logo" src="https://github.com/user-attachments/assets/16cc0d73-6adc-4495-9808-d2ee54aa495e" /><br>
Home Assistant Integration
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

🇬🇧 **English** · 🇩🇪 [**Deutsch**](README_DE.md)

**Current version: v0.5.9.3**

---

## 📖 About Mempool Watch

**Mempool Watch** is a custom Home Assistant integration for monitoring the Bitcoin network through your local Mempool instance or [mempool.space](https://mempool.space/).

> **Privacy:** Do not enter BTC addresses when using a public Mempool instance.

### Highlights

- **18 core sensors** + 14 optional sensors (fees, mempool, difficulty, hashrate, mining, price)
- **Multiple BTC price entities** (select multiple fiat currencies)
- **Unlimited Bitcoin addresses** (confirmed + pending balances)
- **SSL / custom CA certificate** (Umbrel, Start9, …)
- [btc-address-card](https://github.com/jinx-22/btc-address-card) Lovelace Card included! No separate installation or additional download required!

---

# 📊 Sensors

### Core (enabled by default)

| Sensor | Description | Example |
| --- | --- | ---: |
| **Average Block Fees (144 Blocks)** | Average block fees over the last 144 blocks | 0.02134933 BTC |
| **Average TX Fee (144 Blocks)** | Average transaction fee over the last 144 blocks | 496 sats |
| **Block Height** | Current blockchain height | 964019 |
| **BTC Price** | BTC price (USD) | 79,296 USD |
| **Difficulty Adjustment Estimate** | Estimated next difficulty adjustment | -0.79 % |
| **Difficulty Adjustment Progress** | Progress toward the next retarget | 18.4 % |
| **Blocks Remaining Until Difficulty Adjustment** | Blocks remaining until the next retarget | 1,645 blocks |
| **Economy Fee** | Fee for low-priority transactions | 1 sat/vB |
| **Fastest Fee** | Fee for the next block | 3 sat/vB |
| **Half-Hour Fee** | Fee for confirmation in approximately 30 minutes | 3 sat/vB |
| **Hour Fee** | Fee for confirmation in approximately 1 hour | 1 sat/vB |
| **Latest Block Miner** | Miner / pool of the latest block | ViaBTC |
| **Mempool Size** | Current mempool size | 42,485,511 vB |
| **Mempool TX Count** | Number of unconfirmed transactions | 84,930 |
| **Minimum Fee** | Lowest fee currently in the mempool | 1 sat/vB |
| **Network Difficulty** | Current network difficulty | 125,807,076,547,198 |
| **Network Hashrate** | Estimated network hashrate | 872.60 EH/s |
| **Total Miner Rewards (144 Blocks)** | Total miner rewards over the last 144 blocks | 453.0743 BTC |

<img width="20%" alt="sensors" src="https://github.com/user-attachments/assets/30fb3d5c-c1a2-46ad-a84e-da43aad38fa3" />

### Optional (disabled by default)

Enable these sensors in the Entity Registry if required:

| Sensor | Description |
| --- | --- |
| **Total Mempool Fees** | Total fees currently contained in the mempool |
| **Time Remaining Until Difficulty Adjustment** | Hours until the next retarget |
| **Previous Difficulty Retarget** | Previous difficulty adjustment (%) |
| **Next Retarget Height** | Block height of the next retarget |
| **Average Block Time** | Average block time (min.) |
| **Last Block TX Count / Size / Weight** | Details of the latest block |
| **Last Block Median Fee / Total Fees / Reward** | Fees and reward of the latest block |
| **Next Block Median Fee / TX Count** | Projected next mempool block |
| **Projected Mempool Blocks** | Number of projected blocks |

---

# 💱 BTC Price Currencies

USD is always available. During setup or in the integration options, you can select **one or more additional fiat currencies**. A separate BTC price entity is created for each selected currency.

Supported (depending on the response from your Mempool instance at `/api/v1/prices`):

`EUR` `GBP` `CAD` `CHF` `AUD` `JPY`

With API key:

`CNY` `INR` `BRL` `KRW` `TRY` `PLN` `SEK` `NOK` `DKK` `CZK` `HUF` `ILS` `MXN` `SGD` `HKD` `NZD` `ZAR` `RUB` `THB` `TWD` `PHP` `IDR` `MYR` `VND`

> **Note:** An API key is required for additional fiat currencies. The API key must be configured in your Mempool instance under `FIAT_PRICE → API_KEY`.

<img width="80%" alt="Currencies" src="https://github.com/user-attachments/assets/0f9acf0e-ef61-480c-b25b-17bd104c2785" />

---

# ₿ Bitcoin Addresses

Add as many Bitcoin addresses as you like. Each address creates its own entity with:

| Attribute | Description |
| --- | --- |
| `confirmed_balance` | Confirmed on-chain balance |
| `pending_incoming` | Unconfirmed incoming balance |
| `pending_outgoing` | Unconfirmed outgoing balance |
| `pending_change` | Net change of the pending balance (incoming − outgoing) |
| `unconfirmed_count` | Number of unconfirmed transactions |
| `address` | Full Bitcoin address |

**Pending Change:** Positive = more pending BTC incoming, negative = more pending BTC outgoing.

---

# 🖼️ Lovelace BTC Address Card

Dedicated Lovelace Card for BTC address sensors, available in the Card Picker:

INFO here:
**[btc-address-card](https://github.com/jinx-22/btc-address-card)**

## No separate installation required — the Card is already included with Mempool Watch!

<img width="80%" alt="BTC Address Card" src="https://github.com/user-attachments/assets/29846f5d-aa18-420e-b41b-534fd14aac06" />
<img width="80%" alt="BTC Address Card Configuration" src="https://github.com/user-attachments/assets/6a506418-7be7-457f-8bca-f5a6dafb28c3" />

---

# 📦 Installation

## Easy Installation → [![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jinx-22&repository=mempool_watch&category=integration)

## HACS

1. **HACS** → **Integrations** → **Custom repositories**
2. Add `https://github.com/jinx-22/mempool_watch` (Category: **Integration**)
3. Install **Mempool Watch** → Restart Home Assistant
4. **Settings → Devices & services → Add Integration → Mempool Watch**


## Manual

Copy the `mempool_watch` folder to `/config/custom_components/`, restart Home Assistant, and then add the integration through the user interface.

---

# ⚙️ Configuration

**UI only — no YAML required.**

**Setup:** Instance URL, update interval (5–600 s, default 60 s), SSL certificate verification, optional CA certificate (PEM), and fiat currencies.

**Later in Options:** Settings, currencies, and Bitcoin addresses can be added or removed at any time.

<img width="80%" alt="Configuration" src="https://github.com/user-attachments/assets/2d721a9a-afa3-4a25-8465-e7c8e5cf1c7c" />

---

# 🐛 Issues & Feature Requests

Please provide the following information:

- Home Assistant version
- Mempool Watch version
- Relevant logs
- Steps to reproduce the issue

---

# 🧡 Support & Donations

## Lightning

<p align="center">
⚡ <b>Address:</b><br><br>
<code>usefulplay52@walletofsatoshi.com</code><br><br>
<img width="280" alt="Wallet of Satoshi" src="https://github.com/user-attachments/assets/65cc18d9-05d1-4a00-8ccc-9922fdb54baf" />
</p>

## Bitcoin

<div align="center">
<img src="https://github.com/user-attachments/assets/f74cad36-8c05-4a33-89cd-b998075af33b" /><br><br>
<code>bc1qkz7mtp23cmshxnru96lzgeayu0urlysvqk5vry</code><br><br>
<img width="220" alt="Bitcoin Donations" src="https://github.com/user-attachments/assets/196f68e4-b0e8-4f27-bded-8c4fe13b9d45" />
</div>

Thank you for your support — even a free ⭐ helps others discover the project:

[![stars](https://img.shields.io/github/stars/jinx-22/mempool_watch)](https://github.com/jinx-22/mempool_watch/stargazers)

---

# 📜 License

**Apache License 2.0** — see [LICENSE](LICENSE).

---

# ⚠️ Disclaimer

Independent open-source project. **Not** an official product of mempool.space, Home Assistant, or any other third party. Use at your own risk.
