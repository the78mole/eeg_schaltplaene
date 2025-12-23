"""Beispiel: Komplette PV-Anlage mit Speicher.

Zeigt eine vollständige PV-Anlage mit Netzanschluss, Zählern,
Wechselrichter, Batteriespeicher und Hausverbrauch.
"""

import schemdraw
import schemdraw.elements as elm

from schaltplaene.komponenten.erdung import Erdung
from schaltplaene.komponenten.netz import Netz
from schaltplaene.komponenten.schmelzsicherung import Schmelzsicherung
from schaltplaene.komponenten.leitungsschutzschalter import Leitungsschutzschalter
from schaltplaene.komponenten.zaehler import Zaehler, ZaehlerPfeil, ZaehlerFlow
from schaltplaene.komponenten.schalter import Schalter
from schaltplaene.komponenten.enums import ComponentFlow
from schaltplaene.komponenten.verbrauch import Verbrauch
from schaltplaene.komponenten.wechselrichter import Wechselrichter
from schaltplaene.komponenten.batterie import Batterie
from schaltplaene.komponenten.ueberspannungsschutz import Ueberspannungsschutz
from schaltplaene.komponenten.pv_module import PVModul
from schaltplaene.komponenten.pe_line import PELine


# Drawing erstellen
d = schemdraw.Drawing()
d.config(unit=2, fontsize=10)

# Titel
d += elm.Label().at((3, -1)).label("PV-Anlage mit Speicher und Netzanschluss", fontsize=14, halign='center')

# 1. Unten: Netz-Symbol
netz_pos = (3, 0)
d += (netz := Netz(
    bezeichnung="Netz",
    spannung_v="3 x 230/400V",
    label_loc="E"
).at(netz_pos))

d += (hpas := Erdung(
    bezeichnung="PAS",
    label_loc='E'
).at((netz_pos[0] - 4, netz_pos[1] + 0.3)))

d += (uss := Ueberspannungsschutz(
    bezeichnung="F2",
    typ="Typ I+II+III",
    schutzpegel_kv=1.5,
    flow=ComponentFlow.FLOW_H,
    label_loc='S'
).at((netz_pos[0] - 2, netz_pos[1] + 3)))
# Verbindung nach oben
#d += elm.Line().at(netz.anchors['N']).up(0.5)

uss_dot_pos = (netz_pos[0], netz_pos[1] + 3)
d += elm.Dot().at(uss_dot_pos)

# 2. HAK mit Schmelzsicherung 50A
d += (hak := Schmelzsicherung(
    bezeichnung="F1",
    nennstrom_a=50,
    kennlinie="gG",
    typ="NH00",
    flow=ComponentFlow.FLOW_V,
    hak=True
).at((3, netz_pos[1] + 2)))

# Verbindung nach oben
#d += elm.Line().at(hak.anchors['end']).up(0.5)

# 3. Leitungsschutzschalter 35A (Zählervorsicherung/SLS)
d += (sls := Leitungsschutzschalter(
    bezeichnung="F2",
    nennstrom_a=35,
    charakteristik="E",
    flow=ComponentFlow.FLOW_V
).at((3, netz_pos[1] + 4)))

# Verbindung nach oben
#d += elm.Line().at(sls.anchors['end']).up(0.5)

# 4. Zweirichtungszähler 1
d += (zaehler1 := Zaehler(
    bezeichnung="P1",
    info="1EMH00xxx",
    pfeil=ZaehlerPfeil.ARROW_BOTH,
    flow=ZaehlerFlow.FLOW_V
).at((3, netz_pos[1] + 6)))

# Verbindung nach oben
#d += elm.Line().at(zaehler1.anchors['end']).up(0.5)

# 5. Zweirichtungszähler 2 (Speichersystem)
d += (zaehler2 := Zaehler(
    bezeichnung="P2",
    info="EMS SmartMeter",
    pfeil=ZaehlerPfeil.ARROW_BOTH,
    flow=ZaehlerFlow.FLOW_V
).at((3, netz_pos[1] + 8)))

# Verbindung nach oben
#d += elm.Line().at(zaehler2.anchors['end']).up(0.5)

# 6. Schalter (Netztrennung)
d += (trennung := Leitungsschutzschalter(
    bezeichnung="Q1",
    flow=ComponentFlow.FLOW_V
).at((3, netz_pos[1] + 10)))

# Verbindung nach oben zum Sternpunkt
#d += elm.Line().at(trennung.anchors['end']).up(0.5)

# 7. Sternpunkt (Verbindungspunkt)
sternpunkt_pos = (3, netz_pos[1] + 11.3)
d += elm.Dot().at(sternpunkt_pos)

# Von Sternpunkt nach rechts zum Haus
#d += elm.Line().at(sternpunkt_pos).right(1.5)
d += (schalter_haus := Leitungsschutzschalter(
    bezeichnung="Q2",
    flow=ComponentFlow.FLOW_H
).at((5.5, sternpunkt_pos[1])))

# Verbindung zum Haus
#d += elm.Line().at(schalter_haus.anchors['end']).right(1)
d += (haus := Verbrauch(
    bezeichnung="Hausverbrauch",
    leistung_kw=15.0
).at((7.5, sternpunkt_pos[1])))

# Von Sternpunkt nach oben zum Wechselrichter
#d += elm.Line().at(sternpunkt_pos).up(0.5)
d += (schalter_wr := Leitungsschutzschalter(
    bezeichnung="Q3",
    flow=ComponentFlow.FLOW_V
).at((3, sternpunkt_pos[1] + 1.5)))

# Verbindung zum Wechselrichter
#d += elm.Line().at(schalter_wr.anchors['end']).up(1)
d += (wechselrichter := Wechselrichter(
    bezeichnung="T1",
    leistung_kw=10.0,
    flip_h=True,
    label_loc="NE"
).at((3, sternpunkt_pos[1] + 4)))

# Batterie rechts vom Wechselrichter
#d += elm.Line().at(wechselrichter.anchors['E']).right(1)
d += (batterie := Batterie(
    bezeichnung="C1",
    kapazitaet_kwh=10.0,
    spannung_v=400,
    label_loc="E"
).at((6, sternpunkt_pos[1] + 4)))

# PV-Modul oben am Wechselrichter
#d += elm.Line().at(wechselrichter.anchors['W']).up(1)
d += (pv := PVModul(
    bezeichnung="G1",
    leistung="10kWp"
).at((3, sternpunkt_pos[1] + 6)))

d += elm.Line().at(netz.absanchors['N']).to(hak.absanchors['start'])
d += elm.Line().at(hak.absanchors['end']).to(sls.absanchors['start'])
d += elm.Line().at(sls.absanchors['end']).to(zaehler1.absanchors['start'])
d += elm.Line().at(zaehler1.absanchors['end']).to(zaehler2.absanchors['start'])
d += elm.Line().at(zaehler2.absanchors['end']).to(trennung.absanchors['start'])
d += elm.Line().at(trennung.absanchors['end']).to(sternpunkt_pos)
d += elm.Line().at(sternpunkt_pos).to(schalter_haus.absanchors['start'])
d += elm.Line().at(sternpunkt_pos).to(schalter_wr.absanchors['start'])
d += elm.Line().at(schalter_haus.absanchors['end']).to(haus.absanchors['W'])
d += elm.Line().at(schalter_wr.absanchors['end']).to(wechselrichter.absanchors['S'])
d += elm.Line().at(wechselrichter.absanchors['E']).to(batterie.absanchors['W'])
d += elm.Line().at(wechselrichter.absanchors['N']).to(pv.absanchors['start'])
d += elm.Line().at(uss.absanchors['2']).to(uss_dot_pos)

# Erdungsverbindung (PE-Leiter) als grün-gelb-gestrichelte Linie
# Vertikale Linie von PAS bis zur Höhe des PV-Moduls
pe_vertical_dy = pv.absanchors['PE'].y - hpas.absanchors['start'].y
d += PELine(to_pos=(0, pe_vertical_dy)).at(hpas.absanchors['start'])

# Abzweig zum Überspannungsschutz auf Höhe USS
pe_uss_junction = (hpas.absanchors['start'].x, uss.absanchors['1'].y)
d += elm.Dot().at(pe_uss_junction).color('green')

# Horizontale PE-Linie zum Überspannungsschutz
pe_uss_dx = uss.absanchors['1'].x - pe_uss_junction[0]
d += PELine(to_pos=(pe_uss_dx, 0)).at(pe_uss_junction)

# Abzweig zum Wechselrichter auf Höhe WR-W
pe_wr_junction = (hpas.absanchors['start'].x, wechselrichter.absanchors['W'].y)
d += elm.Dot().at(pe_wr_junction).color('green')

# Horizontale PE-Linie zum Wechselrichter
pe_wr_dx = wechselrichter.absanchors['W'].x - pe_wr_junction[0]
d += PELine(to_pos=(pe_wr_dx, 0)).at(pe_wr_junction)

# Horizontale Linie zum PV-Modul PE-Anker
pe_horizontal_start = (hpas.absanchors['start'].x, pv.absanchors['PE'].y)
pe_horizontal_dx = pv.absanchors['PE'].x - hpas.absanchors['start'].x
d += PELine(to_pos=(pe_horizontal_dx, 0)).at(pe_horizontal_start)



# Ausgabe speichern
d.save('output/beispiel_pv_komplett.png')
d.save('output/beispiel_pv_komplett.svg')
print("Komplett-Schaltplan gespeichert: output/beispiel_pv_komplett.png und output/beispiel_pv_komplett.svg")
