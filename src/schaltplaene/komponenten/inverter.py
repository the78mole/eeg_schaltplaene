"""
Wechselrichter-Komponenten für PV-Anlagen.
"""

import schemdraw
import schemdraw.elements as elm
from schemdraw.elements import Element
from schemdraw import segments


class PVWechselrichter(Element):
    """
    PV-Wechselrichter zur Umwandlung von DC in AC.
    
    Darstellung als Rechteck mit '~' Symbol und WR Beschriftung.
    """
    
    def __init__(self, bezeichnung: str = "WR", leistung_kw: float = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Rechteck für Wechselrichter
        w, h = 1.2, 1.2
        self.segments.append(segments.Segment([(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2), (-w/2, -h/2)]))
        
        self.anchors['center'] = (0, 0)
        self.anchors['dc'] = (-w/2, 0)  # DC-Eingang (PV-Seite)
        self.anchors['ac'] = (w/2, 0)   # AC-Ausgang (Netz-Seite)
        
        # Beschriftung
        label_text = f"{bezeichnung}\n~"
        if leistung_kw:
            label_text += f"\n{leistung_kw}kW"
        self.label(label_text, loc='center', fontsize=10)


class HybridInverter(Element):
    """
    Hybrid-Wechselrichter mit Batterieanbindung.
    
    Erweitert den PV-Wechselrichter um einen Batterie-Anschluss.
    """
    
    def __init__(self, bezeichnung: str = "Hybrid-WR", leistung_kw: float = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Rechteck für Wechselrichter
        w, h = 1.5, 1.5
        self.segments.append(segments.Segment([(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2), (-w/2, -h/2)]))
        
        self.anchors['center'] = (0, 0)
        self.anchors['pv'] = (-w/2, h/4)    # DC-Eingang PV
        self.anchors['bat'] = (-w/2, -h/4)  # DC-Anschluss Batterie
        self.anchors['ac'] = (w/2, 0)       # AC-Ausgang
        
        # Beschriftung
        label_text = f"{bezeichnung}\n~"
        if leistung_kw:
            label_text += f"\n{leistung_kw}kW"
        self.label(label_text, loc='center', fontsize=9)


if __name__ == "__main__":
    """Visualisierung der Wechselrichter-Komponenten."""
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=12)
    
    # Titel
    d += elm.Label().at((0, 4)).label("Wechselrichter-Komponenten", fontsize=14)
    
    # PV-Wechselrichter
    d += elm.Label().at((0, 3)).label("PV-Wechselrichter:", halign='left', fontsize=10)
    d += elm.Line().at((0, 2)).right(1).label('DC', loc='top')
    d += PVWechselrichter(bezeichnung="WR", leistung_kw=10.0)
    d += elm.Line().right(1).label('AC', loc='top')
    
    # Hybrid-Wechselrichter
    d += elm.Label().at((0, 0)).label("Hybrid-Wechselrichter:", halign='left', fontsize=10)
    d += elm.Line().at((0, -1)).right(1).label('PV-DC', loc='top')
    wr = HybridInverter(bezeichnung="Hybrid-WR", leistung_kw=10.0)
    d += wr
    d += elm.Line().right(1).label('AC', loc='top')
    
    # Batterieanschluss darstellen
    d += elm.Line().at((1, -1)).down(0.5).label('Batterie', loc='right')
    
    # Speichern und anzeigen
    from pathlib import Path
    output_path = Path("output/komponenten_inverter.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    d.save(str(output_path))
    print(f"Wechselrichter-Komponenten gespeichert: {output_path}")
