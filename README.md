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

**Current version: 0.5.0**

---

## 📖 About

**Mempool Watch** is a custom Home Assistant integration for monitoring the Bitcoin network via your local Mempool instance (or [mempool.space](https://mempool.space/)).

> **Privacy:** Do not enter BTC addresses when using a public Mempool instance.

### Highlights

- **18 core sensors** + 14 optional sensors (fees, mempool, difficulty, hashrate, mining, price)
- **Multiple BTC price entities** (multi-select fiat currencies)
- **Unlimited Bitcoin address** monitoring (confirmed + pending)
- **SSL / custom CA** support (Umbrel, Start9, …)
- Optional [btc-address-card](https://github.com/jinx-22/btc-address-card) Lovelace card

---

# 📊 Sensors

### Core (enabled by default)

| Sensor | Description | Example |
| --- | --- | ---: |
| **Avg block fees (144 blocks)** | Average block fees (last 144 blocks) | 0.02134933 BTC |
| **Avg TX fee (144 blocks)** | Average TX fee (last 144 blocks) | 496 sats |
| **Block height** | Current blockchain height | 964019 |
| **BTC price** | BTC price (USD) | 79,296 USD |
| **Difficulty adjustment estimate** | Estimated next difficulty change | -0.79 % |
| **Difficulty adjustment progress** | Progress to next retarget | 18.4 % |
| **Difficulty adjustment remaining blocks** | Blocks until next retarget | 1,645 blocks |
| **Economy fee** | Low-priority fee rate | 1 sat/vB |
| **Fastest fee** | Next-block fee rate | 3 sat/vB |
| **Half hour fee** | ~30 min confirmation fee | 3 sat/vB |
| **Hour fee** | ~1 h confirmation fee | 1 sat/vB |
| **Latest block miner** | Miner / pool of latest block | ViaBTC |
| **Mempool size** | Current mempool size | 42,485,511 vB |
| **Mempool TX count** | Unconfirmed transactions | 84,930 |
| **Minimum fee** | Lowest fee in mempool | 1 sat/vB |
| **Network difficulty** | Current network difficulty | 125,807,076,547,198 |
| **Network hashrate** | Estimated network hashrate | 872.60 EH/s |
| **Total miners reward (144 blocks)** | Total miner rewards (last 144 blocks) | 453.0743 BTC |

### Optional (disabled by default)

Enable in the entity registry if needed:

| Sensor | Description |
| --- | --- |
| **Mempool total fees** | Total fees in the mempool |
| **Difficulty adjustment remaining time** | Hours until next retarget |
| **Previous difficulty retarget** | Previous adjustment (%) |
| **Next retarget height** | Block height of next retarget |
| **Average block time** | Average block time (min) |
| **Latest block TX count / size / weight** | Latest block details |
| **Latest block median fee / total fees / reward** | Latest block fee & reward stats |
| **Next block median fee / TX count** | Next projected mempool block |
| **Projected mempool blocks** | Number of projected blocks |

---

# 💱 BTC Price Currencies

USD is always available. You can select **one or more** additional fiat currencies (setup or options). Each selection creates its own price sensor.

Supported (depending on your Mempool `/api/v1/prices` response):  
`EUR` `GBP` `CAD` `CHF` `AUD` `JPY` 

with api.key
`CNY` `INR` `BRL` `KRW` `TRY` `PLN` `SEK` `NOK` `DKK` `CZK` `HUF` `ILS` `MXN` `SGD` `HKD` `NZD` `ZAR` `RUB` `THB` `TWD` `PHP` `IDR` `MYR` `VND`

---

# ₿ Bitcoin Addresses

Add any number of addresses. Each becomes its own entity with:

| Attribute | Description |
| --- | --- |
| `confirmed_balance` | Confirmed on-chain balance |
| `pending_incoming` | Unconfirmed incoming |
| `pending_outgoing` | Unconfirmed outgoing |
| `pending_change` | Net pending (incoming − outgoing) |
| `unconfirmed_count` | Unconfirmed TX count |
| `address` | Full address |

**Pending change:** positive = more incoming pending, negative = more outgoing pending.

---

# 🖼️ Optional Address Card

Dedicated Lovelace card for address sensors:  
**[btc-address-card](https://github.com/jinx-22/btc-address-card)**

<img width="485" height="310" alt="btc-address-card" src="https://github.com/user-attachments/assets/ff4caa01-b19b-418c-9c71-8f789c671f44" />

Completely optional — not required for the integration.

---

# 📦 Installation

## HACS (recommended)

1. **HACS** → **Integrations** → **Custom repositories**
2. Add `https://github.com/jinx-22/mempool_watch` (category: **Integration**)
3. Install **Mempool Watch** → restart Home Assistant
4. **Settings → Devices & services → Add Integration → Mempool Watch**
---

## Easy installation -> [![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jinx-22&repository=mempool_watch&category=integration)

## Manual

Copy `mempool_watch` to `/config/custom_components/`, restart, then add the integration via the UI.

---

# ⚙️ Configuration

UI only — no YAML.

**Setup:** instance URL, update interval (5–600 s, default 60), SSL verification, optional CA certificate (PEM), fiat currencies.

**Options later:** settings, currencies, add/remove addresses.

---

# 🐛 Bugs & Feature Requests

Please include: Home Assistant version, Mempool Watch version, logs, steps to reproduce.

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

Thanks for your support — and a free ⭐ helps others find the project:  
[![GitHub stars](https://img.shields.io/github/stars/jinx-22/mempool_watch?style=social)](https://github.com/jinx-22/mempool_watch/stargazers)

---

# 📜 License

**Apache License 2.0** — see [LICENSE](LICENSE).

---

# ⚠️ Disclaimer

Independent open-source project. **Not** an official product of mempool.space, Home Assistant, or any third party. Use at your own risk.
