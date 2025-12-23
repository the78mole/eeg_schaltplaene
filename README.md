# Schaltpläne - Elektrische Schaltpläne für PV-Anlagen

Projektsammlung für elektrische Schaltpläne, insbesondere einpolige Schaltpläne für Hausanschlüsse mit PV-Anlagen und Stromspeichern zur Anmeldung beim Netzbetreiber.

## Übersicht

Dieses Projekt verwendet [Schemdraw](https://schemdraw.readthedocs.io/) zur programmatischen Erstellung von einpoligen Schaltplänen nach DIN EN 60617. Die Schaltpläne können bei Netzbetreibern zur Anmeldung von PV-Anlagen und Stromspeichern eingereicht werden.

## Features

- **Vorgefertigte Komponenten** - 12+ elektrotechnische Komponenten (Zähler, Schalter, Wechselrichter, etc.)
- **Templates** - Fertige Schaltplan-Vorlagen für typische Anwendungsfälle
- **Deutsche Bezeichnungen** - Alle Komponenten mit deutschen Fachbegriffen
- **VDE-konform** - Berücksichtigung von VDE-AR-N 4105 für Erzeugungsanlagen
- **Flexible Parametrisierung** - Anpassbare Werte für Leistungen, Ströme, etc.

## Installation

Dieses Projekt verwendet [uv](https://github.com/astral-sh/uv) für die Verwaltung von Abhängigkeiten.

### Voraussetzungen

```bash
# uv installieren (falls noch nicht vorhanden)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Projekt einrichten

```bash
# Abhängigkeiten installieren
uv sync
```

## Verwendung

### Templates verwenden (empfohlen)

Die einfachste Methode ist die Verwendung der vorgefertigten Templates:

```python
from schaltplaene.templates import PvSpeicherSystemUeberschuss, PvSystemUeberschuss

# PV-Anlage mit Speicher
template = PvSpeicherSystemUeberschuss(
    f1_nennstrom_a=50,
    f2_nennstrom_a=35,
    f2_charakteristik="E",
    z1_zaehler_nr="1EMH00xxx",
    hausverbrauch_kw=15.0,
    wechselrichter_kw=10.0,
    batterie_kwh=10.0,
    batterie_spannung_v=400,
    pv_leistung="10kWp"
)
template.speichere("meine_pv_anlage")

# PV-Anlage ohne Speicher
template = PvSystemUeberschuss(
    wechselrichter_kw=8.0,
    pv_leistung="8kWp"
)
template.speichere("pv_ohne_speicher")
```

### Eigene Schaltpläne erstellen

Für individuelle Schaltpläne können die Komponenten direkt verwendet werden:

```python
import schemdraw
import schemdraw.elements as elm
from schaltplaene.komponenten import Zaehler, Wechselrichter, PVModul

d = schemdraw.Drawing()
d.config(unit=2, fontsize=10)

# Komponenten platzieren
d += (zaehler := Zaehler(
    bezeichnung="P1",
    pfeil=ZaehlerPfeil.ARROW_BOTH
).at((0, 0)))

d += (wr := Wechselrichter(
    bezeichnung="T1",
    leistung_kw=10.0
).at((0, 2)))

# Verbindungen
d += elm.Line().at(zaehler.absanchors['end']).to(wr.absanchors['S'])

d.save('output/mein_schaltplan.png')
```

Siehe [KOMPONENTEN.md](KOMPONENTEN.md) für eine vollständige Übersicht aller verfügbaren Komponenten.

## Projektstruktur

```
schaltplaene/
├── src/
│   └── schaltplaene/
│       ├── komponenten/        # Wiederverwendbare Komponenten
│       │   ├── zaehler.py      # Energiezähler
│       │   ├── wechselrichter.py
│       │   ├── batterie.py
│       │   ├── pv_module.py
│       │   ├── schalter.py
│       │   ├── leitungsschutzschalter.py
│       │   ├── schmelzsicherung.py
│       │   ├── ueberspannungsschutz.py
│       │   ├── verbrauch.py
│       │   ├── netz.py
│       │   ├── erdung.py
│       │   └── pe_line.py      # Schutzleiter-Darstellung
│       ├── templates/          # Vorgefertigte Schaltplan-Templates
│       │   ├── pv_speicher_system_ueberschuss.py  # Mit Batterie
│       │   └── pv_system_ueberschuss.py           # Ohne Batterie
│       └── beispiele/          # Beispiel-Schaltpläne
│           └── pv_komplett.py
├── output/                     # Generierte Schaltpläne (PNG/SVG)
├── docs/                       # Dokumentation
├── README.md                   # Diese Datei
└── KOMPONENTEN.md              # Komponenten-Übersicht
```

## Templates

### PvSpeicherSystemUeberschuss
Komplette PV-Anlage mit Batteriespeicher und Überschusseinspeisung. Enthält:
- Netzanschluss mit HAK-Sicherung
- Leitungsschutzschalter
- Zweirichtungszähler
- Wechselrichter mit Batteriespeicher
- PV-Generator
- Hausverbrauch
- PE-Netz (Schutzleiter)

### PvSystemUeberschuss
PV-Anlage ohne Speicher mit Überschusseinspeisung. Wie oben, aber ohne Batterie.

## Komponenten

Eine vollständige Übersicht aller verfügbaren Komponenten mit Beispielbildern finden Sie in [KOMPONENTEN.md](KOMPONENTEN.md).

Wichtigste Komponenten:
- **Zaehler** - Energiezähler (ein-/zweirichtung)
- **Wechselrichter** - DC/AC-Wandler
- **Batterie** - Batteriespeicher
- **PVModul** - PV-Generator
- **Leitungsschutzschalter** - LS-Schalter mit Charakteristik
- **Schmelzsicherung** - NH-Sicherungen
- **Ueberspannungsschutz** - ÜSS Typ I/II/III
- **Netz** - Netzanschluss-Symbol
- **Erdung** - Potenzialausgleichschiene
- **PELine** - Schutzleiter (grün-gelb)

## Normen und Standards

Die Schaltpläne orientieren sich an:
- DIN EN 61082 (Erstellen von Dokumenten der Elektrotechnik)
- VDE-AR-N 4105 (Erzeugungsanlagen am Niederspannungsnetz)
- TAB (Technische Anschlussbedingungen des jeweiligen Netzbetreibers)

## Entwicklung

```bash
# Tests ausführen
uv run pytest

# Code formatieren
uv run ruff format

# Linting
uv run ruff check
```

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE). Sie können es frei verwenden, modifizieren und weitergeben.

## Beiträge

Beiträge sind willkommen! Bitte öffnen Sie ein Issue oder einen Pull Request auf GitHub.

## Kontakt

Elektro Glaser  
GitHub: [the78mole/eeg_schaltplaene](https://github.com/the78mole/eeg_schaltplaene)
