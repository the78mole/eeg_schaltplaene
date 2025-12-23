"""Schmelzsicherungen nach DIN EN 60617.

NH-Sicherungen, Schraubsicherungen und andere Schmelzsicherungen.
"""

import schemdraw
import schemdraw.elements as elm
from schemdraw import segments
from enum import Enum

# Versuche relative Imports, falle zurück auf absolute (für direkte Ausführung)
try:
    from .enums import ComponentFlow
except ImportError:
    from enums import ComponentFlow


class Schmelzsicherung(elm.Element):
    """
    Schmelzsicherung nach DIN EN 60617.
    
    Dargestellt als Rechteck mit durchgehender Linie.
    Verwendbar für NH-Sicherungen, Schraubsicherungen (D-System), etc.
    
    Args:
        bezeichnung: Bezeichner der Sicherung (z.B. "F1", "F2")
        nennstrom_a: Nennstrom in Ampere (z.B. 16, 25, 63)
        kennlinie: Kennlinie der Sicherung (z.B. "gG", "aM", "gL")
        typ: Typ der Sicherung (z.B. "NH00", "NH1", "D02", "C")
        flow: Ausrichtung (FLOW_V für vertikal, FLOW_H für horizontal)
        hak: Fügt Hausanschlusskasten-Rahmen um die Sicherung hinzu
        debug: Zeigt Ankerpunkte zur Fehlersuche
    """
    
    def __init__(self, 
                 bezeichnung: str = "F1",
                 nennstrom_a: int = 16,
                 kennlinie: str = "gG",
                 typ: str = "NH00",
                 flow: ComponentFlow = ComponentFlow.FLOW_V,
                 hak: bool = False,
                 debug: bool = False,
                 **kwargs):
        
        # Theta-Fix: Verhindere automatische Rotation
        kwargs['theta'] = 0
        
        super().__init__(**kwargs)
        
        # Geometrische Parameter
        rechteck_breite = 0.4
        rechteck_hoehe = 0.6
        leitungs_laenge = 0.6
        
        if flow == ComponentFlow.FLOW_V:
            # Vertikale Ausrichtung: Strom fließt von unten nach oben
            
            # Untere Zuleitung
            self.segments.append(segments.Segment([
                (0, -leitungs_laenge),
                (0, -rechteck_hoehe/2)
            ]))
            
            # Rechteck
            self.segments.append(segments.Segment([
                (-rechteck_breite/2, -rechteck_hoehe/2),
                (rechteck_breite/2, -rechteck_hoehe/2),
                (rechteck_breite/2, rechteck_hoehe/2),
                (-rechteck_breite/2, rechteck_hoehe/2),
                (-rechteck_breite/2, -rechteck_hoehe/2)
            ]))
            
            # Durchgehende Linie (Schmelzleiter)
            self.segments.append(segments.Segment([
                (0, -rechteck_hoehe/2),
                (0, rechteck_hoehe/2)
            ]))
            
            # Obere Ableitung
            self.segments.append(segments.Segment([
                (0, rechteck_hoehe/2),
                (0, leitungs_laenge)
            ]))
            
            # HAK-Rahmen (Hausanschlusskasten)
            if hak:
                hak_breite = rechteck_breite + 0.4
                hak_hoehe = rechteck_hoehe + 0.4
                self.segments.append(segments.Segment([
                    (-hak_breite/2, -hak_hoehe/2),
                    (hak_breite/2, -hak_hoehe/2),
                    (hak_breite/2, hak_hoehe/2),
                    (-hak_breite/2, hak_hoehe/2),
                    (-hak_breite/2, -hak_hoehe/2)
                ], ls='--'))
                # HAK-Beschriftung links
                self.segments.append(segments.SegmentText(
                    (-hak_breite/2 - 0.15, 0), "HAK", fontsize=8, 
                    align=('right', 'center'), rotation=90
                ))
            
            self.anchors['start'] = (0, -leitungs_laenge)
            self.anchors['end'] = (0, leitungs_laenge)
            
            # Debug: Anchors anzeigen
            if debug:
                for name, pos in [('start', (0, -leitungs_laenge)), 
                                 ('end', (0, leitungs_laenge))]:
                    self.segments.append(segments.SegmentCircle(pos, 0.05, fill='red'))
                    self.segments.append(segments.SegmentText(
                        (pos[0] + 0.15, pos[1]), name, fontsize=6, align=('left', 'center'), color='red'
                    ))
            
            # Beschriftung rechts
            if bezeichnung:
                self.segments.append(segments.SegmentText(
                    (0.6, 0.2), bezeichnung, fontsize=10, align=('left', 'center')
                ))
            
            # Technische Daten
            y_offset = -0.05 if bezeichnung else 0.2
            if nennstrom_a:
                self.segments.append(segments.SegmentText(
                    (0.6, y_offset), f"{nennstrom_a}A", fontsize=8, align=('left', 'center')
                ))
                y_offset -= 0.25
            
            if kennlinie:
                self.segments.append(segments.SegmentText(
                    (0.6, y_offset), kennlinie, fontsize=8, align=('left', 'center')
                ))
                y_offset -= 0.25
            
            if typ:
                self.segments.append(segments.SegmentText(
                    (0.6, y_offset), typ, fontsize=7, align=('left', 'center')
                ))
        
        else:  # FLOW_H
            # Horizontale Ausrichtung: Strom fließt von links nach rechts
            
            # Linke Zuleitung
            self.segments.append(segments.Segment([
                (-leitungs_laenge, 0),
                (-rechteck_hoehe/2, 0)
            ]))
            
            # Rechteck (90° gedreht: X-Achse nutzt rechteck_hoehe, Y-Achse nutzt rechteck_breite)
            self.segments.append(segments.Segment([
                (-rechteck_hoehe/2, -rechteck_breite/2),
                (-rechteck_hoehe/2, rechteck_breite/2),
                (rechteck_hoehe/2, rechteck_breite/2),
                (rechteck_hoehe/2, -rechteck_breite/2),
                (-rechteck_hoehe/2, -rechteck_breite/2)
            ]))
            
            # Durchgehende Linie (Schmelzleiter)
            self.segments.append(segments.Segment([
                (-rechteck_hoehe/2, 0),
                (rechteck_hoehe/2, 0)
            ]))
            
            # Rechte Ableitung
            self.segments.append(segments.Segment([
                (rechteck_hoehe/2, 0),
                (leitungs_laenge, 0)
            ]))
            
            # HAK-Rahmen (Hausanschlusskasten)
            if hak:
                hak_breite = rechteck_hoehe + 0.4  # In X-Richtung
                hak_hoehe = rechteck_breite + 0.4  # In Y-Richtung
                self.segments.append(segments.Segment([
                    (-hak_breite/2, -hak_hoehe/2),
                    (hak_breite/2, -hak_hoehe/2),
                    (hak_breite/2, hak_hoehe/2),
                    (-hak_breite/2, hak_hoehe/2),
                    (-hak_breite/2, -hak_hoehe/2)
                ], ls='--'))
                # HAK-Beschriftung oben
                self.segments.append(segments.SegmentText(
                    (0, hak_hoehe/2 + 0.15), "HAK", fontsize=8, 
                    align=('center', 'bottom')
                ))
            
            self.anchors['start'] = (-leitungs_laenge, 0)
            self.anchors['end'] = (leitungs_laenge, 0)
            
            # Debug: Anchors anzeigen
            if debug:
                for name, pos in [('start', (-leitungs_laenge, 0)), 
                                 ('end', (leitungs_laenge, 0))]:
                    self.segments.append(segments.SegmentCircle(pos, 0.05, fill='red'))
                    self.segments.append(segments.SegmentText(
                        (pos[0], pos[1] - 0.15), name, fontsize=6, align=('center', 'top'), color='red'
                    ))
            
            # Beschriftung unten (mit mehr Abstand wenn HAK)
            y_offset = -0.55 if hak else -0.35
            if bezeichnung:
                self.segments.append(segments.SegmentText(
                    (0, y_offset), bezeichnung, fontsize=10, align=('center', 'top')
                ))
                y_offset -= 0.25
            
            # Technische Daten
            if nennstrom_a:
                self.segments.append(segments.SegmentText(
                    (0, y_offset), f"{nennstrom_a}A", fontsize=7, align=('center', 'top')
                ))
                y_offset -= 0.2
            
            if kennlinie:
                self.segments.append(segments.SegmentText(
                    (0, y_offset), kennlinie, fontsize=7, align=('center', 'top')
                ))
                y_offset -= 0.2
            
            if typ:
                self.segments.append(segments.SegmentText(
                    (0, y_offset), typ, fontsize=6, align=('center', 'top')
                ))


if __name__ == "__main__":
    """Visualisierung der Schmelzsicherungen."""
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=12)
    
    # Titel
    d += elm.Label().at((4, 5.5)).label("Schmelzsicherungen (DIN EN 60617)", fontsize=16)
    
    # Vertikale Ausrichtung
    d += elm.Label().at((0.5, 4.5)).label("Vertikale Ausrichtung:", fontsize=12, halign='left')
    
    # NH-Sicherung ohne HAK
    d += Schmelzsicherung(
        bezeichnung="F1",
        nennstrom_a=63,
        kennlinie="gG",
        typ="NH00",
        flow=ComponentFlow.FLOW_V,
        hak=False,
        debug=True
    ).at((1, 3))
    d += elm.Label().at((1, 1)).label("NH-Sicherung\n63A gG NH00", fontsize=9, halign='center')
    
    # Schraubsicherung
    d += Schmelzsicherung(
        bezeichnung="F2",
        nennstrom_a=16,
        kennlinie="gG",
        typ="D02",
        flow=ComponentFlow.FLOW_V,
        debug=True
    ).at((3, 3))
    d += elm.Label().at((3, 1)).label("Schraubsicherung\n16A gG D02", fontsize=9, halign='center')
    
    # NH-Sicherung mit HAK
    d += Schmelzsicherung(
        bezeichnung="F3",
        nennstrom_a=63,
        kennlinie="gG",
        typ="NH00",
        flow=ComponentFlow.FLOW_V,
        hak=True,
        debug=True
    ).at((5, 3))
    d += elm.Label().at((5, 1)).label("NH-Sicherung\nim HAK", fontsize=9, halign='center')
    
    # Horizontale Ausrichtung
    d += elm.Label().at((0.5, -0.5)).label("Horizontale Ausrichtung:", fontsize=12, halign='left')
    
    # NH-Sicherung horizontal
    d += Schmelzsicherung(
        bezeichnung="F4",
        nennstrom_a=125,
        kennlinie="gG",
        typ="NH1",
        flow=ComponentFlow.FLOW_H,
        debug=True
    ).at((1, -2))
    d += elm.Label().at((1, -3.5)).label("NH-Sicherung 125A gG NH1", fontsize=9, halign='center')
    
    # NH-Sicherung horizontal mit HAK
    d += Schmelzsicherung(
        bezeichnung="F5",
        nennstrom_a=63,
        kennlinie="gG",
        typ="NH00",
        flow=ComponentFlow.FLOW_H,
        hak=True,
        debug=True
    ).at((5, -2))
    d += elm.Label().at((5, -3.5)).label("NH-Sicherung im HAK (horizontal)", fontsize=9, halign='center')
    
    # Speichern
    d.save('output/komponenten_schmelzsicherung.png')
    d.save('output/komponenten_schmelzsicherung.svg')
    print("Schmelzsicherung gespeichert: output/komponenten_schmelzsicherung.png und output/komponenten_schmelzsicherung.svg")
