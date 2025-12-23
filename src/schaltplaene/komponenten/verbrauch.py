"""Verbrauch/Haus-Symbol für elektrische Schaltpläne.

Symbolisiert den Verbrauch oder die Hausinstallation.
"""

import schemdraw
import schemdraw.elements as elm
from schemdraw import segments


class Verbrauch(elm.Element):
    """
    Verbrauch/Haus-Symbol für Schaltpläne.
    
    Dargestellt als Rechteck mit Haus-Symbol (Gebäude + Dach).
    
    Args:
        bezeichnung: Bezeichner (z.B. "Haus", "Verbrauch", "Last")
        leistung_kw: Erwartete/maximale Leistung in kW (optional)
        label_loc: Position der Beschriftung ('N', 'S', 'E', 'W', 'NE', 'NO', 'NW', 'SE', 'SO', 'SW')
        debug: Zeigt Ankerpunkte zur Fehlersuche
    """
    
    def __init__(self, 
                 bezeichnung: str = "Haus",
                 leistung_kw: float = 0,
                 label_loc: str = 'N',
                 debug: bool = False,
                 **kwargs):
        
        super().__init__(**kwargs)
        
        # Geometrische Parameter
        breite = 1.0
        hoehe = 1.0
        
        # Rechteck (Gehäuse)
        self.segments.append(segments.Segment([
            (-breite/2, -hoehe/2),
            (breite/2, -hoehe/2),
            (breite/2, hoehe/2),
            (-breite/2, hoehe/2),
            (-breite/2, -hoehe/2)
        ]))
        
        # Haus-Symbol in der Mitte
        # Gebäude (Rechteck)
        haus_breite = 0.4
        haus_hoehe = 0.3
        haus_y = -0.05
        
        self.segments.append(segments.Segment([
            (-haus_breite/2, haus_y - haus_hoehe/2),
            (haus_breite/2, haus_y - haus_hoehe/2),
            (haus_breite/2, haus_y + haus_hoehe/2),
            (-haus_breite/2, haus_y + haus_hoehe/2),
            (-haus_breite/2, haus_y - haus_hoehe/2)
        ]))
        
        # Dach (Dreieck)
        dach_hoehe = 0.25
        dach_y_start = haus_y + haus_hoehe/2
        
        self.segments.append(segments.Segment([
            (-haus_breite/2, dach_y_start),
            (0, dach_y_start + dach_hoehe),
            (haus_breite/2, dach_y_start),
            (-haus_breite/2, dach_y_start)
        ]))
        
        # Ankerpunkte auf allen vier Seiten
        self.anchors['W'] = (-breite/2, 0)  # West (links)
        self.anchors['E'] = (breite/2, 0)   # East (rechts)
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
        
        # Technische Daten an gegenüberliegender Seite
        if leistung_kw:
            tech_positions = {
                'N': ((0, -hoehe/2 - 0.25), ('center', 'top')),
                'S': ((0, hoehe/2 + 0.25), ('center', 'bottom')),
                'E': ((-breite/2 - 0.25, 0), ('right', 'center')),
                'W': ((breite/2 + 0.25, 0), ('left', 'center')),
                'NE': ((-breite/2 - 0.25, -hoehe/2 - 0.25), ('right', 'top')),
                'NO': ((-breite/2 - 0.25, -hoehe/2 - 0.25), ('right', 'top')),
                'NW': ((breite/2 + 0.25, -hoehe/2 - 0.25), ('left', 'top')),
                'SE': ((-breite/2 - 0.25, hoehe/2 + 0.25), ('right', 'bottom')),
                'SO': ((-breite/2 - 0.25, hoehe/2 + 0.25), ('right', 'bottom')),
                'SW': ((breite/2 + 0.25, hoehe/2 + 0.25), ('left', 'bottom'))
            }
            pos, align = tech_positions.get(label_loc.upper(), tech_positions['N'])
            self.segments.append(segments.SegmentText(
                pos, f"{leistung_kw}kW", fontsize=8, align=align
            ))


if __name__ == "__main__":
    """Visualisierung der Verbrauch/Haus-Symbole."""
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=12)
    
    # Titel
    d += elm.Label().at((3, 3.5)).label("Verbrauch / Haus-Symbol", fontsize=16)
    
    # Einfaches Haus
    d += Verbrauch(
        bezeichnung="Haus",
        debug=True
    ).at((1.5, 1.5))
    d += elm.Label().at((1.5, -0.2)).label("Ohne Leistungsangabe", fontsize=9, halign='center')
    
    # Haus mit Leistung
    d += Verbrauch(
        bezeichnung="Verbrauch",
        leistung_kw=15.0,
        debug=True
    ).at((4.5, 1.5))
    d += elm.Label().at((4.5, -0.2)).label("Mit Leistungsangabe", fontsize=9, halign='center')
    
    # Last
    d += Verbrauch(
        bezeichnung="Last",
        leistung_kw=10.0,
        debug=True
    ).at((3, -1.5))
    d += elm.Label().at((3, -3.2)).label("Alternative Bezeichnung", fontsize=9, halign='center')
    
    # Speichern
    d.save('output/komponenten_verbrauch.png')
    d.save('output/komponenten_verbrauch.svg')
    print("Verbrauch/Haus gespeichert: output/komponenten_verbrauch.png und output/komponenten_verbrauch.svg")
