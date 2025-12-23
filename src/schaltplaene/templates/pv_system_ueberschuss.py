"""Template: PV-Anlage ohne Speicher (Überschusseinspeisung).

Vorgefertigtes Template für eine PV-Anlage ohne Speicher:
- Netzanschluss mit HAK
- Zweirichtungszähler
- Wechselrichter
- PV-Generator
- Hausverbrauch
"""

import schemdraw
import schemdraw.elements as elm

from schaltplaene.komponenten.erdung import Erdung
from schaltplaene.komponenten.netz import Netz
from schaltplaene.komponenten.schmelzsicherung import Schmelzsicherung
from schaltplaene.komponenten.leitungsschutzschalter import Leitungsschutzschalter
from schaltplaene.komponenten.zaehler import Zaehler, ZaehlerPfeil
from schaltplaene.komponenten.schalter import Schalter
from schaltplaene.komponenten.enums import ComponentFlow
from schaltplaene.komponenten.verbrauch import Verbrauch
from schaltplaene.komponenten.wechselrichter import Wechselrichter
from schaltplaene.komponenten.ueberspannungsschutz import Ueberspannungsschutz
from schaltplaene.komponenten.pv_module import PVModul
from schaltplaene.komponenten.pe_line import PELine


class PvSystemUeberschuss:
    """Template für PV-Anlage ohne Speicher (Überschusseinspeisung).
    
    Dieses Template erstellt einen vollständigen Schaltplan mit allen
    erforderlichen Komponenten für eine PV-Anlage ohne Batteriespeicher
    und Überschusseinspeisung ins Netz.
    
    Args:
        f1_nennstrom_a: Nennstrom der HAK-Sicherung (F1) in Ampere (z.B. 50)
        f2_nennstrom_a: Nennstrom des Leitungsschutzschalters (F2) in Ampere (z.B. 35)
        f2_charakteristik: Charakteristik des LS (F2) (z.B. "E", "B", "C")
        z1_zaehler_nr: Zählernummer für Zähler P1 (z.B. "1EMH00xxx")
        hausverbrauch_kw: Maximale Leistung Hausverbrauch in kW (z.B. 15.0)
        wechselrichter_kw: Nennleistung Wechselrichter in kW (z.B. 10.0)
        pv_leistung: Nennleistung PV-Generator (z.B. "10kWp" oder 10.0)
    """
    
    def __init__(self,
                 f1_nennstrom_a: int = 50,
                 f2_nennstrom_a: int = 35,
                 f2_charakteristik: str = "E",
                 z1_zaehler_nr: str = "1EMH00xxx",
                 hausverbrauch_kw: float = 15.0,
                 wechselrichter_kw: float = 10.0,
                 pv_leistung = "10kWp"):
        """Initialisiert das PV-System-Template mit den angegebenen Parametern."""
        self.f1_nennstrom_a = f1_nennstrom_a
        self.f2_nennstrom_a = f2_nennstrom_a
        self.f2_charakteristik = f2_charakteristik
        self.z1_zaehler_nr = z1_zaehler_nr
        self.hausverbrauch_kw = hausverbrauch_kw
        self.wechselrichter_kw = wechselrichter_kw
        self.pv_leistung = pv_leistung
    
    def erstelle_schaltplan(self, titel: str = "PV-Anlage ohne Speicher - Überschusseinspeisung") -> schemdraw.Drawing:
        """Erstellt den kompletten Schaltplan.
        
        Args:
            titel: Titel des Schaltplans
            
        Returns:
            Schemdraw Drawing-Objekt mit dem vollständigen Schaltplan
        """
        # Drawing erstellen
        d = schemdraw.Drawing()
        d.config(unit=2, fontsize=10)
        
        # Titel
        d += elm.Label().at((3, -1)).label(titel, fontsize=14, halign='center')
        
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
        
        uss_dot_pos = (netz_pos[0], netz_pos[1] + 3)
        d += elm.Dot().at(uss_dot_pos)
        
        # 2. HAK mit Schmelzsicherung (F1)
        d += (hak := Schmelzsicherung(
            bezeichnung="F1",
            nennstrom_a=self.f1_nennstrom_a,
            kennlinie="gG",
            typ="NH00",
            flow=ComponentFlow.FLOW_V,
            hak=True
        ).at((3, netz_pos[1] + 2)))
        
        # 3. Leitungsschutzschalter (F2)
        d += (sls := Leitungsschutzschalter(
            bezeichnung="F2",
            nennstrom_a=self.f2_nennstrom_a,
            charakteristik=self.f2_charakteristik,
            flow=ComponentFlow.FLOW_V
        ).at((3, netz_pos[1] + 4)))
        
        # 4. Zweirichtungszähler 1 (P1)
        d += (zaehler1 := Zaehler(
            bezeichnung="P1",
            info=self.z1_zaehler_nr,
            pfeil=ZaehlerPfeil.ARROW_BOTH,
            flow=ComponentFlow.FLOW_V
        ).at((3, netz_pos[1] + 6)))
        
        # 5. Zweirichtungszähler 2 (P2 - Speichersystem)
        d += (zaehler2 := Zaehler(
            bezeichnung="P2",
            info="EMS SmartMeter",
            pfeil=ZaehlerPfeil.ARROW_BOTH,
            flow=ComponentFlow.FLOW_V
        ).at((3, netz_pos[1] + 8)))
        
        # 7. Sternpunkt (Verbindungspunkt) - direkt nach P2, ohne Q1
        sternpunkt_pos = (3, netz_pos[1] + 10)
        d += elm.Dot().at(sternpunkt_pos)
        
        # Von Sternpunkt nach rechts zum Haus
        d += (schalter_haus := Leitungsschutzschalter(
            bezeichnung="Q2",
            flow=ComponentFlow.FLOW_H
        ).at((5.5, sternpunkt_pos[1])))
        
        d += (haus := Verbrauch(
            bezeichnung="Hausverbrauch",
            leistung_kw=self.hausverbrauch_kw
        ).at((7.5, sternpunkt_pos[1])))
        
        # Von Sternpunkt nach oben zum Wechselrichter
        d += (schalter_wr := Leitungsschutzschalter(
            bezeichnung="Q3",
            flow=ComponentFlow.FLOW_V
        ).at((3, sternpunkt_pos[1] + 1.5)))
        
        d += (wechselrichter := Wechselrichter(
            bezeichnung="T1",
            leistung_kw=self.wechselrichter_kw,
            flip_h=True,
            label_loc="NE"
        ).at((3, sternpunkt_pos[1] + 4)))
        
        # PV-Modul oben am Wechselrichter (ohne Batterie)
        d += (pv := PVModul(
            bezeichnung="G1",
            leistung=self.pv_leistung
        ).at((3, sternpunkt_pos[1] + 6)))
        
        # Verbindungsleitungen
        d += elm.Line().at(netz.absanchors['N']).to(hak.absanchors['start'])
        d += elm.Line().at(hak.absanchors['end']).to(sls.absanchors['start'])
        d += elm.Line().at(sls.absanchors['end']).to(zaehler1.absanchors['start'])
        d += elm.Line().at(zaehler1.absanchors['end']).to(zaehler2.absanchors['start'])
        d += elm.Line().at(zaehler2.absanchors['end']).to(sternpunkt_pos)
        d += elm.Line().at(sternpunkt_pos).to(schalter_haus.absanchors['start'])
        d += elm.Line().at(sternpunkt_pos).to(schalter_wr.absanchors['start'])
        d += elm.Line().at(schalter_haus.absanchors['end']).to(haus.absanchors['W'])
        d += elm.Line().at(schalter_wr.absanchors['end']).to(wechselrichter.absanchors['S'])
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
        
        return d
    
    def speichere(self, dateiname_basis: str = "pv_system"):
        """Erstellt und speichert den Schaltplan als PNG und SVG.
        
        Args:
            dateiname_basis: Basis-Dateiname ohne Endung (z.B. "pv_system")
        """
        d = self.erstelle_schaltplan()
        d.save(f'output/{dateiname_basis}.png')
        d.save(f'output/{dateiname_basis}.svg')
        print(f"Schaltplan gespeichert: output/{dateiname_basis}.png und output/{dateiname_basis}.svg")


if __name__ == "__main__":
    """Beispiel-Verwendung des Templates."""
    # Standard-Konfiguration
    template = PvSystemUeberschuss()
    template.speichere("beispiel_pv_ohne_speicher_standard")
    
    # Angepasste Konfiguration
    template_custom = PvSystemUeberschuss(
        f1_nennstrom_a=63,
        f2_nennstrom_a=50,
        f2_charakteristik="C",
        z1_zaehler_nr="1EMH12345",
        hausverbrauch_kw=20.0,
        wechselrichter_kw=15.0,
        pv_leistung="15kWp"
    )
    template_custom.speichere("beispiel_pv_ohne_speicher_custom")
