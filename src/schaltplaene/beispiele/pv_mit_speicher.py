"""
Beispiel: PV-Anlage mit Batteriespeicher und Kaskadenmessung.

Typischer Aufbau für eine PV-Anlage mit Speicher zur Anmeldung beim Netzbetreiber.
Messkonzept: Kaskadenmessung (Zweirichtungszähler für Netz, Erzeugungszähler für PV)
"""

import schemdraw
import schemdraw.elements as elm
from pathlib import Path

from schaltplaene.komponenten import (
    ZweirichtungsZaehler,
    HybridInverter,
    PVString,
    Trennstelle,
    Leitungsschutzschalter,
    FISchutzschalter,
)


def erstelle_schaltplan(
    pv_leistung_kwp: float = 10.0,
    speicher_kwh: float = 5.0,
    inverter_leistung_kw: float = 10.0,
    ausgabepfad: str = "output/pv_mit_speicher.png"
):
    """
    Erstellt einen einpoligen Schaltplan für PV-Anlage mit Speicher.
    
    Args:
        pv_leistung_kwp: Nennleistung der PV-Anlage in kWp
        speicher_kwh: Speicherkapazität in kWh
        inverter_leistung_kw: Wechselrichter-Leistung in kW
        ausgabepfad: Pfad für die Ausgabedatei
    """
    
    d = schemdraw.Drawing()
    d.config(unit=2, fontsize=10)
    
    # Titel
    d += elm.Label().at((0, 3)).label(
        f"PV-Anlage mit Speicher\n{pv_leistung_kwp}kWp PV + {speicher_kwh}kWh Speicher",
        fontsize=14
    )
    
    # === Netzanschluss ===
    d += elm.Line().right(1).at((0, 0)).label('Netz', loc='left')
    d += elm.Dot()
    
    # === Zähler (Zweirichtungszähler) ===
    d += elm.Line().right(0.5)
    zaehler_pos = d.here
    d += ZweirichtungsZaehler(bezeichnung="Z1")
    d += elm.Line().right(0.5)
    
    # === Hausanschlusskasten (HAK) ===
    d += elm.Dot()
    hak_verzweigung = d.here
    
    # Abzweig zum Haus (nach unten)
    d += elm.Line().at(hak_verzweigung).down(1.5)
    d += elm.Dot().label('Hausinstallation\n(Verbraucher)', loc='bottom')
    
    # === Weiter zur PV-Anlage (nach rechts) ===
    d += elm.Line().at(hak_verzweigung).right(1)
    
    # Hauptschalter PV-Anlage
    d += Trennstelle(bezeichnung="HS-PV", allpolig=True)
    d += elm.Line().right(0.5)
    
    # Leitungsschutzschalter
    d += Leitungsschutzschalter(bezeichnung="LS", nennstrom_a=25, charakteristik="C")
    d += elm.Line().right(0.5)
    
    # FI-Schutzschalter (Typ A für PV erforderlich!)
    d += FISchutzschalter(typ="A", nennstrom_a=25, ausloesstrom_ma=30)
    d += elm.Line().right(0.5)
    
    # === Hybrid-Wechselrichter ===
    d += elm.Dot()
    wr_eingang = d.here
    
    d += elm.Line().right(0.5)
    wr = HybridInverter(bezeichnung="Hybrid-WR", leistung_kw=inverter_leistung_kw)
    d += wr
    
    # === PV-Module (nach oben vom WR) ===
    # Vereinfachte Darstellung ohne komplexe Anchor-Verweise
    d += elm.Line().at(wr_eingang).up(2)
    d += elm.Dot().label('DC+', loc='left')
    d += elm.Line().up(0.5)
    d += PVString(anzahl_module=25, leistung_pro_modul_wp=400)
    
    # === Batteriespeicher (nach unten vom WR) ===
    d += elm.Line().at(wr_eingang).down(1)
    d += elm.Dot().label('Batterie', loc='left')
    d += elm.Line().down(0.3)
    d += elm.Battery().label(f'{speicher_kwh}kWh', loc='right')
    
    # === Zusätzliche Beschriftungen ===
    d += elm.Label().at((zaehler_pos[0], zaehler_pos[1] - 1)).label(
        'Messkonzept:\nKaskadenmessung',
        fontsize=8
    )
    
    # Legende
    d += elm.Label().at((0, -3)).label(
        'Anmerkungen:\n'
        '• FI Typ A erforderlich für PV-Anlagen\n'
        '• Hauptschalter muss allpolig trennen\n'
        '• Zähler: Zweirichtungszähler (Bezug/Einspeisung)\n'
        '• Ersatzstromfunktion über Hybrid-WR',
        fontsize=8,
        halign='left'
    )
    
    # Speichern
    output_path = Path(ausgabepfad)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    d.save(str(output_path))
    print(f"Schaltplan gespeichert: {output_path}")


if __name__ == "__main__":
    erstelle_schaltplan()
