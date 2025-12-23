"""Wechselrichter nach DIN EN 60617.

Wandelt Gleichstrom (DC) in Wechselstrom (AC) um.
"""

import math
import schemdraw
import schemdraw.elements as elm
from schemdraw import segments


class Wechselrichter(elm.Element):
    """
    Wechselrichter nach DIN EN 60617.
    
    Dargestellt als Rechteck mit Diagonale:
    - Links: DC-Symbol (= mit gestrichelter zweiter Linie)
    - Rechts: AC-Symbol (doppelte ~)
    
    Args:
        bezeichnung: Bezeichner des Wechselrichters (z.B. "WR1", "WR2")
        leistung_kw: Nennleistung in kW (z.B. 10, 15)
        hersteller: Hersteller/Typ des Wechselrichters (optional)
        flip_h: Horizontal spiegeln (DC/AC-Seiten tauschen)
        flip_v: Vertikal spiegeln (oben/unten tauschen)
        label_loc: Position der Beschriftung ('N', 'S', 'E', 'W', 'NE', 'NO', 'NW', 'SE', 'SO', 'SW')
        debug: Zeigt Ankerpunkte zur Fehlersuche
    """
    
    def __init__(self, 
                 bezeichnung: str = "WR1",
                 leistung_kw: float = 10.0,
                 hersteller: str = "",
                 flip_h: bool = False,
                 flip_v: bool = False,
                 label_loc: str = 'N',
                 debug: bool = False,
                 **kwargs):
        
        super().__init__(**kwargs)
        
        # Geometrische Parameter
        breite = 1.0
        hoehe = 1.0
        
        # Spiegelfaktoren
        fx = -1 if flip_h else 1
        fy = -1 if flip_v else 1
        
        # Rechteck
        self.segments.append(segments.Segment([
            (fx * -breite/2, fy * -hoehe/2),
            (fx * breite/2, fy * -hoehe/2),
            (fx * breite/2, fy * hoehe/2),
            (fx * -breite/2, fy * hoehe/2),
            (fx * -breite/2, fy * -hoehe/2)
        ]))
        
        # Diagonale von links-unten nach rechts-oben
        self.segments.append(segments.Segment([
            (fx * -breite/2, fy * -hoehe/2),
            (fx * breite/2, fy * hoehe/2)
        ]))
        
        # DC-Symbol im linken oberen Dreieck (=)
        dc_x = -breite/4
        dc_y = hoehe/3.5
        dc_laenge = 0.25
        dc_abstand = 0.08
        
        # Durchgezogene Linie (oben)
        self.segments.append(segments.Segment([
            (fx * (dc_x - dc_laenge/2), fy * (dc_y + dc_abstand/2)),
            (fx * (dc_x + dc_laenge/2), fy * (dc_y + dc_abstand/2))
        ]))
        
        # Gestrichelte Linie (unten) - manuell gezeichnet: 1/3 Strich, 1/3 Lücke, 1/3 Strich
        dc_strich_laenge = dc_laenge / 3
        dc_luecke = dc_laenge / 3
        # Linker Strich
        self.segments.append(segments.Segment([
            (fx * (dc_x - dc_laenge/2), fy * (dc_y - dc_abstand/2)),
            (fx * (dc_x - dc_laenge/2 + dc_strich_laenge), fy * (dc_y - dc_abstand/2))
        ]))
        # Rechter Strich
        self.segments.append(segments.Segment([
            (fx * (dc_x + dc_laenge/2 - dc_strich_laenge), fy * (dc_y - dc_abstand/2)),
            (fx * (dc_x + dc_laenge/2), fy * (dc_y - dc_abstand/2))
        ]))
        
        # AC-Symbol im rechten unteren Dreieck (~~)
        ac_x = breite/4
        ac_y = -hoehe/3.5
        ac_laenge = 0.3
        ac_abstand = 0.1
        
        # Obere Welle (~)
        punkte_oben = []
        schritte = 20
        for i in range(schritte + 1):
            t = i / schritte
            x = ac_x - ac_laenge/2 + t * ac_laenge
            y = ac_y + ac_abstand/2 + 0.06 * math.sin(t * 2 * math.pi)
            punkte_oben.append((fx * x, fy * y))
        self.segments.append(segments.Segment(punkte_oben))
        
        # Untere Welle (~)
        punkte_unten = []
        for i in range(schritte + 1):
            t = i / schritte
            x = ac_x - ac_laenge/2 + t * ac_laenge
            y = ac_y - ac_abstand/2 + 0.06 * math.sin(t * 2 * math.pi)
            punkte_unten.append((fx * x, fy * y))
        self.segments.append(segments.Segment(punkte_unten))
        
        # Ankerpunkte auf allen vier Seiten (unabhängig von Spiegelung)
        self.anchors['W'] = (-breite/2, 0)  # West (links, DC-Seite ohne Spiegelung)
        self.anchors['E'] = (breite/2, 0)   # East (rechts, AC-Seite ohne Spiegelung)
        self.anchors['N'] = (0, hoehe/2)    # North (oben)
        self.anchors['S'] = (0, -hoehe/2)   # South (unten)
        
        # Debug: Anchors anzeigen
        if debug:
            for name, pos in [('W', (-breite/2, 0)), 
                             ('E', (breite/2, 0)),
                             ('N', (0, hoehe/2)),
                             ('S', (0, -hoehe/2))]:
                self.segments.append(segments.SegmentCircle(pos, 0.05, fill='red'))
                self.segments.append(segments.SegmentText(
                    (pos[0] * 1.2, pos[1] * 1.2), name, fontsize=6, align=('center', 'center'), color='red'
                ))
        
        # Beschriftung an angegebener Position
        if bezeichnung:
            label_positions = {
                'N': ((0, hoehe/2 + 0.25), ('center', 'bottom')),
                'S': ((0, -hoehe/2 - 0.25), ('center', 'top')),
                'E': ((breite/2 + 0.25, 0), ('left', 'center')),
                'W': ((-breite/2 - 0.25, 0), ('right', 'center')),
                'NE': ((breite/2 + 0.25, hoehe/2 + 0.25), ('left', 'bottom')),
                'NO': ((breite/2 + 0.25, hoehe/2 + 0.25), ('left', 'bottom')),
                'NW': ((-breite/2 - 0.25, hoehe/2 + 0.25), ('right', 'bottom')),
                'SE': ((breite/2 + 0.25, -hoehe/2 - 0.25), ('left', 'top')),
                'SO': ((breite/2 + 0.25, -hoehe/2 - 0.25), ('left', 'top')),
                'SW': ((-breite/2 - 0.25, -hoehe/2 - 0.25), ('right', 'top'))
            }
            pos, align = label_positions.get(label_loc.upper(), label_positions['N'])
            self.segments.append(segments.SegmentText(
                pos, bezeichnung, fontsize=10, align=align
            ))
        
        # Technische Daten direkt unter dem Bezeichner
        if label_loc.upper() in ['N', 'S', 'NE', 'NO', 'NW', 'SE', 'SO', 'SW']:
            # Vertikale Anordnung: Leistung und Hersteller unter dem Bezeichner
            y_offset = -0.2 if label_loc.upper() in ['N', 'NE', 'NO', 'NW'] else 0.2
            current_pos = list(label_positions.get(label_loc.upper(), label_positions['N'])[0])
            current_align = label_positions.get(label_loc.upper(), label_positions['N'])[1]
            
            if leistung_kw:
                current_pos[1] += y_offset
                self.segments.append(segments.SegmentText(
                    tuple(current_pos), f"{leistung_kw}kW", fontsize=8, align=current_align
                ))
            if hersteller:
                current_pos[1] += y_offset
                self.segments.append(segments.SegmentText(
                    tuple(current_pos), hersteller, fontsize=7, align=current_align
                ))
        else:  # E oder W - horizontal nebeneinander oder vertikal gestapelt
            pos, align = label_positions.get(label_loc.upper(), label_positions['E'])
            y_offset = -0.2
            current_pos = list(pos)
            
            if leistung_kw:
                current_pos[1] += y_offset
                self.segments.append(segments.SegmentText(
                    tuple(current_pos), f"{leistung_kw}kW", fontsize=8, align=align
                ))
            if hersteller:
                current_pos[1] += y_offset
                self.segments.append(segments.SegmentText(
                    tuple(current_pos), hersteller, fontsize=7, align=align
                ))


if __name__ == "__main__":
    """Visualisierung der Wechselrichter."""
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=12)
    
    # Titel
    d += elm.Label().at((3, 3.5)).label("Wechselrichter (DIN EN 60617)", fontsize=16)
    
    # Standard-Wechselrichter
    d += Wechselrichter(
        bezeichnung="WR1",
        leistung_kw=10.0,
        hersteller="",
        debug=True
    ).at((1.5, 2))
    d += elm.Label().at((1.5, 0.5)).label("Standard", fontsize=9, halign='center')
    
    # Horizontal gespiegelt
    d += Wechselrichter(
        bezeichnung="WR2",
        leistung_kw=10.0,
        flip_h=True,
        debug=True
    ).at((4.5, 2))
    d += elm.Label().at((4.5, 0.5)).label("Horizontal gespiegelt", fontsize=9, halign='center')
    
    # Vertikal gespiegelt
    d += Wechselrichter(
        bezeichnung="WR3",
        leistung_kw=10.0,
        flip_v=True,
        debug=True
    ).at((1.5, -1))
    d += elm.Label().at((1.5, -2.5)).label("Vertikal gespiegelt", fontsize=9, halign='center')
    
    # Beides gespiegelt
    d += Wechselrichter(
        bezeichnung="WR4",
        leistung_kw=10.0,
        flip_h=True,
        flip_v=True,
        debug=True
    ).at((4.5, -1))
    d += elm.Label().at((4.5, -2.5)).label("Horizontal + Vertikal", fontsize=9, halign='center')
    
    # Speichern
    d.save('output/komponenten_wechselrichter.png')
    d.save('output/komponenten_wechselrichter.svg')
    print("Wechselrichter gespeichert: output/komponenten_wechselrichter.png und output/komponenten_wechselrichter.svg")
