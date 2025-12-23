# GitHub Copilot Instruktionen für Schaltpläne-Projekt

## Projektkontext

Dies ist ein Python-Projekt zur Erstellung elektrischer Schaltpläne mit Schemdraw. Der Fokus liegt auf einpoligen Schaltplänen für Hausanschlüsse mit PV-Anlagen und Stromspeichern zur Anmeldung beim Netzbetreiber.

## Technologie-Stack

- **Python 3.11+**
- **Schemdraw** - Hauptbibliothek für Schaltplan-Erstellung
- **uv** - Paket- und Projektverwaltung (nicht pip!)
- **pytest** - Testing Framework
- **ruff** - Linting und Formatierung

## Code-Konventionen

### Allgemein
- Verwende deutsche Bezeichner für elektrotechnische Komponenten und Funktionen
- Englische Bezeichner für allgemeine Programmierkonzepte
- Docstrings auf Deutsch
- Kommentare auf Deutsch

### Beispiel
```python
def erstelle_pv_anlage(leistung_kwp: float, mit_speicher: bool = False):
    """
    Erstellt einen Schaltplan für eine PV-Anlage.
    
    Args:
        leistung_kwp: Nennleistung in kWp
        mit_speicher: Ob ein Batteriespeicher enthalten ist
    """
    pass
```

## Elektrische Konventionen

### Symbole und Bezeichnungen
- Verwende standardisierte Symbole nach DIN EN 61082
- Bezeichne Komponenten mit gängigen Abkürzungen:
  - `Z` für Zähler
  - `WR` für Wechselrichter
  - `PV` für Photovoltaik
  - `BAT` für Batteriespeicher
  - `LS` für Leitungsschutzschalter
  - `FI` für Fehlerstrom-Schutzschalter
  - `ÜSS` für Überspannungsschutz

### Phasenbezeichnungen
- Verwende L1, L2, L3 für Außenleiter
- N für Neutralleiter
- PE für Schutzleiter

### Farbcodes (in Kommentaren)
- Schwarz/Braun: L1
- Schwarz/Schwarz: L2
- Schwarz/Grau: L3
- Blau: N
- Grün-Gelb: PE

## Projektstruktur

### Komponenten (`src/schaltplaene/komponenten/`)
Erstelle wiederverwendbare Klassen für elektrische Komponenten:
- Erben von Schemdraw-Elementen oder erstelle Custom-Elemente
- Implementiere konsistente Anschluss-Points (`.start`, `.end`, etc.)
- Dokumentiere elektrische Parameter als Docstring

### Messkonzepte (`src/schaltplaene/messkonzepte/`)
Implementiere verschiedene Messkonzepte als Funktionen:
- Klare Benennung des Messkonzepts
- Parameter für Anpassungen (Zählertyp, Leistung, etc.)
- Rückgabe des Drawing-Objekts

### Beispiele (`src/schaltplaene/beispiele/`)
Konkrete Anwendungsfälle:
- Vollständige, ausführbare Skripte
- Speichere Ausgabe in `output/` Verzeichnis
- Verwende aussagekräftige Dateinamen (z.B. `output/pv_10kwp_mit_5kwh_speicher.png`)

## Best Practices für Schemdraw

### Drawing-Kontext
```python
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d.config(unit=2)  # Skalierung anpassen
    # Komponenten hinzufügen
    d.save('output/schaltplan.png')
```

### Verbindungen
- Verwende `.right()`, `.left()`, `.up()`, `.down()` für Richtungen
- Nutze `.at()` für präzise Positionierung
- Verwende `elm.Line()` für einfache Verbindungen
- Setze `elm.Dot()` an Verzweigungspunkten

### Labels
- Beschrifte alle wichtigen Komponenten
- Verwende `.label()` für Bezeichnungen
- Position mit `loc='top'`, `loc='bottom'`, etc. anpassen

### Lesbarkeit
- Gruppiere zusammengehörige Komponenten
- Kommentiere elektrische Zusammenhänge
- Halte Schaltpläne übersichtlich (ggf. in mehrere Zeichnungen aufteilen)

## Sicherheit und Normen

### Wichtige Hinweise in Code
Copilot sollte bei sicherheitsrelevanten Komponenten Kommentare hinzufügen:
```python
# WICHTIG: FI-Schutzschalter Typ A oder B für PV-Anlagen erforderlich
d += FISchutzschalter(typ='A')

# Hinweis: Trennstelle muss allpolig trennen (gem. VDE-AR-N 4105)
d += Trennstelle(allpolig=True)
```

### VDE-Konformität
- Beachte VDE-AR-N 4105 für Erzeugungsanlagen
- Implementiere NA-Schutz (Netz- und Anlagenschutz)
- Berücksichtige Selektivität bei Überstromschutz

## Testing

- Erstelle Tests für Komponenten-Erstellung
- Teste, ob Schaltpläne ohne Fehler generiert werden
- Validiere, dass alle erforderlichen Komponenten vorhanden sind

```python
def test_pv_anlage_vollstaendig():
    """Prüft ob PV-Anlage alle erforderlichen Komponenten enthält."""
    komponenten = erstelle_pv_anlage(10.0)
    assert 'zaehler' in komponenten
    assert 'wechselrichter' in komponenten
    assert 'pv_module' in komponenten
```

## Dokumentation

- README.md aktualisieren bei neuen Features
- Docstrings für alle öffentlichen Funktionen/Klassen
- Kommentare für komplexe elektrische Zusammenhänge
- Beispiele für jedes Messkonzept

## Abhängigkeiten hinzufügen

Verwende **ausschließlich uv**, niemals pip:
```bash
# Richtig
uv add schemdraw
uv add --dev pytest

# Falsch (niemals verwenden!)
pip install schemdraw
```

## Commit-Nachrichten

Verwende deutsche, aussagekräftige Commit-Messages:
- `feat: Messkonzept Kaskadenmessung hinzugefügt`
- `fix: Positionierung des FI-Schalters korrigiert`
- `docs: README um Installation erweitert`
- `refactor: Zähler-Komponente vereinfacht`
