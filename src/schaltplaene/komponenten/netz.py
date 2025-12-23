"""Netz/Strommast-Symbol für elektrische Schaltpläne.

Symbolisiert die Verbindung zum öffentlichen Stromnetz.
"""

import schemdraw
import schemdraw.elements as elm
from schemdraw import segments


class Netz(elm.Element):
    """
    Netz/Strommast-Symbol für Schaltpläne.
    
    Dargestellt als Rechteck mit Strommast-Symbol.
    
    Args:
        bezeichnung: Bezeichner (z.B. "Netz", "EVU", "Stromnetz")
        spannung_v: Netzspannung als Zahl (z.B. 230, 400) oder Text (z.B. "3 x 230/400V")
        label_loc: Position der Beschriftung ('N', 'S', 'E', 'W', 'NE', 'NO', 'NW', 'SE', 'SO', 'SW')
        debug: Zeigt Ankerpunkte zur Fehlersuche
    """
    
    def __init__(self, 
                 bezeichnung: str = "Netz",
                 spannung_v = 400,
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
        
        # Strommast-Symbol in der Mitte (drei Dreiecke)
        
        # Großes längliches Dreieck als Mast (mit offenem Fußende)
        mast_hoehe = 0.5
        mast_breite_unten = 0.15
        mast_spitze_y = 0.3
        mast_basis_y = mast_spitze_y - mast_hoehe
        
        # Nur die beiden Schenkel, nicht die Basis
        self.segments.append(segments.Segment([
            (-mast_breite_unten/2, mast_basis_y),
            (0, mast_spitze_y)
        ]))
        self.segments.append(segments.Segment([
            (0, mast_spitze_y),
            (mast_breite_unten/2, mast_basis_y)
        ]))
        
        # Kurzes breites Dreieck oben (gemeinsame Spitze)
        quertraeger_oben_breite = 0.5
        quertraeger_oben_hoehe = 0.1
        
        self.segments.append(segments.Segment([
            (-quertraeger_oben_breite/2, mast_spitze_y - quertraeger_oben_hoehe),
            (0, mast_spitze_y),
            (quertraeger_oben_breite/2, mast_spitze_y - quertraeger_oben_hoehe),
            (-quertraeger_oben_breite/2, mast_spitze_y - quertraeger_oben_hoehe)
        ]))
        
        # Mittleres Dreieck (etwas breiter als das obere)
        quertraeger_mitte_breite = 0.6
        quertraeger_mitte_hoehe = 0.12
        quertraeger_mitte_y = mast_spitze_y - quertraeger_oben_hoehe - 0.08
        
        self.segments.append(segments.Segment([
            (-quertraeger_mitte_breite/2, quertraeger_mitte_y - quertraeger_mitte_hoehe),
            (0, quertraeger_mitte_y),
            (quertraeger_mitte_breite/2, quertraeger_mitte_y - quertraeger_mitte_hoehe),
            (-quertraeger_mitte_breite/2, quertraeger_mitte_y - quertraeger_mitte_hoehe)
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
        
        # Beschriftung und technische Daten an angegebener Position (gestapelt)
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
        
        # Bezeichnung
        if bezeichnung:
            self.segments.append(segments.SegmentText(
                pos, bezeichnung, fontsize=10, align=align
            ))
        
        # Spannung unter der Bezeichnung
        if spannung_v:
            # y_offset für Stapelung (immer nach unten = negativ)
            y_offset = -0.2
            
            # Position für Spannungsangabe
            spannung_pos = (pos[0], pos[1] + y_offset)
            
            # Wenn spannung_v eine Zahl ist, füge "V" hinzu, sonst verwende den String direkt
            if isinstance(spannung_v, (int, float)):
                spannung_text = f"{spannung_v}V"
            else:
                spannung_text = str(spannung_v)
            
            self.segments.append(segments.SegmentText(
                spannung_pos, spannung_text, fontsize=8, align=align
            ))


if __name__ == "__main__":
    """Visualisierung der Netz/Strommast-Symbole."""
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=12)
    
    # Titel
    d += elm.Label().at((3, 3.5)).label("Netz / Strommast-Symbol", fontsize=16)
    
    # Netz 230V
    d += Netz(
        bezeichnung="Netz",
        spannung_v=230,
        debug=True
    ).at((1.5, 1.5))
    d += elm.Label().at((1.5, -0.2)).label("230V Einphasig", fontsize=9, halign='center')
    
    # Netz 400V
    d += Netz(
        bezeichnung="EVU",
        spannung_v=400,
        debug=True
    ).at((4.5, 1.5))
    d += elm.Label().at((4.5, -0.2)).label("400V Drehstrom", fontsize=9, halign='center')
    
    # Stromnetz
    d += Netz(
        bezeichnung="Stromnetz",
        spannung_v=400,
        debug=True
    ).at((3, -1.5))
    d += elm.Label().at((3, -3.2)).label("Alternative Bezeichnung", fontsize=9, halign='center')
    
    # Speichern
    d.save('output/komponenten_netz.png')
    d.save('output/komponenten_netz.svg')
    print("Netz/Strommast gespeichert: output/komponenten_netz.png und output/komponenten_netz.svg")
