"""
Zähler-Komponenten für elektrische Schaltpläne.
"""

from enum import Enum
import schemdraw
import schemdraw.elements as elm
from schemdraw.elements import Element
from schemdraw import segments
from .enums import ComponentFlow


class ZaehlerPfeil(Enum):
    """Richtungspfeile für Zähler."""
    ARROW_NONE = 0   # Keine Pfeile
    ARROW_IN = 1     # Bezug (Pfeil nach oben)
    ARROW_OUT = 2    # Einspeisung (Pfeil nach unten)
    ARROW_BOTH = 3   # Zweirichtung (beide Pfeile)


class ZaehlerTarif(Enum):
    """Tarif-Option des Zählers."""
    TARIF_EINZEL = 0  # Ein Zählwerk (Eintarif)
    TARIF_ZWEI = 1    # Zwei Zählwerke (Zweitarif/HT+NT)


class Zaehler(Element):
    """
    Stromzähler (Einrichtung oder Zweirichtung).
    
    Darstellung als Rechteck mit Einheit (z.B. "kWh") und schmalem Rechteck darüber.
    Eingang unten, Ausgang (gezählt) oben.
    Mit optionalen Richtungspfeilen.
    
    Args:
        bezeichnung: Beschriftung des Zählers (z.B. "Z1")
        info: Zusätzliche Information unter dem Bezeichner (z.B. Zählernummer, "EMS SmartMeter")
        einheit: Einheit für die Messung (z.B. "kWh", "Wh", "MWh")
        pfeil: Richtungspfeil (ZaehlerPfeil.ARROW_NONE, ARROW_IN, ARROW_OUT, ARROW_BOTH)
        flow: Flussrichtung (ComponentFlow.FLOW_V für vertikal, FLOW_H für horizontal)
        tarif: Tarif-Option (ZaehlerTarif.TARIF_EINZEL oder TARIF_ZWEI)
        debug: Wenn True, werden rote Punkte an den Anchors gezeichnet
    """
    
    def __init__(self, bezeichnung: str = "Z", info: str = "", einheit: str = "kWh", 
                 pfeil: ZaehlerPfeil = ZaehlerPfeil.ARROW_NONE,
                 flow: ComponentFlow = ComponentFlow.FLOW_V,
                 tarif: ZaehlerTarif = ZaehlerTarif.TARIF_EINZEL,
                 debug: bool = False, *args, **kwargs):
        # Fix für Schemdraw Auto-Rotation: Horizontale Zähler brauchen theta=0
        if flow == ComponentFlow.FLOW_H and 'theta' not in kwargs:
            kwargs['theta'] = 0
        
        super().__init__(*args, **kwargs)
        
        # Hauptrechteck mit Einheit
        breite = 1.0
        hoehe = 0.8
        
        # Hauptrechteck
        self.segments.append(segments.Segment([
            (-breite/2, -hoehe/2), 
            (breite/2, -hoehe/2), 
            (breite/2, hoehe/2), 
            (-breite/2, hoehe/2), 
            (-breite/2, -hoehe/2)
        ]))
        
        # Schmales Rechteck darüber (Zählwerk)
        schmale_hoehe = 0.12
        abstand = 0.02
        
        if tarif == ZaehlerTarif.TARIF_ZWEI:
            # Ein großes Rechteck mit Trennlinie für Zweitarif (HT/NT)
            gesamthoehe = 2*schmale_hoehe + abstand
            self.segments.append(segments.Segment([
                (-breite/2, hoehe/2),
                (breite/2, hoehe/2),
                (breite/2, hoehe/2 + gesamthoehe),
                (-breite/2, hoehe/2 + gesamthoehe),
                (-breite/2, hoehe/2)
            ]))
            # Trennlinie in der Mitte
            self.segments.append(segments.Segment([
                (-breite/2, hoehe/2 + schmale_hoehe + abstand/2),
                (breite/2, hoehe/2 + schmale_hoehe + abstand/2)
            ]))
            ausgang_y = hoehe/2 + gesamthoehe
        else:
            # Ein schmales Rechteck für Eintarif
            self.segments.append(segments.Segment([
                (-breite/2, hoehe/2),
                (breite/2, hoehe/2),
                (breite/2, hoehe/2 + schmale_hoehe),
                (-breite/2, hoehe/2 + schmale_hoehe),
                (-breite/2, hoehe/2)
            ]))
            ausgang_y = hoehe/2 + schmale_hoehe
        
        # Anchors: abhängig von der Flussrichtung
        if flow == ComponentFlow.FLOW_V:
            # Vertikal: Eingang unten, Ausgang oben
            self.anchors['in'] = (0, -hoehe/2)
            self.anchors['out'] = (0, ausgang_y)
        else:  # FLOW_H
            # Horizontal: Eingang links, Ausgang rechts
            self.anchors['in'] = (-breite/2, 0)
            self.anchors['out'] = (breite/2, 0)
        
        self.anchors['center'] = (0, 0)
        self.anchors['start'] = self.anchors['in']
        self.anchors['end'] = self.anchors['out']
        
        # Richtungspfeile (Position abhängig von flow)
        pfeil_hoehe = 0.6
        pfeil_breite = 0.6
        
        if flow == ComponentFlow.FLOW_V:
            # Vertikale Ausrichtung: Pfeile links vom Zähler
            pfeil_x_mitte = -breite/2 - 0.2
            
            if pfeil == ZaehlerPfeil.ARROW_IN:
                # Ein Pfeil nach oben (Bezug)
                self.segments.append(segments.Segment([
                    (pfeil_x_mitte, -pfeil_hoehe/2),
                    (pfeil_x_mitte, pfeil_hoehe/2)
                ]))
                self.segments.append(segments.Segment([
                    (pfeil_x_mitte - 0.1, pfeil_hoehe/2 - 0.1),
                    (pfeil_x_mitte, pfeil_hoehe/2),
                    (pfeil_x_mitte + 0.1, pfeil_hoehe/2 - 0.1)
                ]))
                
            elif pfeil == ZaehlerPfeil.ARROW_OUT:
                # Ein Pfeil nach unten (Einspeisung)
                self.segments.append(segments.Segment([
                    (pfeil_x_mitte, pfeil_hoehe/2),
                    (pfeil_x_mitte, -pfeil_hoehe/2)
                ]))
                self.segments.append(segments.Segment([
                    (pfeil_x_mitte - 0.1, -pfeil_hoehe/2 + 0.1),
                    (pfeil_x_mitte, -pfeil_hoehe/2),
                    (pfeil_x_mitte + 0.1, -pfeil_hoehe/2 + 0.1)
                ]))
                
            elif pfeil == ZaehlerPfeil.ARROW_BOTH:
                # Zwei Pfeile (oben + unten)
                pfeil_x_links = -breite/2 - 0.35
                pfeil_x_rechts = -breite/2 - 0.2
                
                # Pfeil nach oben (Einspeisung)
                self.segments.append(segments.Segment([
                    (pfeil_x_links, -pfeil_hoehe/2),
                    (pfeil_x_links, pfeil_hoehe/2)
                ]))
                self.segments.append(segments.Segment([
                    (pfeil_x_links - 0.1, pfeil_hoehe/2 - 0.1),
                    (pfeil_x_links, pfeil_hoehe/2),
                    (pfeil_x_links + 0.1, pfeil_hoehe/2 - 0.1)
                ]))
                
                # Pfeil nach unten (Bezug)
                self.segments.append(segments.Segment([
                    (pfeil_x_rechts, pfeil_hoehe/2),
                    (pfeil_x_rechts, -pfeil_hoehe/2)
                ]))
                self.segments.append(segments.Segment([
                    (pfeil_x_rechts - 0.1, -pfeil_hoehe/2 + 0.1),
                    (pfeil_x_rechts, -pfeil_hoehe/2),
                    (pfeil_x_rechts + 0.1, -pfeil_hoehe/2 + 0.1)
                ]))
        
        else:  # FLOW_H
            # Horizontale Ausrichtung: Pfeile unter dem Zähler
            pfeil_y_mitte = -hoehe/2 - 0.2
            
            if pfeil == ZaehlerPfeil.ARROW_IN:
                # Ein Pfeil nach rechts (Bezug)
                self.segments.append(segments.Segment([
                    (-pfeil_breite/2, pfeil_y_mitte),
                    (pfeil_breite/2, pfeil_y_mitte)
                ]))
                self.segments.append(segments.Segment([
                    (pfeil_breite/2 - 0.1, pfeil_y_mitte - 0.1),
                    (pfeil_breite/2, pfeil_y_mitte),
                    (pfeil_breite/2 - 0.1, pfeil_y_mitte + 0.1)
                ]))
                
            elif pfeil == ZaehlerPfeil.ARROW_OUT:
                # Ein Pfeil nach links (Einspeisung)
                self.segments.append(segments.Segment([
                    (pfeil_breite/2, pfeil_y_mitte),
                    (-pfeil_breite/2, pfeil_y_mitte)
                ]))
                self.segments.append(segments.Segment([
                    (-pfeil_breite/2 + 0.1, pfeil_y_mitte - 0.1),
                    (-pfeil_breite/2, pfeil_y_mitte),
                    (-pfeil_breite/2 + 0.1, pfeil_y_mitte + 0.1)
                ]))
                
            elif pfeil == ZaehlerPfeil.ARROW_BOTH:
                # Zwei Pfeile (links + rechts)
                pfeil_y_oben = -hoehe/2 - 0.35
                pfeil_y_unten = -hoehe/2 - 0.2
                
                # Pfeil nach rechts (Bezug)
                self.segments.append(segments.Segment([
                    (-pfeil_breite/2, pfeil_y_oben),
                    (pfeil_breite/2, pfeil_y_oben)
                ]))
                self.segments.append(segments.Segment([
                    (pfeil_breite/2 - 0.1, pfeil_y_oben - 0.1),
                    (pfeil_breite/2, pfeil_y_oben),
                    (pfeil_breite/2 - 0.1, pfeil_y_oben + 0.1)
                ]))
                
                # Pfeil nach links (Einspeisung)
                self.segments.append(segments.Segment([
                    (pfeil_breite/2, pfeil_y_unten),
                    (-pfeil_breite/2, pfeil_y_unten)
                ]))
                self.segments.append(segments.Segment([
                    (-pfeil_breite/2 + 0.1, pfeil_y_unten - 0.1),
                    (-pfeil_breite/2, pfeil_y_unten),
                    (-pfeil_breite/2 + 0.1, pfeil_y_unten + 0.1)
                ]))
        
        # Beschriftung - Einheit zentriert im Hauptrechteck als Label
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['fontsize'] = 10
        self.segments.append(segments.SegmentText(
            (0, 0), einheit, fontsize=10
        ))
        
        # Bezeichnung - Position abhängig vom Flow
        if flow == ComponentFlow.FLOW_V:
            # Vertikal: Bezeichnung rechts vom Symbol
            self.segments.append(segments.SegmentText(
                (breite/2 + 0.15, 0), bezeichnung, fontsize=10, align=('left', 'center')
            ))
            # Info-Text unter dem Bezeichner (falls vorhanden)
            if info:
                self.segments.append(segments.SegmentText(
                    (breite/2 + 0.15, -0.25), info, fontsize=8, align=('left', 'center')
                ))
        else:  # FLOW_H
            # Horizontal: Bezeichnung über dem Symbol
            self.segments.append(segments.SegmentText(
                (0, ausgang_y + 0.15), bezeichnung, fontsize=10, align=('center', 'bottom')
            ))
            # Info-Text unter dem Bezeichner (falls vorhanden)
            if info:
                self.segments.append(segments.SegmentText(
                    (0, ausgang_y + 0.35), info, fontsize=8, align=('center', 'bottom')
                ))
        
        # Debug: Rote Punkte an den Anchors
        if debug:
            from schemdraw.segments import SegmentCircle
            self.segments.append(SegmentCircle(self.anchors['start'], 0.08, fill='red'))
            self.segments.append(SegmentCircle(self.anchors['end'], 0.08, fill='red'))


if __name__ == "__main__":
    """Visualisierung der Zähler-Komponenten."""
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=12)
    
    # Titel über den Symbolen
    d += elm.Label().at((3, 6.5)).label("Zähler-Komponente: Konfigurationsoptionen", fontsize=16)
    
    # Reihe 1: FLOW_V Eintarif
    z1 = Zaehler(bezeichnung="Z1", pfeil=ZaehlerPfeil.ARROW_IN, flow=ComponentFlow.FLOW_V, debug=True)
    d += z1.at((1.5, 5.5))
    d += elm.Label().at((1.5, 4.5)).label("FLOW_V Ein", halign='center', fontsize=9)
    
    d += Zaehler(bezeichnung="Z2", pfeil=ZaehlerPfeil.ARROW_BOTH, flow=ComponentFlow.FLOW_V, debug=True).at((4.5, 5.5))
    d += elm.Label().at((4.5, 4.5)).label("FLOW_V Zwei", halign='center', fontsize=9)
    
    # Reihe 2: FLOW_V Zweitarif
    z3 = Zaehler(bezeichnung="Z3", pfeil=ZaehlerPfeil.ARROW_IN, flow=ComponentFlow.FLOW_V, tarif=ZaehlerTarif.TARIF_ZWEI, debug=True)
    d += z3.at((1.5, 3.5))
    d += elm.Label().at((1.5, 2.5)).label("FLOW_V HT/NT", halign='center', fontsize=9)
    
    d += Zaehler(bezeichnung="Z4", pfeil=ZaehlerPfeil.ARROW_BOTH, flow=ComponentFlow.FLOW_V, tarif=ZaehlerTarif.TARIF_ZWEI, debug=True).at((4.5, 3.5))
    d += elm.Label().at((4.5, 2.5)).label("FLOW_V HT/NT+Zwei", halign='center', fontsize=9)
    
    # Verbindung Z3 -> Z1 (vertikal)
    d += elm.Line().at(z3.end).to(z1.start)
    
    # Reihe 3: FLOW_H Eintarif
    z5 = Zaehler(bezeichnung="Z5", pfeil=ZaehlerPfeil.ARROW_IN, flow=ComponentFlow.FLOW_H, debug=True)
    d += z5.at((1.5, 1.5))
    d += elm.Label().at((1.5, 0.5)).label("FLOW_H Ein", halign='center', fontsize=9)
    
    z6 = Zaehler(bezeichnung="Z6", pfeil=ZaehlerPfeil.ARROW_BOTH, flow=ComponentFlow.FLOW_H, tarif=ZaehlerTarif.TARIF_ZWEI, debug=True)
    d += z6.at((4.5, 1.5))
    d += elm.Label().at((4.5, 0.5)).label("FLOW_H HT/NT+Zwei", halign='center', fontsize=9)
    
    # Verbindung Z5 -> Z6 (horizontal)
    d += elm.Line().at(z5.end).to(z6.start)
    
    # Dokumentation rechts neben den Symbolen (linksbündig)
    doc_x = 6.5
    doc_y_start = 5.5
    d += elm.Label().at((doc_x, doc_y_start)).label("Parameter:", fontsize=11, loc='right')
    d += elm.Label().at((doc_x, doc_y_start-0.4)).label("", fontsize=9, loc='right')
    d += elm.Label().at((doc_x, doc_y_start-0.8)).label("ZaehlerPfeil:", fontsize=10, loc='right')
    d += elm.Label().at((doc_x+0.2, doc_y_start-1.1)).label("• ARROW_NONE - keine Pfeile", fontsize=9, loc='right')
    d += elm.Label().at((doc_x+0.2, doc_y_start-1.4)).label("• ARROW_IN - Pfeil nach oben (↑)", fontsize=9, loc='right')
    d += elm.Label().at((doc_x+0.2, doc_y_start-1.7)).label("• ARROW_OUT - Pfeil nach unten (↓)", fontsize=9, loc='right')
    d += elm.Label().at((doc_x+0.2, doc_y_start-2.0)).label("• ARROW_BOTH - beide Pfeile (↑↓)", fontsize=9, loc='right')
    d += elm.Label().at((doc_x, doc_y_start-2.5)).label("ComponentFlow:", fontsize=10, loc='right')
    d += elm.Label().at((doc_x+0.2, doc_y_start-2.8)).label("• FLOW_V - vertikale Anschlüsse", fontsize=9, loc='right')
    d += elm.Label().at((doc_x+0.2, doc_y_start-3.1)).label("• FLOW_H - horizontale Anschlüsse", fontsize=9, loc='right')
    d += elm.Label().at((doc_x, doc_y_start-3.6)).label("ZaehlerTarif:", fontsize=10, loc='right')
    d += elm.Label().at((doc_x+0.2, doc_y_start-3.9)).label("• TARIF_EINZEL - einfacher Zähler", fontsize=9, loc='right')
    d += elm.Label().at((doc_x+0.2, doc_y_start-4.2)).label("• TARIF_ZWEI - Zweitarif (HT/NT)", fontsize=9, loc='right')
    
    # Speichern und anzeigen
    from pathlib import Path
    output_path_png = Path("output/komponenten_zaehler.png")
    output_path_svg = Path("output/komponenten_zaehler.svg")
    output_path_png.parent.mkdir(parents=True, exist_ok=True)
    d.save(str(output_path_png))
    d.save(str(output_path_svg))
    print(f"Zähler-Komponenten gespeichert: {output_path_png} und {output_path_svg}")
