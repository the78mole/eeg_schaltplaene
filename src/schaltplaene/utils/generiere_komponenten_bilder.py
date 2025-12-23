"""Generiert Beispielbilder für alle Komponenten für die Dokumentation.

Dieses Skript erstellt für jede Komponente ein kleines Beispielbild
und speichert es im img/ Verzeichnis.
"""

import schemdraw
import schemdraw.elements as elm

from schaltplaene.komponenten.zaehler import Zaehler, ZaehlerPfeil, ZaehlerFlow
from schaltplaene.komponenten.wechselrichter import Wechselrichter
from schaltplaene.komponenten.batterie import Batterie
from schaltplaene.komponenten.pv_module import PVModul
from schaltplaene.komponenten.leitungsschutzschalter import Leitungsschutzschalter
from schaltplaene.komponenten.schmelzsicherung import Schmelzsicherung
from schaltplaene.komponenten.schalter import Schalter
from schaltplaene.komponenten.enums import ComponentFlow
from schaltplaene.komponenten.ueberspannungsschutz import Ueberspannungsschutz
from schaltplaene.komponenten.verbrauch import Verbrauch
from schaltplaene.komponenten.netz import Netz
from schaltplaene.komponenten.erdung import Erdung
from schaltplaene.komponenten.pe_line import PELine
from schaltplaene.komponenten.fehlerstromschutzschalter import FISchutzschalter


def generiere_alle_bilder():
    """Generiert Beispielbilder für alle Komponenten."""
    
    # 1. Zaehler
    print("Generiere Zaehler...")
    d = schemdraw.Drawing()
    d.config(unit=2, fontsize=10)
    d += Zaehler(
        bezeichnung="P1",
        info="1EMH00xxx",
        pfeil=ZaehlerPfeil.ARROW_BOTH,
        flow=ZaehlerFlow.FLOW_V
    ).at((0, 0))
    d.save('img/zaehler.png')
    d.save('img/zaehler.svg')
    
    # 2. Wechselrichter
    print("Generiere Wechselrichter...")
    d = schemdraw.Drawing()
    d.config(unit=2, fontsize=10)
    d += Wechselrichter(
        bezeichnung="T1",
        leistung_kw=10.0,
        hersteller="SMA",
        label_loc="E"
    ).at((0, 0))
    d.save('img/wechselrichter.png')
    d.save('img/wechselrichter.svg')
    
    # 3. Batterie
    print("Generiere Batterie...")
    d = schemdraw.Drawing()
    d.config(unit=2, fontsize=10)
    d += Batterie(
        bezeichnung="C1",
        kapazitaet_kwh=10.0,
        spannung_v=400,
        label_loc="E"
    ).at((0, 0))
    d.save('img/batterie.png')
    d.save('img/batterie.svg')
    
    # 4. PVModul
    print("Generiere PV-Modul...")
    d = schemdraw.Drawing()
    d.config(unit=2, fontsize=10)
    d += PVModul(
        bezeichnung="G1",
        leistung="12x455Wp",
        label_loc="E"
    ).at((0, 0))
    d.save('img/pv_module.png')
    d.save('img/pv_module.svg')
    
    # 5. Leitungsschutzschalter
    print("Generiere Leitungsschutzschalter...")
    d = schemdraw.Drawing()
    d.config(unit=2, fontsize=10)
    d += Leitungsschutzschalter(
        bezeichnung="Q1",
        nennstrom_a=35,
        charakteristik="E",
        flow=ComponentFlow.FLOW_V,
        label_loc="E"
    ).at((0, 0))
    d.save('img/leitungsschutzschalter.png')
    d.save('img/leitungsschutzschalter.svg')
    
    # 6. Schmelzsicherung
    print("Generiere Schmelzsicherung...")
    d = schemdraw.Drawing()
    d.config(unit=2, fontsize=10)
    d += Schmelzsicherung(
        bezeichnung="F1",
        nennstrom_a=50,
        kennlinie="gG",
        typ="NH00",
        hak=True,
        flow=ComponentFlow.FLOW_V,
        label_loc="E"
    ).at((0, 0))
    d.save('img/schmelzsicherung.png')
    d.save('img/schmelzsicherung.svg')
    
    # 7. Schalter
    print("Generiere Schalter...")
    d = schemdraw.Drawing()
    d.config(unit=2, fontsize=10)
    d += Schalter(
        bezeichnung="Q1",
        flow=ComponentFlow.FLOW_V,
        label_loc="E"
    ).at((0, 0))
    d.save('img/schalter.png')
    d.save('img/schalter.svg')
    
    # 8. Ueberspannungsschutz
    print("Generiere Überspannungsschutz...")
    d = schemdraw.Drawing()
    d.config(unit=2, fontsize=10)
    d += Ueberspannungsschutz(
        bezeichnung="F1",
        typ="Typ I+II+III",
        schutzpegel_kv=1.5,
        flow=ComponentFlow.FLOW_H,
        label_loc="S"
    ).at((0, 0))
    d.save('img/ueberspannungsschutz.png')
    d.save('img/ueberspannungsschutz.svg')
    
    # 9. Verbrauch
    print("Generiere Verbrauch...")
    d = schemdraw.Drawing()
    d.config(unit=2, fontsize=10)
    d += Verbrauch(
        bezeichnung="Hausverbrauch",
        leistung_kw=15.0,
        label_loc="E"
    ).at((0, 0))
    d.save('img/verbrauch.png')
    d.save('img/verbrauch.svg')
    
    # 10. Netz
    print("Generiere Netz...")
    d = schemdraw.Drawing()
    d.config(unit=2, fontsize=10)
    d += Netz(
        bezeichnung="Netz",
        spannung_v="3 x 230/400V",
        label_loc="E"
    ).at((0, 0))
    d.save('img/netz.png')
    d.save('img/netz.svg')
    
    # 11. Erdung
    print("Generiere Erdung...")
    d = schemdraw.Drawing()
    d.config(unit=2, fontsize=10)
    d += Erdung(
        bezeichnung="PAS",
        label_loc='E'
    ).at((0, 0))
    d.save('img/erdung.png')
    d.save('img/erdung.svg')
    
    # 12. PELine
    print("Generiere PE-Line...")
    d = schemdraw.Drawing()
    d.config(unit=2, fontsize=10)
    d += elm.Dot().at((0, 0)).label('Start', loc='left')
    d += PELine(to_pos=(2, 0)).at((0, 0))
    d += elm.Dot().at((2, 0)).label('Ende', loc='right')
    d.save('img/pe_line.png')
    d.save('img/pe_line.svg')
    
    # 13. Fehlerstromschutzschalter
    print("Generiere FI-Schutzschalter...")
    d = schemdraw.Drawing()
    d.config(unit=2, fontsize=10)
    d += FISchutzschalter(
        bezeichnung="F1",
        ausloesstrom_ma=30,
        typ="A",
        flow=ComponentFlow.FLOW_V,
        label_loc="E"
    ).at((0, 0))
    d.save('img/fehlerstromschutzschalter.png')
    d.save('img/fehlerstromschutzschalter.svg')
    
    print("\nAlle Komponenten-Bilder wurden im Ordner 'img/' gespeichert.")


if __name__ == "__main__":
    generiere_alle_bilder()
