"""PE-Leitung (Schutzleiter) nach DIN-Norm grün-gelb.

Darstellung einer Schutzleiter-Verbindung in grün-gelber Kennzeichnung.
"""

import schemdraw
import schemdraw.elements as elm
from schemdraw import segments


class PELine(elm.Element):
    """
    PE-Leitung (Schutzleiter) in grün-gelber Darstellung.
    
    Zeichnet eine Linie mit gelber Grundfarbe und grüner gestrichelter
    Überlagerung zur Kennzeichnung von Schutzleitern (PE).
    
    Args:
        to_pos: Zielposition als Tuple (x, y) - relativ zum Startpunkt
        **kwargs: Weitere Argumente für Element (z.B. at() für Startposition)
    """
    
    def __init__(self, to_pos: tuple = (1, 0), **kwargs):
        # Theta-Fix: Verhindere automatische Rotation
        kwargs['theta'] = 0
        
        super().__init__(**kwargs)
        
        # Gelbe Grundlinie (durchgezogen)
        self.segments.append(segments.Segment([
            (0, 0),
            to_pos
        ], color='gold', lw=2))
        
        # Grüne gestrichelte Linie darüber
        self.segments.append(segments.Segment([
            (0, 0),
            to_pos
        ], color='green', lw=2, ls='--'))
        
        # Ankerpunkte
        self.anchors['start'] = (0, 0)
        self.anchors['end'] = to_pos


def pe_line_between(drawing, start_anchor, end_anchor):
    """
    Hilfsfunktion zum Zeichnen einer PE-Leitung zwischen zwei Ankern.
    
    Args:
        drawing: Schemdraw Drawing-Objekt
        start_anchor: Start-Ankerpunkt (z.B. komponente.absanchors['N'])
        end_anchor: End-Ankerpunkt (z.B. andere_komponente.absanchors['start'])
    
    Returns:
        Das Drawing-Objekt für Method-Chaining
    """
    dx = end_anchor.x - start_anchor.x
    dy = end_anchor.y - start_anchor.y
    
    drawing += PELine(to_pos=(dx, dy)).at(start_anchor)
    return drawing


if __name__ == "__main__":
    """Visualisierung der PE-Leitungen."""
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=12)
    
    # Titel
    d += elm.Label().at((2, 2.5)).label("PE-Leitung (Schutzleiter)", fontsize=16)
    
    # Horizontale PE-Leitung
    d += elm.Dot().at((0.5, 1.5)).label("Start", loc='left')
    d += PELine(to_pos=(2, 0)).at((0.5, 1.5))
    d += elm.Dot().at((2.5, 1.5)).label("Ende", loc='right')
    d += elm.Label().at((1.5, 1.2)).label("Horizontal", fontsize=9, halign='center')
    
    # Vertikale PE-Leitung
    d += elm.Dot().at((0.5, 0.5)).label("Start", loc='bottom')
    d += PELine(to_pos=(0, -1.5)).at((0.5, 0.5))
    d += elm.Dot().at((0.5, -1)).label("Ende", loc='top')
    d += elm.Label().at((0.8, -0.25)).label("Vertikal", fontsize=9, halign='left')
    
    # Diagonale PE-Leitung
    d += elm.Dot().at((1.5, 0.5)).label("Start", loc='bottom')
    d += PELine(to_pos=(1.5, -1.2)).at((1.5, 0.5))
    d += elm.Dot().at((3, -0.7)).label("Ende", loc='right')
    d += elm.Label().at((2.5, -0.2)).label("Diagonal", fontsize=9, halign='center')
    
    # Speichern
    d.save('output/komponenten_pe_line.png')
    d.save('output/komponenten_pe_line.svg')
    print("PE-Leitung gespeichert: output/komponenten_pe_line.png und output/komponenten_pe_line.svg")
