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

🇬🇧 [English](README.md) · 🇩🇪 **Deutsch**

**Aktuelle Version: 0.5.9**

---

## 📖 Über Mempool Watch

**Mempool Watch** ist eine benutzerdefinierte Home-Assistant-Integration zur Überwachung des Bitcoin-Netzwerks über deine lokale Mempool-Instanz (oder [mempool.space](https://mempool.space/)).

> **Privatsphäre:** Bei einer öffentlichen Mempool-Instanz keine BTC-Adressen eingeben.

### Highlights

- **18 Core-Sensoren** + 14 optionale Sensoren (Fees, Mempool, Difficulty, Hashrate, Mining, Preis)
- **Mehrere BTC-Preis-Entitäten** (Mehrfachauswahl Fiat-Währungen)
- **Unbegrenzte Bitcoin-Adressen** (bestätigt + pending)
- **SSL / eigenes CA-Zertifikat** (Umbrel, Start9, …)
- [btc-address-card](https://github.com/jinx-22/btc-address-card) Lovelace-Card inklusive! Kein extra Download/Installation nötig!

---

# 📊 Sensoren

### Core (standardmäßig aktiv)

| Sensor | Beschreibung | Beispiel |
| --- | --- | ---: |
| **Avg block fees (144 blocks)** | Durchschnittliche Blockgebühren (letzte 144 Blöcke) | 0,02134933 BTC |
| **Avg TX fee (144 blocks)** | Durchschnittliche TX-Gebühr (letzte 144 Blöcke) | 496 sats |
| **Block height** | Aktuelle Blockchain-Höhe | 964019 |
| **BTC price** | BTC-Preis (USD) | 79.296 USD |
| **Difficulty adjustment estimate** | Geschätzte nächste Difficulty-Änderung | -0,79 % |
| **Difficulty adjustment progress** | Fortschritt bis zum nächsten Retarget | 18,4 % |
| **Difficulty adjustment remaining blocks** | Blöcke bis zum nächsten Retarget | 1.645 Blöcke |
| **Economy fee** | Fee für niedrige Priorität | 1 sat/vB |
| **Fastest fee** | Fee für nächsten Block | 3 sat/vB |
| **Half hour fee** | Fee für ~30 Min. Bestätigung | 3 sat/vB |
| **Hour fee** | Fee für ~1 Std. Bestätigung | 1 sat/vB |
| **Latest block miner** | Miner / Pool des letzten Blocks | ViaBTC |
| **Mempool size** | Aktuelle Mempool-Größe | 42.485.511 vB |
| **Mempool TX count** | Unbestätigte Transaktionen | 84.930 |
| **Minimum fee** | Niedrigste Fee im Mempool | 1 sat/vB |
| **Network difficulty** | Aktuelle Netzwerk-Difficulty | 125.807.076.547.198 |
| **Network hashrate** | Geschätzte Netzwerk-Hashrate | 872,60 EH/s |
| **Total miners reward (144 blocks)** | Gesamte Miner-Rewards (letzte 144 Blöcke) | 453,0743 BTC |

### Optional (standardmäßig deaktiviert)

Bei Bedarf in der Entitätsregistrierung aktivieren:

| Sensor | Beschreibung |
| --- | --- |
| **Mempool total fees** | Gesamte Fees im Mempool |
| **Difficulty adjustment remaining time** | Stunden bis zum nächsten Retarget |
| **Previous difficulty retarget** | Vorherige Anpassung (%) |
| **Next retarget height** | Blockhöhe des nächsten Retargets |
| **Average block time** | Durchschnittliche Blockzeit (Min.) |
| **Latest block TX count / size / weight** | Details zum letzten Block |
| **Latest block median fee / total fees / reward** | Fees & Reward des letzten Blocks |
| **Next block median fee / TX count** | Nächster projizierter Mempool-Block |
| **Projected mempool blocks** | Anzahl projizierter Blöcke |

---

# 💱 BTC-Preis-Währungen

USD ist immer verfügbar. Du kannst **eine oder mehrere** weitere Fiat-Währungen wählen (Setup oder Optionen). Jede Auswahl erzeugt einen eigenen Preissensor.

Unterstützt (abhängig von der Antwort deiner Mempool-Instanz unter `/api/v1/prices`):  
`EUR` `GBP` `CAD` `CHF` `AUD` `JPY`

mit API-Key:  
`CNY` `INR` `BRL` `KRW` `TRY` `PLN` `SEK` `NOK` `DKK` `CZK` `HUF` `ILS` `MXN` `SGD` `HKD` `NZD` `ZAR` `RUB` `THB` `TWD` `PHP` `IDR` `MYR` `VND`

---

# ₿ Bitcoin-Adressen

Beliebig viele Adressen hinzufügen. Jede wird zur eigenen Entität mit:

| Attribut | Beschreibung |
| --- | --- |
| `confirmed_balance` | Bestätigtes On-Chain-Guthaben |
| `pending_incoming` | Unbestätigter Eingang |
| `pending_outgoing` | Unbestätigter Ausgang |
| `pending_change` | Netto-Pending (Eingang − Ausgang) |
| `unconfirmed_count` | Anzahl unbestätigter TXs |
| `address` | Vollständige Adresse |

**Pending change:** positiv = mehr eingehend pending, negativ = mehr ausgehend pending.

---

# 🖼️ Lovelace BTC Address Card

Lovelace-Card für BTC-Address-Sensoren in der Kartenauswahl:

INFO hier:
**[btc-address-card](https://github.com/jinx-22/btc-address-card)**

## Karte muss nicht extra installiert werden da schon in Mempool Watch enthalten!

<img width="485" height="310" alt="btc-address-card" src="https://github.com/user-attachments/assets/ff4caa01-b19b-418c-9c71-8f789c671f44" />

---

# 📦 Installation

## HACS (empfohlen)

1. **HACS** → **Integrationen** → **Benutzerdefinierte Repositories**
2. `https://github.com/jinx-22/mempool_watch` hinzufügen (Kategorie: **Integration**)
3. **Mempool Watch** installieren → Home Assistant neu starten
4. **Einstellungen → Geräte & Dienste → Integration hinzufügen → Mempool Watch**

## Einfache Installation → [![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jinx-22&repository=mempool_watch&category=integration)

## Manuell

Ordner `mempool_watch` nach `/config/custom_components/` kopieren, neu starten, Integration über die UI hinzufügen.

---

# ⚙️ Konfiguration

Nur über die UI — kein YAML.

**Setup:** Instanz-URL, Update-Intervall (5–600 s, Standard 60), SSL-Prüfung, optional CA-Zertifikat (PEM), Fiat-Währungen.

**Später in den Optionen:** Einstellungen, Währungen, Adressen hinzufügen/entfernen.

---

# 🐛 Fehler & Feature Requests

Bitte angeben: Home-Assistant-Version, Mempool-Watch-Version, Logs, Schritte zur Reproduktion.

---

# 🧡 Support & Spenden

## Lightning

<p align="center">
⚡ <b>Adresse:</b><br><br>
<code>usefulplay52@walletofsatoshi.com</code><br><br>
<img width="320" alt="Self_Wallet of Satoshi" src="https://github.com/user-attachments/assets/65cc18d9-05d1-4a00-8ccc-9922fdb54baf" />
</p>

## Bitcoin

<div align="center">
<img src="https://github.com/user-attachments/assets/f74cad36-8c05-4a33-89cd-b998075af33b" /><br><br>
<code>bc1qkz7mtp23cmshxnru96lzgeayu0urlysvqk5vry</code><br><br>
<img alt="Donations_240px" src="https://github.com/user-attachments/assets/196f68e4-b0e8-4f27-bded-8c4fe13b9d45" />
</div>

Danke für deine Unterstützung — ein kostenloses ⭐ hilft anderen, das Projekt zu finden:  
[![GitHub stars](https://img.shields.io/github/stars/jinx-22/mempool_watch?style=social)](https://github.com/jinx-22/mempool_watch/stargazers)

---

# 📜 Lizenz

**Apache License 2.0** — siehe [LICENSE](LICENSE).

---

# ⚠️ Haftungsausschluss

Unabhängiges Open-Source-Projekt. **Kein** offizielles Produkt von mempool.space, Home Assistant oder Drittanbietern. Nutzung auf eigene Verantwortung.
