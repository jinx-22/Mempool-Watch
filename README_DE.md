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

🇬🇧 **[English Description](README.md)**

---

## 📖 Über Mempool Watch

**Mempool Watch** ist eine benutzerdefinierte Home-Assistant-Integration zur Überwachung des Bitcoin-Netzwerks mit Daten von deinem lokalen gehosteten Mempool!

Der öffentlich zugängliche [mempool.space](https://mempool.space/) ist auch möglich! Beachte aber, dass hier bei eingabe von BTC-Addressen deine Privatsphäre gefährdet ist!!! 

Die Integration stellt detaillierte Bitcoin-Netzwerkinformationen direkt als native Home-Assistant-Entitäten bereit.

Mempool Watch stellt aktuell **18+1 Bitcoin-Netzwerk-Sensoren** zur Verfügung und überwacht unter anderem Blockchain-Statistiken, Transaktionsgebühren, Mempool-Aktivität, Mining-Informationen, Netzwerk-Difficulty, Netzwerk-Hashrate, Difficulty-Anpassungen und den Bitcoin-Preis.

Zusätzlich unterstützt Mempool Watch:

- Eine optionale zweite BTC-Preis-Entität
- Eine unbegrenzte Anzahl an Bitcoin-Adressen
- Bestätigte und unbestätigte Informationen zu Bitcoin-Adressen
- Die optionale `btc-address-card.js` Lovelace Card

---

# 🚀 Funktionen/Sensoren

### ₿ Bitcoin-Netzwerk

Wichtige Kennzahlen des Bitcoin-Netzwerks direkt in Home Assistant überwachen:

- Aktuelle Blockhöhe
- Netzwerk-Difficulty
- Netzwerk-Hashrate
- Geschätzte Difficulty-Anpassung
- Fortschritt der Difficulty-Anpassung
- Verbleibende Blöcke bis zur nächsten Difficulty-Anpassung
- Miner des letzten Blocks
- Durchschnittliche Blockgebühren
- Durchschnittliche Transaktionsgebühren
- Gesamte Miner-Rewards

### 📊 Mempool

Den aktuellen Bitcoin-Mempool überwachen:

- Mempool-Größe
- Anzahl der Mempool-Transaktionen
- Minimale Fee
- Economy Fee
- Hour Fee
- Half-Hour Fee
- Fastest Fee

### 💱 Bitcoin-Preis

Mempool Watch stellt den aktuellen BTC-Preis bereit und kann optional eine zweite BTC-Preis-Entität in einer anderen Währung erstellen.

### ₿ Bitcoin-Adressen

Eine **unbegrenzte Anzahl von Bitcoin-Adressen** als eigene Home-Assistant-Entitäten überwachen:

- Bestätigtes Guthaben
- Unbestätigte Eingänge
- Unbestätigte Ausgänge
- Netto-Pending-Betrag
- Anzahl unbestätigter Transaktionen
- Vollständige Bitcoin-Adresse

---

# 📊 Sensoren

Mempool Watch stellt folgende **18 Bitcoin-Netzwerk-Sensoren** bereit:

| Sensor | Beschreibung | Beispiel |
|---|---|---:|
| **Avg block fees (144 blocks)** | Durchschnittliche Blockgebühren der letzten 144 Blöcke | 0,02134933 BTC |
| **Avg TX fee (144 blocks)** | Durchschnittliche Transaktionsgebühr der letzten 144 Blöcke | 496 sats |
| **Block height** | Aktuelle Höhe der Bitcoin-Blockchain | 964019 |
| **BTC price** | Aktueller Bitcoin-Preis | 79.296 USD |
| **Difficulty adjustment estimate** | Geschätzte Änderung bei der nächsten Difficulty-Anpassung | -0,79 % |
| **Difficulty adjustment progress** | Fortschritt bis zur nächsten Difficulty-Anpassung | 18,4 % |
| **Difficulty adjustment remaining blocks** | Verbleibende Blöcke bis zur nächsten Difficulty-Anpassung | 1.645 Blöcke |
| **Economy fee** | Empfohlene Fee für niedrige Priorität | 1 sat/vB |
| **Fastest fee** | Empfohlene Fee für die schnellstmögliche Bestätigung | 3 sat/vB |
| **Half hour fee** | Empfohlene Fee für eine Bestätigung innerhalb von ca. 30 Minuten | 3 sat/vB |
| **Hour fee** | Empfohlene Fee für eine Bestätigung innerhalb von ca. 1 Stunde | 1 sat/vB |
| **Latest block miner** | Miner bzw. Mining-Pool des zuletzt gefundenen Blocks | ViaBTC |
| **Mempool size** | Aktuelle Größe des Bitcoin-Mempools | 42.485.511 vB |
| **Mempool TX count** | Anzahl der unbestätigten Transaktionen | 84.930 |
| **Minimum fee** | Aktuell niedrigste im Mempool vertretene Fee | 1 sat/vB |
| **Network difficulty** | Aktuelle Bitcoin-Netzwerk-Difficulty | 125.807.076.547.198 |
| **Network hashrate** | Geschätzte Hashrate des Bitcoin-Netzwerks | 872,60 EH/s |
| **Total miners reward (144 blocks)** | Gesamte Miner-Rewards der letzten 144 Blöcke | 453,0743 BTC |
---

# 💱 Zusätzliche BTC-Preis-Entität

Optional kann eine **zweite BTC-Preis-Entität** konfiguriert werden.

Damit kann Bitcoin gleichzeitig in zwei verschiedenen Währungen überwacht werden.

Zum Beispiel:

**BTC/USD + BTC/EUR**

Wenn keine zweite Preis-Entität benötigt wird, kann **Keine** ausgewählt werden.

### Unterstützte Währungen

| Code | Währung |
|---|---|
| `none` | Keine |
| `EUR` | Euro |
| `GBP` | Britisches Pfund |
| `CAD` | Kanadischer Dollar |
| `CHF` | Schweizer Franken |
| `AUD` | Australischer Dollar |
| `JPY` | Japanischer Yen |
| `CNY` | Chinesischer Yuan |
| `INR` | Indische Rupie |
| `BRL` | Brasilianischer Real |
| `KRW` | Südkoreanischer Won |
| `TRY` | Türkische Lira |
| `PLN` | Polnischer Złoty |
| `SEK` | Schwedische Krone |
| `NOK` | Norwegische Krone |
| `DKK` | Dänische Krone |
| `CZK` | Tschechische Krone |
| `HUF` | Ungarischer Forint |
| `ILS` | Israelischer Neuer Schekel |
| `MXN` | Mexikanischer Peso |
| `SGD` | Singapur-Dollar |
| `HKD` | Hongkong-Dollar |
| `NZD` | Neuseeland-Dollar |
| `ZAR` | Südafrikanischer Rand |
| `RUB` | Russischer Rubel |
| `THB` | Thailändischer Baht |
| `TWD` | Neuer Taiwan-Dollar |
| `PHP` | Philippinischer Peso |
| `IDR` | Indonesische Rupiah |
| `MYR` | Malaysischer Ringgit |
| `VND` | Vietnamesischer Đồng |

---

# ₿ Bitcoin-Adressen überwachen

Mempool Watch kann einzelne Bitcoin-Adressen direkt in Home Assistant überwachen.

Es gibt **keine feste Begrenzung für die Anzahl der Bitcoin-Adressen**, die hinzugefügt werden können.

Jede Bitcoin-Adresse wird als eigene Home-Assistant-Entität angelegt.

### Verfügbare Attribute

| Attribut | Beschreibung |
|---|---|
| `chain_stats` | Bestätigtes On-Chain-Guthaben |
| `pending_incoming` | Unbestätigter eingehender Betrag |
| `pending_outgoing` | Unbestätigter ausgehender Betrag |
| `pending_change` | Netto-Pending-Betrag: Eingang − Ausgang |
| `unconfirmed_count` | Anzahl unbestätigter Transaktionen |
| `confirmed_balance` | Bestätigtes Guthaben |
| `address` | Vollständige Bitcoin-Adresse |

### Pending Change

Das Attribut `pending_change` stellt den aktuellen unbestätigten Nettobetrag dar:

**Eingang − Ausgang**

Ein positiver Wert bedeutet, dass aktuell mehr Bitcoin unbestätigt eingehen.

Ein negativer Wert bedeutet, dass aktuell mehr Bitcoin unbestätigt ausgehen.

Damit lässt sich neben dem bestätigten Guthaben auch die aktuelle **unbestätigte Aktivität** einer Bitcoin-Adresse überwachen.

---

# 🖼️ Optionale Bitcoin Address Card

Als zusätzliche Lovelace-Karte kann eine eigene Bitcoin Address Card verwendet werden.

### `btc-address-card.js`

Die Card kann unter anderem anzeigen:

- Bestätigtes Guthaben
- Unbestätigte Eingänge
- Unbestätigte Ausgänge
- Pending Change
- Anzahl unbestätigter Transaktionen
- Bitcoin-Adresse

<img width="485" height="310" alt="btc-address-card" src="https://github.com/user-attachments/assets/ff4caa01-b19b-418c-9c71-8f789c671f44" />


Die Card ist **vollständig optional** und für die Mempool-Watch-Integration nicht erforderlich.

### Repository

[btc-address-card.js Repository](https://github.com/jinx-22/btc-address-card)

---

# 📦 Installation

## HACS (kommt -> dauert ca. 2 Wochen)

Die empfohlene Installationsmethode ist **HACS**.
(ist in Arbeit, muss noch hinzugefügt werden, kann 2 Wochen dauern!)

1. **HACS** öffnen
2. **Integrationen** auswählen
3. Nach **Mempool Watch** suchen
4. Integration installieren
5. Home Assistant neu starten
6. **Einstellungen → Geräte & Dienste** öffnen
7. **Integration hinzufügen** auswählen
8. Nach **Mempool Watch** suchen
9. Konfiguration abschließen

### Direkter HACS-Link

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jinx-22&repository=mempool_watch&category=integration)

---

## Manuelle Installation

Die aktuelle Version herunterladen und den Ordner `mempool_watch` nach:

`/config/custom_components/`

kopieren.

Nach dem Kopieren der Dateien Home Assistant neu starten.

Anschließend:

**Einstellungen → Geräte & Dienste → Integration hinzufügen**

und nach:

**Mempool Watch**

suchen.

---

# ⚙️ Konfiguration

Mempool Watch wird vollständig über die Home-Assistant-Oberfläche konfiguriert.

Eine YAML-Konfiguration ist nicht erforderlich.

Nach der Installation:

**Einstellungen → Geräte & Dienste → Integration hinzufügen → Mempool Watch**

Die Integration ermöglicht die Konfiguration der verfügbaren Optionen sowie optional die Auswahl einer zweiten BTC-Preiswährung und das Hinzufügen von Bitcoin-Adressen.

---


# 🌐 Datenquelle

Mempool Watch verwendet Daten von von der eingegebenen/verbundenen Mempool-Instanz
Die Bitcoin-Netzwerkdaten werden von der Integration in native Home-Assistant-Entitäten umgewandelt.

Diese Entitäten können unter anderem verwendet werden für:

- Dashboards
- Automationen
- Scripts
- Templates
- Benachrichtigungen
- Statistiken
- Mining-Dashboards

---

# 🐛 Fehler & Feature Requests

Wenn du einen Fehler findest, erstelle bitte ein Issue in diesem Repository.

Bei einem Fehler bitte möglichst folgende Informationen angeben:

- Home-Assistant-Version
- Mempool-Watch-Version
- Relevante Log-Ausgaben
- Schritte zur Reproduktion
- Screenshots, sofern hilfreich

---

# 🧡 Support & Spenden

Wenn dir dieses Projekt gefällt und du es nützlich findest, freue ich mich sehr über eine kleine Spende.

Jede Unterstützung hilft bei der weiteren Entwicklung 🚀

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

Vielen Dank für deine Unterstützung!

Und gib dem Projekt gerne einen kostenlosen ⭐ auf GitHub, damit auch andere Nutzer das Projekt entdecken können.



---

# 📜 Lizenz

Dieses Projekt steht unter der **Apache License 2.0**.

Den vollständigen Lizenztext findest du unter [LICENSE](LICENSE).

---

# ⚠️ Haftungsausschluss

Mempool Watch ist ein unabhängiges Open-Source-Projekt.

Es handelt sich **nicht um ein offizielles Produkt von mempool.space, Home Assistant oder einer anderen Drittanbieter-Organisation**.

Die Integration verwendet Daten, die von externen Bitcoin-Diensten bereitgestellt werden.

Die Nutzung erfolgt auf eigene Verantwortung.
