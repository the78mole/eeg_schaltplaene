"""Batteriespeicher nach DIN EN 60617.

Batteriespeicher für PV-Anlagen und andere Anwendungen.
"""

import schemdraw
import schemdraw.elements as elm
from schemdraw import segments


class Batterie(elm.Element):
    """
    Batteriespeicher nach DIN EN 60617.
    
    Dargestellt als Rechteck mit Batteriesymbol (mehrere Zellen).
    
    Args:
        bezeichnung: Bezeichner der Batterie (z.B. "BAT1", "BAT2")
        kapazitaet_kwh: Kapazität in kWh (z.B. 5, 10, 13.5)
        spannung_v: Nennspannung in Volt (z.B. 48, 400)
        hersteller: Hersteller/Typ der Batterie (optional)
        debug: Zeigt Ankerpunkte zur Fehlersuche
    """
    
    def __init__(self, 
                 bezeichnung: str = "BAT1",
                 kapazitaet_kwh: float = 10.0,
                 spannung_v: int = 48,
                 hersteller: str = "",
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
        
        # Batteriesymbol in der Mitte (um 90° gegen UZS gedreht)
        # Fettes gefülltes Rechteck (negative Elektrode / Minus) - unten
        minus_breite = 0.25
        minus_hoehe = 0.04  # Dicke des Rechtecks
        minus_y = -0.05
        self.segments.append(segments.Segment([
            (-minus_breite/2, minus_y - minus_hoehe/2),
            (minus_breite/2, minus_y - minus_hoehe/2),
            (minus_breite/2, minus_y + minus_hoehe/2),
            (-minus_breite/2, minus_y + minus_hoehe/2),
            (-minus_breite/2, minus_y - minus_hoehe/2)
        ], fill='black'))
        
        # Dünner längerer Strich (positive Elektrode / Plus) - oben
        plus_breite = 0.45
        plus_dicke = 1  # Normale Linienstärke
        plus_y = 0.05
        self.segments.append(segments.Segment([
            (-plus_breite/2, plus_y),
            (plus_breite/2, plus_y)
        ], lw=plus_dicke))
        
        # Stummel als Anschlüsse (kurz, nicht bis zum Rand)
        stummel_laenge = 0.2
        
        # Unterer Stummel (von Minus-Elektrode nach unten)
        self.segments.append(segments.Segment([
            (0, minus_y),
            (0, minus_y - stummel_laenge)
        ]))
        
        # Oberer Stummel (von Plus-Elektrode nach oben)
        self.segments.append(segments.Segment([
            (0, plus_y),
            (0, plus_y + stummel_laenge)
        ]))
        
        # Ankerpunkte auf allen vier Seiten
        self.anchors['W'] = (-breite/2, 0)  # West (links)
        self.anchors['E'] = (breite/2, 0)   # East (rechts)
        self.anchors['N'] = (0, hoehe/2)    # North (oben)
        self.anchors['S'] = (0, -hoehe/2)   # South (unten)
        self.anchors['plus'] = (breite/2, 0)   # Plus-Pol (rechts)
        self.anchors['minus'] = (-breite/2, 0) # Minus-Pol (links)
        
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
        
        # Beschriftung oben
        if bezeichnung:
            self.segments.append(segments.SegmentText(
                (0, hoehe/2 + 0.25), bezeichnung, fontsize=10, align=('center', 'bottom')
            ))
        
        # Technische Daten unten
        y_offset = -hoehe/2 - 0.25
        if kapazitaet_kwh:
            self.segments.append(segments.SegmentText(
                (0, y_offset), f"{kapazitaet_kwh}kWh", fontsize=8, align=('center', 'top')
            ))
            y_offset -= 0.2
        
        if spannung_v:
            self.segments.append(segments.SegmentText(
                (0, y_offset), f"{spannung_v}V", fontsize=8, align=('center', 'top')
            ))
            y_offset -= 0.2
        
        if hersteller:
            self.segments.append(segments.SegmentText(
                (0, y_offset), hersteller, fontsize=7, align=('center', 'top')
            ))


if __name__ == "__main__":
    """Visualisierung der Batteriespeicher."""
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=12)
    
    # Titel
    d += elm.Label().at((3, 3.5)).label("Batteriespeicher (DIN EN 60617)", fontsize=16)
    
    # Kleiner Speicher
    d += Batterie(
        bezeichnung="BAT1",
        kapazitaet_kwh=5.0,
        spannung_v=48,
        debug=True
    ).at((1.5, 1.5))
    d += elm.Label().at((1.5, -0.2)).label("5kWh / 48V", fontsize=9, halign='center')
    
    # Mittelgroßer Speicher
    d += Batterie(
        bezeichnung="BAT2",
        kapazitaet_kwh=10.0,
        spannung_v=400,
        debug=True
    ).at((4.5, 1.5))
    d += elm.Label().at((4.5, -0.2)).label("10kWh / 400V", fontsize=9, halign='center')
    
    # Großer Speicher mit Hersteller
    d += Batterie(
        bezeichnung="BAT3",
        kapazitaet_kwh=13.5,
        spannung_v=400,
        hersteller="Tesla Powerwall",
        debug=True
    ).at((3, -1.5))
    d += elm.Label().at((3, -3.5)).label("Mit Herstellerangabe", fontsize=9, halign='center')
    
    # Speichern
    d.save('output/komponenten_batterie.png')
    d.save('output/komponenten_batterie.svg')
    print("Batterie gespeichert: output/komponenten_batterie.png und output/komponenten_batterie.svg")
