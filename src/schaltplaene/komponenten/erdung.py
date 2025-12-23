"""Erdungssymbol / Potenzialausgleichschiene nach DIN EN 60617.

Symbolisiert die Erdung oder Potenzialausgleichschiene.
"""

import schemdraw
import schemdraw.elements as elm
from schemdraw import segments


class Erdung(elm.Element):
    """
    Erdungssymbol nach DIN EN 60617.
    
    Dargestellt als vertikale Linie mit drei horizontalen Linien
    (von oben nach unten kürzer werdend).
    
    Args:
        bezeichnung: Bezeichner (z.B. "PE", "PA", "Erdung")
        label_loc: Position der Beschriftung ('N', 'S', 'E', 'W', 'NE', 'NO', 'NW', 'SE', 'SO', 'SW')
        debug: Zeigt Ankerpunkte zur Fehlersuche
    """
    
    def __init__(self, 
                 bezeichnung: str = "PE",
                 label_loc: str = 'E',
                 debug: bool = False,
                 **kwargs):
        
        super().__init__(**kwargs)
        
        # Geometrische Parameter
        verbindung_laenge = 0.3  # Länge der Verbindungsleitung nach oben
        balken_abstand = 0.1    # Vertikaler Abstand zwischen Balken
        balken1_breite = 0.6    # Breitester Balken (oben)
        balken2_breite = 0.4    # Mittlerer Balken
        balken3_breite = 0.2    # Schmalster Balken (unten)
        
        # Vertikale Verbindungsleitung
        self.segments.append(segments.Segment([
            (0, 0),
            (0, -verbindung_laenge)
        ]))
        
        # Erster Balken (breitester, oben)
        balken1_y = -verbindung_laenge
        self.segments.append(segments.Segment([
            (-balken1_breite/2, balken1_y),
            (balken1_breite/2, balken1_y)
        ]))
        
        # Zweiter Balken (mittel)
        balken2_y = balken1_y - balken_abstand
        self.segments.append(segments.Segment([
            (-balken2_breite/2, balken2_y),
            (balken2_breite/2, balken2_y)
        ]))
        
        # Dritter Balken (schmalster, unten)
        balken3_y = balken2_y - balken_abstand
        self.segments.append(segments.Segment([
            (-balken3_breite/2, balken3_y),
            (balken3_breite/2, balken3_y)
        ]))
        
        # Ankerpunkt oben (Verbindungspunkt)
        self.anchors['N'] = (0, 0)  # Oben
        self.anchors['start'] = (0, 0)  # Alias für N
        
        # Debug: Anchors anzeigen
        if debug:
            self.segments.append(segments.SegmentCircle((0, 0), 0.05, fill='red'))
            self.segments.append(segments.SegmentText(
                (0.1, 0.1), 'N/start', fontsize=6, align=('left', 'center'), color='red'
            ))
        
        # Beschriftung an angegebener Position
        if bezeichnung:
            # Bounding box für Label-Positionierung
            gesamt_hoehe = verbindung_laenge + 2 * balken_abstand
            gesamt_breite = balken1_breite
            
            label_positions = {
                'N': ((0, 0.25), ('center', 'bottom')),
                'S': ((0, -(gesamt_hoehe + 0.25)), ('center', 'top')),
                'E': ((gesamt_breite/2 + 0.25, -gesamt_hoehe/2), ('left', 'center')),
                'W': ((-gesamt_breite/2 - 0.25, -gesamt_hoehe/2), ('right', 'center')),
                'NE': ((gesamt_breite/2 + 0.25, 0.25), ('left', 'bottom')),
                'NO': ((gesamt_breite/2 + 0.25, 0.25), ('left', 'bottom')),
                'NW': ((-gesamt_breite/2 - 0.25, 0.25), ('right', 'bottom')),
                'SE': ((gesamt_breite/2 + 0.25, -(gesamt_hoehe + 0.25)), ('left', 'top')),
                'SO': ((gesamt_breite/2 + 0.25, -(gesamt_hoehe + 0.25)), ('left', 'top')),
                'SW': ((-gesamt_breite/2 - 0.25, -(gesamt_hoehe + 0.25)), ('right', 'top'))
            }
            pos, align = label_positions.get(label_loc.upper(), label_positions['E'])
            self.segments.append(segments.SegmentText(
                pos, bezeichnung, fontsize=10, align=align
            ))


if __name__ == "__main__":
    """Visualisierung der Erdungssymbole."""
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=12)
    
    # Titel
    d += elm.Label().at((3, 2)).label("Erdungssymbol / Potenzialausgleich", fontsize=16)
    
    # Standard-Erdung
    d += Erdung(
        bezeichnung="PE",
        label_loc='E',
        debug=True
    ).at((1.5, 0.5))
    d += elm.Label().at((1.5, -1.5)).label("Schutzleiter", fontsize=9, halign='center')
    
    # Potenzialausgleich
    d += Erdung(
        bezeichnung="PA",
        label_loc='E',
        debug=True
    ).at((3, 0.5))
    d += elm.Label().at((3, -1.5)).label("Potenzialausgleich", fontsize=9, halign='center')
    
    # Erdung mit Label unten
    d += Erdung(
        bezeichnung="Erdung",
        label_loc='S',
        debug=True
    ).at((4.5, 0.5))
    d += elm.Label().at((4.5, -1.5)).label("Label unten", fontsize=9, halign='center')
    
    # Speichern
    d.save('output/komponenten_erdung.png')
    d.save('output/komponenten_erdung.svg')
    print("Erdungssymbol gespeichert: output/komponenten_erdung.png und output/komponenten_erdung.svg")
