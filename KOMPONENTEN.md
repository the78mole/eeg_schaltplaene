# Komponenten-Übersicht

Diese Datei listet alle verfügbaren Komponenten für die Schaltplan-Erstellung auf.

Alle Komponenten befinden sich im Modul `schaltplaene.komponenten` und können direkt importiert werden.

---

## 1. Zaehler (Energiezähler)

**Datei:** `zaehler.py`

Energiezähler mit verschiedenen Pfeilvarianten für Bezug, Einspeisung oder bidirektionalen Betrieb.

**Parameter:**
- `bezeichnung`: Bezeichner (z.B. "P1", "Z1")
- `info`: Zusatzinformation wie Zählernummer (z.B. "1EMH00xxx")
- `einheit`: Einheit (Standard: "kWh")
- `pfeil`: Pfeilrichtung (`ZaehlerPfeil.ARROW_NONE`, `ARROW_IN`, `ARROW_OUT`, `ARROW_BOTH`)
- `flow`: Durchflussrichtung (`ZaehlerFlow.FLOW_V` = vertikal, `FLOW_H` = horizontal)
- `tarif`: Tarifanzeige (`ZaehlerTarif.TARIF_NONE`, `TARIF_HT`, `TARIF_NT`, `TARIF_HT_NT`)
- `label_loc`: Beschriftungsposition ('N', 'S', 'E', 'W', 'NE', 'NO', 'NW', 'SE', 'SO', 'SW')

**Beispiel:**
```python
from schaltplaene.komponenten import Zaehler, ZaehlerPfeil, ZaehlerFlow

z = Zaehler(
    bezeichnung="P1",
    info="1EMH00xxx",
    pfeil=ZaehlerPfeil.ARROW_BOTH,
    flow=ZaehlerFlow.FLOW_V
)
```

![Zaehler](img/zaehler.svg)

---

## 2. Wechselrichter (DC/AC-Wandler)

**Datei:** `wechselrichter.py`

Wechselrichter mit DC- und AC-Anschlüssen, Leistungsangabe und optionaler Herstellerinfo.

**Parameter:**
- `bezeichnung`: Bezeichner (z.B. "T1", "WR1")
- `leistung_kw`: Nennleistung in kW
- `hersteller`: Herstellername (optional)
- `flip_h`: Horizontale Spiegelung (Standard: False)
- `label_loc`: Beschriftungsposition

**Beispiel:**
```python
from schaltplaene.komponenten import Wechselrichter

wr = Wechselrichter(
    bezeichnung="T1",
    leistung_kw=10.0,
    hersteller="SMA",
    flip_h=True
)
```

![Wechselrichter](img/wechselrichter.svg)

---

## 3. Batterie (Batteriespeicher)

**Datei:** `batterie.py`

Batteriespeicher mit Kapazitäts- und Spannungsangabe.

**Parameter:**
- `bezeichnung`: Bezeichner (z.B. "C1", "BAT1")
- `kapazitaet_kwh`: Speicherkapazität in kWh
- `spannung_v`: Nennspannung in V (Standard: 400)
- `label_loc`: Beschriftungsposition

**Beispiel:**
```python
from schaltplaene.komponenten import Batterie

bat = Batterie(
    bezeichnung="C1",
    kapazitaet_kwh=10.0,
    spannung_v=400
)
```

![Batterie](img/batterie.svg)

---

## 4. PVModul (PV-Generator)

**Datei:** `pv_module.py`

Photovoltaik-Generator mit Leistungsangabe.

**Parameter:**
- `bezeichnung`: Bezeichner (z.B. "G1", "PV1")
- `leistung`: Nennleistung als Zahl (z.B. 10.0) oder String (z.B. "12x455Wp", "10kWp")
- `label_loc`: Beschriftungsposition

**Beispiel:**
```python
from schaltplaene.komponenten import PVModul

pv = PVModul(
    bezeichnung="G1",
    leistung="12x455Wp"
)
```

![PV-Modul](img/pv_module.svg)

---

## 5. Leitungsschutzschalter (LS-Schalter)

**Datei:** `leitungsschutzschalter.py`

Leitungsschutzschalter mit Charakteristik und Nennstrom.

**Parameter:**
- `bezeichnung`: Bezeichner (z.B. "Q1", "LS1")
- `nennstrom_a`: Nennstrom in Ampere
- `charakteristik`: Auslösecharakteristik ("B", "C", "D", "E", ...)
- `flow`: Durchflussrichtung (`ComponentFlow.FLOW_V` oder `FLOW_H`)
- `label_loc`: Beschriftungsposition

**Beispiel:**
```python
from schaltplaene.komponenten import Leitungsschutzschalter, ComponentFlow

ls = Leitungsschutzschalter(
    bezeichnung="Q1",
    nennstrom_a=35,
    charakteristik="E",
    flow=ComponentFlow.FLOW_V
)
```

![Leitungsschutzschalter](img/leitungsschutzschalter.svg)

---

## 6. Schmelzsicherung (NH-Sicherung)

**Datei:** `schmelzsicherung.py`

Schmelzsicherung mit optionalem HAK-Rahmen (Hausanschlusskasten).

**Parameter:**
- `bezeichnung`: Bezeichner (z.B. "F1", "SLS1")
- `nennstrom_a`: Nennstrom in Ampere
- `kennlinie`: Kennlinie (z.B. "gG", "aM")
- `typ`: Bauform (z.B. "NH00", "NH1", "NH2")
- `hak`: HAK-Rahmen anzeigen (Standard: False)
- `flow`: Durchflussrichtung
- `label_loc`: Beschriftungsposition

**Beispiel:**
```python
from schaltplaene.komponenten import Schmelzsicherung, ComponentFlow

sicherung = Schmelzsicherung(
    bezeichnung="F1",
    nennstrom_a=50,
    kennlinie="gG",
    typ="NH00",
    hak=True,
    flow=ComponentFlow.FLOW_V
)
```

![Schmelzsicherung](img/schmelzsicherung.svg)

---

## 7. Schalter (Allgemeiner Schalter)

**Datei:** `schalter.py`

Allgemeiner Schalter ohne Auslösecharakteristik.

**Parameter:**
- `bezeichnung`: Bezeichner (z.B. "Q1", "S1")
- `flow`: Durchflussrichtung
- `label_loc`: Beschriftungsposition

**Beispiel:**
```python
from schaltplaene.komponenten import Schalter, ComponentFlow

schalter = Schalter(
    bezeichnung="Q1",
    flow=ComponentFlow.FLOW_H
)
```

![Schalter](img/schalter.svg)

---

## 8. Ueberspannungsschutz (ÜSS)

**Datei:** `ueberspannungsschutz.py`

Überspannungsschutz mit Typ-Angabe und Schutzpegel.

**Parameter:**
- `bezeichnung`: Bezeichner (z.B. "F1", "USS1")
- `typ`: Schutztyp (z.B. "Typ I", "Typ II", "Typ I+II+III")
- `schutzpegel_kv`: Schutzpegel in kV (optional)
- `flow`: Durchflussrichtung
- `label_loc`: Beschriftungsposition

**Beispiel:**
```python
from schaltplaene.komponenten import Ueberspannungsschutz, ComponentFlow

uess = Ueberspannungsschutz(
    bezeichnung="F1",
    typ="Typ I+II+III",
    schutzpegel_kv=1.5,
    flow=ComponentFlow.FLOW_H
)
```

![Überspannungsschutz](img/ueberspannungsschutz.svg)

---

## 9. Verbrauch (Hausverbrauch)

**Datei:** `verbrauch.py`

Symbolische Darstellung des Hausverbrauchs mit Haus-Icon.

**Parameter:**
- `bezeichnung`: Bezeichner (z.B. "Hausverbrauch")
- `leistung_kw`: Maximale Leistung in kW (optional)
- `label_loc`: Beschriftungsposition

**Beispiel:**
```python
from schaltplaene.komponenten import Verbrauch

haus = Verbrauch(
    bezeichnung="Hausverbrauch",
    leistung_kw=15.0
)
```

![Verbrauch](img/verbrauch.svg)

---

## 10. Netz (Netzanschluss)

**Datei:** `netz.py`

Netzanschluss-Symbol mit Strommast-Darstellung.

**Parameter:**
- `bezeichnung`: Bezeichner (z.B. "Netz", "EVU")
- `spannung_v`: Netzspannung als Zahl (z.B. 400) oder String (z.B. "3 x 230/400V")
- `label_loc`: Beschriftungsposition

**Beispiel:**
```python
from schaltplaene.komponenten import Netz

netz = Netz(
    bezeichnung="Netz",
    spannung_v="3 x 230/400V"
)
```

![Netz](img/netz.svg)

---

## 11. Erdung (Potenzialausgleichschiene)

**Datei:** `erdung.py`

Erdungssymbol für Potenzialausgleichschiene (PAS).

**Parameter:**
- `bezeichnung`: Bezeichner (z.B. "PAS", "Erdung")
- `label_loc`: Beschriftungsposition

**Beispiel:**
```python
from schaltplaene.komponenten import Erdung

pas = Erdung(
    bezeichnung="PAS",
    label_loc='E'
)
```

![Erdung](img/erdung.svg)

---

## 12. PELine (Schutzleiter)

**Datei:** `pe_line.py`

Schutzleiter-Linie in grün-gelb (Overlay-Technik).

**Parameter:**
- `to_pos`: Zielposition als Tupel (x, y) relativ zum Startpunkt

**Beispiel:**
```python
from schaltplaene.komponenten.pe_line import PELine

# PE-Linie nach rechts (2 Einheiten)
d += PELine(to_pos=(2, 0)).at(startpunkt)

# PE-Linie nach oben (3 Einheiten)
d += PELine(to_pos=(0, 3)).at(startpunkt)
```

![PE-Line](img/pe_line.svg)

---

## 13. Fehlerstromschutzschalter (FI-Schalter)

**Datei:** `fehlerstromschutzschalter.py`

Fehlerstrom-Schutzschalter (RCD) mit Typ und Auslösestrom.

**Parameter:**
- `bezeichnung`: Bezeichner (z.B. "F1", "FI1")
- `auslösestrom_ma`: Auslösestrom in mA (z.B. 30, 300)
- `typ`: FI-Typ ("A", "B", "F", ...)
- `flow`: Durchflussrichtung
- `label_loc`: Beschriftungsposition

**Beispiel:**
```python
from schaltplaene.komponenten import Fehlerstromschutzschalter, ComponentFlow

fi = Fehlerstromschutzschalter(
    bezeichnung="F1",
    auslösestrom_ma=30,
    typ="A",
    flow=ComponentFlow.FLOW_V
)
```

![FI-Schutzschalter](img/fehlerstromschutzschalter.svg)

---

## Label-Positionen

Alle Komponenten unterstützen die folgenden Label-Positionen über den Parameter `label_loc`:

- **N** - Norden (oben)
- **S** - Süden (unten)
- **E** - Osten (rechts)
- **W** - Westen (links)
- **NE** / **NO** - Nordost (oben rechts)
- **NW** - Nordwest (oben links)
- **SE** / **SO** - Südost (unten rechts)
- **SW** - Südwest (unten links)

## Anchors (Anschlusspunkte)

Jede Komponente stellt Ankerpunkte für Verbindungsleitungen bereit:

**Wichtig:** Verwenden Sie `absanchors` für Verbindungen nach der Platzierung mit `.at()`:

```python
# Komponente platzieren
d += (komponente := MeineKomponente().at((2, 3)))

# Verbindung zu absanchors (absolute Koordinaten)
d += elm.Line().at(komponente.absanchors['N']).to(andere_komponente.absanchors['S'])
```

Häufige Anchors:
- `N`, `S`, `E`, `W` - Himmelsrichtungen
- `start`, `end` - Ein-/Ausgang bei Durchflusskomponenten
- `PE` - Schutzleiteranschluss
- `1`, `2`, `3` - Nummerierte Anschlüsse

---

## Verwendung im Code

```python
import schemdraw
import schemdraw.elements as elm
from schaltplaene.komponenten import (
    Zaehler, ZaehlerPfeil, ZaehlerFlow,
    Wechselrichter,
    Batterie,
    PVModul,
    Leitungsschutzschalter,
    ComponentFlow
)

d = schemdraw.Drawing()
d.config(unit=2, fontsize=10)

# Komponenten platzieren
d += (z := Zaehler(
    bezeichnung="P1",
    pfeil=ZaehlerPfeil.ARROW_BOTH,
    flow=ZaehlerFlow.FLOW_V
).at((0, 0)))

d += (wr := Wechselrichter(
    bezeichnung="T1",
    leistung_kw=10.0
).at((0, 2)))

# Verbindungen
d += elm.Line().at(z.absanchors['end']).to(wr.absanchors['S'])

d.save('output/mein_schaltplan.png')
```

---

Zurück zur [README](README.md)
