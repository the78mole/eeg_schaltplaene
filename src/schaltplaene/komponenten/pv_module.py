"""
PV-Modul und String-Komponenten.
"""

import schemdraw
import schemdraw.elements as elm
from schemdraw.elements import Element
from schemdraw import segments


class PVModul(Element):
    """
    Einzelnes PV-Modul nach DIN EN 60617.
    
    Darstellung als längliches Rechteck mit nach innen gerichteter Dreieckspitze am oberen Ende.
    
    Args:
        leistung: Optionale Leistungsangabe als Zahl (in Wp) oder als Text (z.B. "12x455Wp")
        bezeichnung: Optionale Bezeichnung (z.B. "PV1")
    """
    
    def __init__(self, leistung = None, bezeichnung: str = None, debug: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Längliches Rechteck
        breite = 0.6
        hoehe = 1.2
        
        # Rechteck
        self.segments.append(segments.Segment([
            (-breite/2, -hoehe/2),
            (breite/2, -hoehe/2),
            (breite/2, hoehe/2),
            (-breite/2, hoehe/2),
            (-breite/2, -hoehe/2)
        ]))
        
        # Dreieckspitze am oberen Ende (nach innen gerichtet)
        dreieck_hoehe = 0.25
        self.segments.append(segments.Segment([
            (-breite/2, hoehe/2),
            (0, hoehe/2 - dreieck_hoehe),
            (breite/2, hoehe/2)
        ]))
        
        # Anschlüsse (einpolige Darstellung)
        self.anchors['minus'] = (0, -hoehe/2)
        self.anchors['start'] = (0, -hoehe/2)
        self.anchors['end'] = (0, -hoehe/2)
        
        # Standard-Ankerpunkte (N, S, E, W)
        self.anchors['W'] = (-breite/2, 0)  # West (links)
        self.anchors['E'] = (breite/2, 0)   # East (rechts)
        self.anchors['N'] = (0, hoehe/2)    # North (oben)
        self.anchors['S'] = (0, -hoehe/2)   # South (unten)
        
        # PE-Anker (entspricht W-Anker)
        self.anchors['PE'] = (-breite/2, 0)
        
        # Debug: Anchors anzeigen
        if debug:
            for name, pos in [('minus', (0, -hoehe/2)), ('start', (0, -hoehe/2)), 
                             ('end', (0, -hoehe/2)), ('W/PE', (-breite/2, 0)),
                             ('E', (breite/2, 0)), ('N', (0, hoehe/2)), ('S', (0, -hoehe/2))]:
                self.segments.append(segments.SegmentCircle(pos, 0.05, fill='red'))
                self.segments.append(segments.SegmentText(
                    (pos[0] - 0.15, pos[1]), name, fontsize=6, align=('right', 'center'), color='red'
                ))
        
        # Beschriftung
        if bezeichnung:
            self.segments.append(segments.SegmentText(
                (breite/2 + 0.1, 0), bezeichnung, fontsize=10, align=('left', 'center')
            ))
        
        if leistung:
            # Leistung kann Zahl oder String sein
            if isinstance(leistung, (int, float)):
                leistung_text = f"{leistung}Wp"
            else:
                leistung_text = str(leistung)
            
            label_y = -0.3 if bezeichnung else 0
            self.segments.append(segments.SegmentText(
                (breite/2 + 0.1, label_y), leistung_text, fontsize=8, align=('left', 'center')
            ))


class PVString(Element):
    """
    PV-String (mehrere Module in Reihe).
    
    Darstellung als mehrere verkettete PV-Symbole (Rechtecke mit Dreieck).
    
    Args:
        anzahl_module: Anzahl der Module im String
        leistung_pro_modul_wp: Leistung pro Modul in Wp
        bezeichnung: Optionale Bezeichnung (z.B. "String 1")
    """
    
    def __init__(self, anzahl_module: int = 10, leistung_pro_modul_wp: int = 400, 
                 bezeichnung: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Drei Rechtecke mit Dreiecken übereinander (symbolisch für mehrere Module)
        breite = 0.6
        modul_hoehe = 0.8
        abstand = 0.15
        dreieck_hoehe = 0.2
        
        y_start = 0
        
        for i in range(3):
            y_pos = y_start + i * (modul_hoehe + abstand)
            
            # Rechteck
            self.segments.append(segments.Segment([
                (-breite/2, y_pos),
                (breite/2, y_pos),
                (breite/2, y_pos + modul_hoehe),
                (-breite/2, y_pos + modul_hoehe),
                (-breite/2, y_pos)
            ]))
            
            # Dreieckspitze
            self.segments.append(segments.Segment([
                (-breite/2, y_pos + modul_hoehe),
                (0, y_pos + modul_hoehe - dreieck_hoehe),
                (breite/2, y_pos + modul_hoehe)
            ]))
            
            # Verbindungslinie zum nächsten Modul
            if i < 2:
                self.segments.append(segments.Segment([
                    (0, y_pos + modul_hoehe),
                    (0, y_pos + modul_hoehe + abstand)
                ]))
        
        gesamt_hoehe = 3 * modul_hoehe + 2 * abstand
        
        # Anschlüsse am Anfang und Ende
        self.anchors['center'] = (0, y_start + gesamt_hoehe/2)
        self.anchors['minus'] = (0, y_start)
        self.anchors['plus'] = (0, y_start + gesamt_hoehe)
        self.anchors['start'] = (0, y_start)
        self.anchors['end'] = (0, y_start + gesamt_hoehe)
        
        # Beschriftung
        gesamtleistung_kwp = (anzahl_module * leistung_pro_modul_wp) / 1000
        
        if bezeichnung:
            self.segments.append(segments.SegmentText(
                (breite/2 + 0.1, y_start + gesamt_hoehe/2 + 0.3), 
                bezeichnung, fontsize=10, align=('left', 'center')
            ))
        
        self.segments.append(segments.SegmentText(
            (breite/2 + 0.1, y_start + gesamt_hoehe/2 - 0.2), 
            f"{anzahl_module}×{leistung_pro_modul_wp}Wp",
            fontsize=8, align=('left', 'center')
        ))
        
        self.segments.append(segments.SegmentText(
            (breite/2 + 0.1, y_start + gesamt_hoehe/2 - 0.5), 
            f"({gesamtleistung_kwp:.1f}kWp)",
            fontsize=8, align=('left', 'center')
        ))


if __name__ == "__main__":
    """Visualisierung der PV-Modul-Komponenten."""
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=12)
    
    # Titel
    d += elm.Label().at((3, 6)).label("PV-Komponenten (DIN EN 60617)", fontsize=16)
    
    # Einzelnes PV-Modul ohne Leistung
    d += PVModul(bezeichnung="PV1").at((1, 4))
    
    # Einzelnes PV-Modul mit Leistung als Zahl
    d += PVModul(leistung=400, bezeichnung="PV2").at((3, 4))
    
    # Einzelnes PV-Modul mit Leistung als Text
    d += PVModul(leistung="12x455Wp", bezeichnung="PV3").at((5, 4))
    
    # PV-Modul mit Debug-Anchors
    d += PVModul(leistung=400, bezeichnung="PV4", debug=True).at((1, 1.5))
    
    # PV-String
    d += PVString(anzahl_module=3, leistung_pro_modul_wp=400, bezeichnung="String 1").at((7.5, 2.5))
    
    # Dokumentation rechts
    doc_x = 9
    doc_y_start = 4
    d += elm.Label().at((doc_x, doc_y_start)).label("Komponenten:", fontsize=11, loc='right')
    d += elm.Label().at((doc_x+0.2, doc_y_start-0.4)).label("• PVModul - einzelnes Modul", fontsize=9, loc='right')
    d += elm.Label().at((doc_x+0.3, doc_y_start-0.7)).label("- Rechteck mit Dreieckspitze", fontsize=8, loc='right')
    d += elm.Label().at((doc_x+0.3, doc_y_start-1.0)).label("- Plus/Minus vertikal", fontsize=8, loc='right')
    d += elm.Label().at((doc_x+0.2, doc_y_start-1.4)).label("• PVString - mehrere Module", fontsize=9, loc='right')
    d += elm.Label().at((doc_x+0.3, doc_y_start-1.7)).label("- 3 verkettete Module", fontsize=8, loc='right')
    d += elm.Label().at((doc_x+0.3, doc_y_start-2.0)).label("- Gesamtleistung in kWp", fontsize=8, loc='right')
    
    # Speichern und anzeigen
    from pathlib import Path
    output_path_png = Path("output/komponenten_pv_module.png")
    output_path_svg = Path("output/komponenten_pv_module.svg")
    output_path_png.parent.mkdir(parents=True, exist_ok=True)
    d.save(str(output_path_png))
    d.save(str(output_path_svg))
    print(f"PV-Modul-Komponenten gespeichert: {output_path_png} und {output_path_svg}")
