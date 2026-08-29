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

🇬🇧 **English** · 🇩🇪 [Deutsch](README_DE.md)

**Current version: 0.5.9**

---

## 📖 About Mempool Watch

**Mempool Watch** is a custom Home Assistant integration for monitoring the Bitcoin network through your local Mempool instance (or [mempool.space](https://mempool.space/)).

> **Privacy:** Do not enter BTC addresses when using a public Mempool instance.

### Highlights

- **18 core sensors** + 14 optional sensors (fees, mempool, difficulty, hashrate, mining, price)
- **Multiple BTC price entities** (multi-select fiat currencies)
- **Unlimited Bitcoin addresses** (confirmed + pending)
- **SSL / custom CA certificate** (Umbrel, Start9, …)
- [btc-address-card](https://github.com/jinx-22/btc-address-card) Lovelace card included! No separate download or installation required!

---

# 📊 Sensors

### Core (enabled by default)

| Sensor | Description | Example |
| --- | --- | ---: |
| **Avg block fees (144 blocks)** | Average block fees (last 144 blocks) | 0.02134933 BTC |
| **Avg TX fee (144 blocks)** | Average transaction fee (last 144 blocks) | 496 sats |
| **Block height** | Current blockchain height | 964019 |
| **BTC price** | BTC price (USD) | 79,296 USD |
| **Difficulty adjustment estimate** | Estimated next difficulty adjustment | -0.79 % |
| **Difficulty adjustment progress** | Progress until the next retarget | 18.4 % |
| **Difficulty adjustment remaining blocks** | Blocks remaining until the next retarget | 1,645 blocks |
| **Economy fee** | Fee for low-priority transactions | 1 sat/vB |
| **Fastest fee** | Fee for the next block | 3 sat/vB |
| **Half hour fee** | Fee for confirmation in ~30 minutes | 3 sat/vB |
| **Hour fee** | Fee for confirmation in ~1 hour | 1 sat/vB |
| **Latest block miner** | Miner / pool of the latest block | ViaBTC |
| **Mempool size** | Current mempool size | 42,485,511 vB |
| **Mempool TX count** | Number of unconfirmed transactions | 84,930 |
| **Minimum fee** | Lowest fee in the mempool | 1 sat/vB |
| **Network difficulty** | Current network difficulty | 125,807,076,547,198 |
| **Network hashrate** | Estimated network hashrate | 872.60 EH/s |
| **Total miners reward (144 blocks)** | Total miner rewards (last 144 blocks) | 453.0743 BTC |

### Optional (disabled by default)

Enable them in the entity registry if required:

| Sensor | Description |
| --- | --- |
| **Mempool total fees** | Total fees currently in the mempool |
| **Difficulty adjustment remaining time** | Hours until the next retarget |
| **Previous difficulty retarget** | Previous difficulty adjustment (%) |
| **Next retarget height** | Block height of the next retarget |
| **Average block time** | Average block time (min.) |
| **Latest block TX count / size / weight** | Details of the latest block |
| **Latest block median fee / total fees / reward** | Fees & reward of the latest block |
| **Next block median fee / TX count** | Next projected mempool block |
| **Projected mempool blocks** | Number of projected blocks |

---

# 💱 BTC Price Currencies

USD is always available. You can select **one or more** additional fiat currencies during setup or in the options. Each selected currency creates its own BTC price sensor.

Supported (depending on the response from your Mempool instance at `/api/v1/prices`):  
`EUR` `GBP` `CAD` `CHF` `AUD` `JPY`

With API key:  
`CNY` `INR` `BRL` `KRW` `TRY` `PLN` `SEK` `NOK` `DKK` `CZK` `HUF` `ILS` `MXN` `SGD` `HKD` `NZD` `ZAR` `RUB` `THB` `TWD` `PHP` `IDR` `MYR` `VND`

---

# ₿ Bitcoin Addresses

Add as many addresses as you like. Each address creates its own entity with:

| Attribute | Description |
| --- | --- |
| `confirmed_balance` | Confirmed on-chain balance |
| `pending_incoming` | Unconfirmed incoming balance |
| `pending_outgoing` | Unconfirmed outgoing balance |
| `pending_change` | Net pending balance (incoming − outgoing) |
| `unconfirmed_count` | Number of unconfirmed transactions |
| `address` | Full Bitcoin address |

**Pending change:** positive = more incoming pending, negative = more outgoing pending.

---

# 🖼️ Lovelace BTC Address Card

Dedicated Lovelace card for BTC address sensors in the card picker:

INFO here:
**[btc-address-card](https://github.com/jinx-22/btc-address-card)**

## No separate installation is required because the card is already included in Mempool Watch!

<img width="485" height="310" alt="btc-address-card" src="https://github.com/user-attachments/assets/ff4caa01-b19b-418c-9c71-8f789c671f44" />

---

# 📦 Installation

## HACS (recommended)

1. **HACS** → **Integrations** → **Custom repositories**
2. Add `https://github.com/jinx-22/mempool_watch` (Category: **Integration**)
3. Install **Mempool Watch** → Restart Home Assistant
4. **Settings → Devices & services → Add Integration → Mempool Watch**

## Easy installation → [![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jinx-22&repository=mempool_watch&category=integration)

## Manual

Copy the `mempool_watch` folder to `/config/custom_components/`, restart Home Assistant, and add the integration through the UI.

---

# ⚙️ Configuration

UI only — no YAML.

**Setup:** Instance URL, update interval (5–600 s, default 60), SSL verification, optional CA certificate (PEM), and fiat currencies.

**Later in the options:** Settings, currencies, and addresses can be added or removed.

---

# 🐛 Issues & Feature Requests

Please include: Home Assistant version, Mempool Watch version, logs, and steps to reproduce the issue.

---

# 🧡 Support & Donations

## Lightning

<p align="center">
⚡ <b>Address:</b><br><br>
<code>usefulplay52@walletofsatoshi.com</code><br><br>
<img width="320" alt="Self_Wallet of Satoshi" src="https://github.com/user-attachments/assets/65cc18d9-05d1-4a00-8ccc-9922fdb54baf" />
</p>

## Bitcoin

<div align="center">
<img src="https://github.com/user-attachments/assets/f74cad36-8c05-4a33-89cd-b998075af33b" /><br><br>
<code>bc1qkz7mtp23cmshxnru96lzgeayu0urlysvqk5vry</code><br><br>
<img alt="Donations_240px" src="https://github.com/user-attachments/assets/196f68e4-b0e8-4f27-bded-8c4fe13b9d45" />
</div>

Thank you for your support — a free ⭐ helps others discover the project:  
[![GitHub stars](https://img.shields.io/github/stars/jinx-22/mempool_watch?style=social)](https://github.com/jinx-22/mempool_watch/stargazers)

---

# 📜 License

**Apache License 2.0** — see [LICENSE](LICENSE).

---

# ⚠️ Disclaimer

Independent open-source project. **Not** an official product of mempool.space, Home Assistant, or any third party. Use at your own risk.
