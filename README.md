# WordPress Blog Analytics Dashboard

Ein Python-basiertes CLI-Tool zur Analyse von WordPress-Blogs über die REST API. Erstellt detaillierte Statistiken über Blogposts, Wortfrequenzen und Schreibgewohnheiten.

## Features

- 📊 **Umfassende Post-Analyse**: Wortanzahl, Lesezeit, Veröffentlichungsdaten
- 🔤 **Wortfrequenz-Analyse**: Identifiziert die häufigsten Begriffe in deinen Posts
- 📈 **Multiple Output-Formate**: Terminal, HTML-Dashboard, JSON-Export
- 🚀 **Einfache Bedienung**: Direkt über die Kommandozeile
- 🔌 **REST API Integration**: Nutzt die standardmäßige WordPress REST API

## Installation

```bash
# Repository klonen
git clone https://github.com/sozialwelten/WordPress-Blog-Analytics-Dashboard.git
cd WordPress-Blog-Analytics-Dashboard

# Dependencies installieren
pip install -r requirements.txt

# Script ausführbar machen (Linux/macOS)
chmod +x WordPressBlogAnalyticsDashboard.py
```

## Voraussetzungen

- Python 3.7+
- WordPress-Blog mit aktivierter REST API (standardmäßig aktiviert)
- `requests` Library

## Verwendung

### Basis-Analyse (Terminal-Output)

```bash
./WordPressBlogAnalyticsDashboard.py https://deinblog.de
```

### HTML-Dashboard generieren

```bash
./WordPressBlogAnalyticsDashboard.py https://deinblog.de --format html
```

Erstellt eine interaktive HTML-Datei mit Visualisierungen.

### JSON-Export

```bash
./WordPressBlogAnalyticsDashboard.py https://deinblog.de --format json
```

Exportiert strukturierte Daten für weitere Verarbeitung.

### Hilfe anzeigen

```bash
./WordPressBlogAnalyticsDashboard.py --help
```

## Ausgabebeispiel (Terminal)

```
======================================================================
📊 WORDPRESS BLOG ANALYTICS DASHBOARD
======================================================================

📈 ÜBERSICHT
----------------------------------------------------------------------
Anzahl Posts:        3
Gesamt Wörter:       2,847
Durchschn. Wörter:   949 pro Post
Durchschn. Lesezeit: 4.7 Minuten
Zeitraum:            15.03.2024 - 28.10.2024

📝 POSTS IM DETAIL
----------------------------------------------------------------------

1. Mein erster Meilenstein
   📅 15.03.2024
   📄 823 Wörter | ⏱️  4 Min. Lesezeit
   🔗 https://deinblog.de/meilenstein-1

🔤 TOP 15 HÄUFIGSTE WÖRTER
----------------------------------------------------------------------
entwicklung......... 23 ███████████████
projekt............. 18 ██████████████
daten............... 15 ████████████
```

## Analysierte Metriken

- **Post-Statistiken**: Anzahl, Gesamtwörter, Durchschnitte
- **Lesezeit**: Berechnet mit ~200 Wörtern/Minute
- **Zeitraum**: Erster bis letzter Post
- **Wortfrequenz**: Top-Begriffe über alle Posts
- **Einzelne Posts**: Titel, Datum, Länge, Link

## Use Cases

- 📝 Persönliches Schreibtracking
- 📊 Blog-Performance-Analyse
- 🔍 Thematische Schwerpunkte identifizieren
- 📈 Schreibgewohnheiten visualisieren
- 💾 Datenexport für weitere statistische Analysen

## Technische Details

- Nutzt WordPress REST API v2 (`/wp-json/wp/v2/posts`)
- Unterstützt Pagination für Blogs mit vielen Posts
- HTML-Reports mit responsivem Design
- JSON-Export kompatibel mit Pandas, R, Excel

## Erweiterungsmöglichkeiten

- Sentiment-Analyse mit `textblob` oder `vaderSentiment`
- Zeitreihen-Visualisierungen mit `matplotlib`
- Kategorie- und Tag-Analyse
- Vergleich zwischen verschiedenen Zeiträumen
- Export als CSV für Tableau/Power BI

## Lizenz

GNU General Public License v3.0

**Michael Karbacher**

---

*Entwickelt als Teil eines persönlichen Learning-Projekts für Data Analytics und Wissensmanagementsysteme.*