"""Überspannungsschutz nach DIN EN 60617.

Ableiter zum Schutz vor Überspannungen.
"""

import schemdraw
import schemdraw.elements as elm
from schemdraw import segments

# Versuche relative Imports, falle zurück auf absolute (für direkte Ausführung)
try:
    from .enums import ComponentFlow
except ImportError:
    from enums import ComponentFlow


class Ueberspannungsschutz(elm.Element):
    """
    Überspannungsschutz (ÜSS) nach DIN EN 60617.
    
    Dargestellt als Rechteck mit gefülltem Dreieck (ähnlich PV-Modul).
    
    Args:
        bezeichnung: Bezeichner des ÜSS (z.B. "ÜSS1", "SPD1")
        schutzpegel_kv: Schutzpegel in kV (z.B. 1.5, 2.5)
        typ: Typ des ÜSS (z.B. "Typ 1", "Typ 2", "Typ 3")
        flow: Ausrichtung (FLOW_V für vertikal, FLOW_H für horizontal)
        debug: Zeigt Ankerpunkte zur Fehlersuche
    """
    
    def __init__(self, 
                 bezeichnung: str = "ÜSS1",
                 schutzpegel_kv: float = 1.5,
                 typ: str = "Typ 2",
                 flow: ComponentFlow = ComponentFlow.FLOW_V,
                 debug: bool = False,
                 **kwargs):
        
        # Theta-Fix: Verhindere automatische Rotation
        kwargs['theta'] = 0
        
        super().__init__(**kwargs)
        
        # Geometrische Parameter (kleiner als PV-Modul)
        rechteck_breite = 0.3
        rechteck_hoehe = 0.6
        dreieck_hoehe = 0.2
        anschluss_laenge = 0.3
        
        if flow == ComponentFlow.FLOW_V:
            # Vertikale Ausrichtung
            
            # Rechteck
            self.segments.append(segments.Segment([
                (-rechteck_breite/2, -rechteck_hoehe/2),
                (rechteck_breite/2, -rechteck_hoehe/2),
                (rechteck_breite/2, rechteck_hoehe/2),
                (-rechteck_breite/2, rechteck_hoehe/2),
                (-rechteck_breite/2, -rechteck_hoehe/2)
            ]))
            
            # Gefülltes Dreieck oben (Spitze zeigt nach innen/unten)
            dreieck_y_start = rechteck_hoehe/2
            self.segments.append(segments.Segment([
                (-rechteck_breite/2, dreieck_y_start),
                (0, dreieck_y_start - dreieck_hoehe),
                (rechteck_breite/2, dreieck_y_start),
                (-rechteck_breite/2, dreieck_y_start)
            ], fill='black'))
            
            # Oberer Anschluss (vom oberen Rechteckrand nach oben)
            self.segments.append(segments.Segment([
                (0, dreieck_y_start),
                (0, dreieck_y_start + anschluss_laenge)
            ]))
            
            # Unterer Anschluss (vom Rechteck nach unten)
            self.segments.append(segments.Segment([
                (0, -rechteck_hoehe/2),
                (0, -rechteck_hoehe/2 - anschluss_laenge)
            ]))
            
            # Ankerpunkte
            self.anchors['1'] = (0, -rechteck_hoehe/2 - anschluss_laenge)
            self.anchors['2'] = (0, dreieck_y_start + anschluss_laenge)
            self.anchors['start'] = (0, -rechteck_hoehe/2 - anschluss_laenge)
            self.anchors['end'] = (0, dreieck_y_start + anschluss_laenge)
            
            # Debug: Anchors anzeigen
            if debug:
                for name, pos in [('1', self.anchors['1']), 
                                 ('2', self.anchors['2'])]:
                    self.segments.append(segments.SegmentCircle(pos, 0.05, fill='red'))
                    self.segments.append(segments.SegmentText(
                        (pos[0] + 0.2, pos[1]), name, fontsize=6, align=('left', 'center'), color='red'
                    ))
            
            # Beschriftung rechts
            if bezeichnung:
                self.segments.append(segments.SegmentText(
                    (0.4, 0.2), bezeichnung, fontsize=10, align=('left', 'center')
                ))
            
            # Technische Daten
            y_offset = -0.05 if bezeichnung else 0.2
            if schutzpegel_kv:
                self.segments.append(segments.SegmentText(
                    (0.4, y_offset), f"{schutzpegel_kv}kV", fontsize=8, align=('left', 'center')
                ))
                y_offset -= 0.25
            
            if typ:
                self.segments.append(segments.SegmentText(
                    (0.4, y_offset), typ, fontsize=7, align=('left', 'center')
                ))
        
        else:  # FLOW_H
            # Horizontale Ausrichtung
            
            # Rechteck (90° gedreht: X-Achse nutzt rechteck_hoehe, Y-Achse nutzt rechteck_breite)
            self.segments.append(segments.Segment([
                (-rechteck_hoehe/2, -rechteck_breite/2),
                (rechteck_hoehe/2, -rechteck_breite/2),
                (rechteck_hoehe/2, rechteck_breite/2),
                (-rechteck_hoehe/2, rechteck_breite/2),
                (-rechteck_hoehe/2, -rechteck_breite/2)
            ]))
            
            # Gefülltes Dreieck rechts (Spitze zeigt nach innen/links)
            dreieck_x_start = rechteck_hoehe/2
            self.segments.append(segments.Segment([
                (dreieck_x_start, -rechteck_breite/2),
                (dreieck_x_start - dreieck_hoehe, 0),
                (dreieck_x_start, rechteck_breite/2),
                (dreieck_x_start, -rechteck_breite/2)
            ], fill='black'))
            
            # Rechter Anschluss (vom rechten Rechteckrand nach rechts)
            self.segments.append(segments.Segment([
                (dreieck_x_start, 0),
                (dreieck_x_start + anschluss_laenge, 0)
            ]))
            
            # Linker Anschluss (vom Rechteck nach links)
            self.segments.append(segments.Segment([
                (-rechteck_hoehe/2, 0),
                (-rechteck_hoehe/2 - anschluss_laenge, 0)
            ]))
            
            # Ankerpunkte
            self.anchors['1'] = (-rechteck_hoehe/2 - anschluss_laenge, 0)
            self.anchors['2'] = (dreieck_x_start + anschluss_laenge, 0)
            self.anchors['start'] = (-rechteck_hoehe/2 - anschluss_laenge, 0)
            self.anchors['end'] = (dreieck_x_start + anschluss_laenge, 0)
            
            # Debug: Anchors anzeigen
            if debug:
                for name, pos in [('1', self.anchors['1']), 
                                 ('2', self.anchors['2'])]:
                    self.segments.append(segments.SegmentCircle(pos, 0.05, fill='red'))
                    self.segments.append(segments.SegmentText(
                        (pos[0], pos[1] + 0.2), name, fontsize=6, align=('center', 'bottom'), color='red'
                    ))
            
            # Beschriftung unten
            y_offset = -0.35
            if bezeichnung:
                self.segments.append(segments.SegmentText(
                    (0, y_offset), bezeichnung, fontsize=10, align=('center', 'top')
                ))
                y_offset -= 0.25
            
            # Technische Daten
            if schutzpegel_kv:
                self.segments.append(segments.SegmentText(
                    (0, y_offset), f"{schutzpegel_kv}kV", fontsize=7, align=('center', 'top')
                ))
                y_offset -= 0.2
            
            if typ:
                self.segments.append(segments.SegmentText(
                    (0, y_offset), typ, fontsize=6, align=('center', 'top')
                ))


if __name__ == "__main__":
    """Visualisierung der Überspannungsschutz-Komponenten."""
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=12)
    
    # Titel
    d += elm.Label().at((3, 4.5)).label("Überspannungsschutz (DIN EN 60617)", fontsize=16)
    
    # Vertikale Ausrichtung
    d += elm.Label().at((0.5, 3.5)).label("Vertikale Ausrichtung:", fontsize=12, halign='left')
    
    # Typ 1 vertikal
    d += Ueberspannungsschutz(
        bezeichnung="ÜSS1",
        schutzpegel_kv=1.5,
        typ="Typ 1",
        flow=ComponentFlow.FLOW_V,
        debug=True
    ).at((1.5, 2))
    d += elm.Label().at((1.5, 0.2)).label("Typ 1", fontsize=9, halign='center')
    
    # Typ 2 vertikal
    d += Ueberspannungsschutz(
        bezeichnung="ÜSS2",
        schutzpegel_kv=1.5,
        typ="Typ 2",
        flow=ComponentFlow.FLOW_V,
        debug=True
    ).at((3, 2))
    d += elm.Label().at((3, 0.2)).label("Typ 2", fontsize=9, halign='center')
    
    # Typ 3 vertikal
    d += Ueberspannungsschutz(
        bezeichnung="ÜSS3",
        schutzpegel_kv=0.8,
        typ="Typ 3",
        flow=ComponentFlow.FLOW_V,
        debug=True
    ).at((4.5, 2))
    d += elm.Label().at((4.5, 0.2)).label("Typ 3", fontsize=9, halign='center')
    
    # Horizontale Ausrichtung
    d += elm.Label().at((0.5, -0.5)).label("Horizontale Ausrichtung:", fontsize=12, halign='left')
    
    # Horizontal
    d += Ueberspannungsschutz(
        bezeichnung="ÜSS4",
        schutzpegel_kv=1.5,
        typ="Typ 2",
        flow=ComponentFlow.FLOW_H,
        debug=True
    ).at((3, -2))
    d += elm.Label().at((3, -3.5)).label("Horizontal", fontsize=9, halign='center')
    
    # Speichern
    d.save('output/komponenten_ueberspannungsschutz.png')
    d.save('output/komponenten_ueberspannungsschutz.svg')
    print("Überspannungsschutz gespeichert: output/komponenten_ueberspannungsschutz.png und output/komponenten_ueberspannungsschutz.svg")
