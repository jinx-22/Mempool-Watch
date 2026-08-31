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

🇬🇧 [**English**](README.md) · 🇩🇪 **Deutsch**

**Aktuelle Version: 0.5.9.2**

---

## 📖 Über Mempool Watch

**Mempool Watch** ist eine benutzerdefinierte Home-Assistant-Integration zur Überwachung des Bitcoin-Netzwerks über deine lokale Mempool-Instanz oder [mempool.space](https://mempool.space/).

> **Datenschutz:** Gib bei der Verwendung einer öffentlichen Mempool-Instanz keine BTC-Adressen ein.

### Highlights

- **18 Core-Sensoren** + 14 optionale Sensoren (Gebühren, Mempool, Difficulty, Hashrate, Mining, Preis)
- **Mehrere BTC-Preis-Entitäten** (Auswahl mehrerer Fiat-Währungen)
- **Unbegrenzte Bitcoin-Adressen** (bestätigt + ausstehend)
- **SSL / eigenes CA-Zertifikat** (Umbrel, Start9, …)
- [btc-address-card](https://github.com/jinx-22/btc-address-card) Lovelace Card enthalten! Keine separate Installation oder zusätzlicher Download erforderlich!

---

# 📊 Sensoren

### Core (standardmäßig aktiviert)

| Sensor | Beschreibung | Beispiel |
| --- | --- | ---: |
| **Durchschnittliche Blockgebühren (144 Blöcke)** | Durchschnittliche Blockgebühren der letzten 144 Blöcke | 0.02134933 BTC |
| **Durchschnittliche TX-Gebühr (144 Blöcke)** | Durchschnittliche Transaktionsgebühr der letzten 144 Blöcke | 496 sats |
| **Blockhöhe** | Aktuelle Höhe der Blockchain | 964019 |
| **BTC-Preis** | BTC-Preis (USD) | 79,296 USD |
| **Difficulty-Anpassungsschätzung** | Geschätzte nächste Difficulty-Anpassung | -0.79 % |
| **Difficulty-Anpassungsfortschritt** | Fortschritt bis zum nächsten Retarget | 18.4 % |
| **Verbleibende Blöcke bis zur Difficulty-Anpassung** | Verbleibende Blöcke bis zum nächsten Retarget | 1.645 Blöcke |
| **Economy-Gebühr** | Gebühr für Transaktionen mit niedriger Priorität | 1 sat/vB |
| **Schnellste Gebühr** | Gebühr für den nächsten Block | 3 sat/vB |
| **Halbe-Stunde-Gebühr** | Gebühr für eine Bestätigung in ca. 30 Minuten | 3 sat/vB |
| **Stunden-Gebühr** | Gebühr für eine Bestätigung in ca. 1 Stunde | 1 sat/vB |
| **Miner des letzten Blocks** | Miner / Pool des letzten Blocks | ViaBTC |
| **Mempool-Größe** | Aktuelle Größe des Mempools | 42,485,511 vB |
| **Mempool TX-Anzahl** | Anzahl unbestätigter Transaktionen | 84,930 |
| **Mindestgebühr** | Niedrigste Gebühr im Mempool | 1 sat/vB |
| **Netzwerk-Difficulty** | Aktuelle Netzwerk-Difficulty | 125,807,076,547,198 |
| **Netzwerk-Hashrate** | Geschätzte Netzwerk-Hashrate | 872.60 EH/s |
| **Gesamte Miner-Belohnung (144 Blöcke)** | Gesamte Miner-Belohnungen der letzten 144 Blöcke | 453.0743 BTC |

<img width="263" height="798" alt="Sensoren" src="https://github.com/user-attachments/assets/e958a33c-0d03-4ba6-8474-54c570547850" />

### Optional (standardmäßig deaktiviert)

Bei Bedarf in der Entity Registry aktivieren:

| Sensor | Beschreibung |
| --- | --- |
| **Mempool-Gesamtgebühren** | Gesamte aktuell im Mempool befindliche Gebühren |
| **Verbleibende Zeit bis zur Difficulty-Anpassung** | Stunden bis zum nächsten Retarget |
| **Vorheriges Difficulty-Retarget** | Vorherige Difficulty-Anpassung (%) |
| **Höhe des nächsten Retargets** | Blockhöhe des nächsten Retargets |
| **Durchschnittliche Blockzeit** | Durchschnittliche Blockzeit (Min.) |
| **TX-Anzahl / Größe / Gewicht des letzten Blocks** | Details zum letzten Block |
| **Median-Gebühr / Gesamtgebühren / Belohnung des letzten Blocks** | Gebühren und Belohnung des letzten Blocks |
| **Median-Gebühr / TX-Anzahl des nächsten Blocks** | Prognostizierter nächster Mempool-Block |
| **Prognostizierte Mempool-Blöcke** | Anzahl der prognostizierten Blöcke |

---

# 💱 BTC-Preiswährungen

USD ist immer verfügbar. Während der Einrichtung oder in den Optionen können **eine oder mehrere zusätzliche Fiat-Währungen** ausgewählt werden. Für jede ausgewählte Währung wird eine eigene BTC-Preis-Entität erstellt.

Unterstützt (abhängig von der Antwort deiner Mempool-Instanz auf `/api/v1/prices`):

`EUR` `GBP` `CAD` `CHF` `AUD` `JPY`

Mit API-Key:

`CNY` `INR` `BRL` `KRW` `TRY` `PLN` `SEK` `NOK` `DKK` `CZK` `HUF` `ILS` `MXN` `SGD` `HKD` `NZD` `ZAR` `RUB` `THB` `TWD` `PHP` `IDR` `MYR` `VND`

> **Hinweis:** Für zusätzliche Fiat-Währungen wird ein API-Key benötigt. Dieser muss in deiner Mempool-Instanz unter `FIAT_PRICE → API_KEY` hinterlegt werden.

<img width="893" height="606" alt="Währungen" src="https://github.com/user-attachments/assets/0f9acf0e-ef61-480c-b25b-17bd104c2785" />

---

# ₿ Bitcoin-Adressen

Füge beliebig viele Bitcoin-Adressen hinzu. Jede Adresse erstellt eine eigene Entität mit:

| Attribut | Beschreibung |
| --- | --- |
| `confirmed_balance` | Bestätigter On-Chain-Saldo |
| `pending_incoming` | Unbestätigter eingehender Saldo |
| `pending_outgoing` | Unbestätigter ausgehender Saldo |
| `pending_change` | Nettoänderung des ausstehenden Saldos (eingehend − ausgehend) |
| `unconfirmed_count` | Anzahl unbestätigter Transaktionen |
| `address` | Vollständige Bitcoin-Adresse |

**Pending Change:** Positiv = mehr eingehende ausstehende BTC, negativ = mehr ausgehende ausstehende BTC.

---

# 🖼️ Lovelace BTC Address Card

Dedizierte Lovelace Card für BTC-Adresssensoren, verfügbar im Card Picker:

INFO hier:
**[btc-address-card](https://github.com/jinx-22/btc-address-card)**

## Keine separate Installation erforderlich, da die Card bereits in Mempool Watch enthalten ist!

<img width="1146" height="656" alt="BTC Address Card" src="https://github.com/user-attachments/assets/29846f5d-aa18-420e-b41b-534fd14aac06" />
<img width="1037" height="746" alt="BTC Address Card Konfiguration" src="https://github.com/user-attachments/assets/6a506418-7be7-457f-8bca-f5a6dafb28c3" />

---

# 📦 Installation

## HACS (empfohlen)

1. **HACS** → **Integrationen** → **Benutzerdefinierte Repositories**
2. `https://github.com/jinx-22/mempool_watch` hinzufügen (Kategorie: **Integration**)
3. **Mempool Watch** installieren → Home Assistant neu starten
4. **Einstellungen → Geräte & Dienste → Integration hinzufügen → Mempool Watch**

## Einfache Installation → [![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jinx-22&repository=mempool_watch&category=integration)

## Manuell

Den Ordner `mempool_watch` nach `/config/custom_components/` kopieren, Home Assistant neu starten und die Integration anschließend über die Benutzeroberfläche hinzufügen.

---

# ⚙️ Konfiguration

**Nur über die Benutzeroberfläche — kein YAML erforderlich.**

**Einrichtung:** Instanz-URL, Aktualisierungsintervall (5–600 s, Standard 60 s), SSL-Zertifikatsprüfung, optionales CA-Zertifikat (PEM) und Fiat-Währungen.

**Später in den Optionen:** Einstellungen, Währungen und Bitcoin-Adressen können jederzeit hinzugefügt oder entfernt werden.

<img width="897" height="543" alt="Konfiguration" src="https://github.com/user-attachments/assets/2d721a9a-afa3-4a25-8465-e7c8e5cf1c7c" />

---

# 🐛 Fehler & Feature Requests

Bitte gib folgende Informationen an:

- Home-Assistant-Version
- Mempool-Watch-Version
- relevante Logs
- Schritte zur Reproduktion des Problems

---

# 🧡 Support & Spenden

## Lightning

<p align="center">
⚡ <b>Adresse:</b><br><br>
<code>usefulplay52@walletofsatoshi.com</code><br><br>
<img width="320" alt="Wallet of Satoshi" src="https://github.com/user-attachments/assets/65cc18d9-05d1-4a00-8ccc-9922fdb54baf" />
</p>

## Bitcoin

<div align="center">
<img src="https://github.com/user-attachments/assets/f74cad36-8c05-4a33-89cd-b998075af33b" /><br><br>
<code>bc1qkz7mtp23cmshxnru96lzgeayu0urlysvqk5vry</code><br><br>
<img alt="Bitcoin-Spenden" src="https://github.com/user-attachments/assets/196f68e4-b0e8-4f27-bded-8c4fe13b9d45" />
</div>

Vielen Dank für deine Unterstützung — ein kostenloser ⭐ hilft anderen, das Projekt zu entdecken:

[![stars](https://img.shields.io/github/stars/jinx-22/mempool_watch)](https://github.com/jinx-22/mempool_watch/stargazers)

---

# 📜 Lizenz

**Apache License 2.0** — siehe [LICENSE](LICENSE).

---

# ⚠️ Haftungsausschluss

Unabhängiges Open-Source-Projekt. **Kein** offizielles Produkt von mempool.space, Home Assistant oder einem anderen Drittanbieter. Nutzung auf eigene Verantwortung.
