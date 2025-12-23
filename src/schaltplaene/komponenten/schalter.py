"""
Schalter-Komponenten.
"""

import schemdraw
import schemdraw.elements as elm
from schemdraw.elements import Element
from schemdraw import segments

try:
    from .enums import ComponentFlow
except ImportError:
    from enums import ComponentFlow


class Schalter(Element):
    """
    Schalter / Hauptschalter nach DIN EN 60617.
    
    Darstellung als Schalter-Symbol mit schräger Unterbrechung.
    
    Args:
        bezeichnung: Bezeichnung (z.B. "HS", "S")
        flow: Flussrichtung (ComponentFlow.FLOW_V für vertikal, FLOW_H für horizontal)
        oeffner: Wenn True, wird ein Öffner-Kontakt dargestellt (rechtwinkliger Strich vom offenen Kontakt)
    """
    
    def __init__(self, bezeichnung: str = "S",
                 flow: ComponentFlow = ComponentFlow.FLOW_V, oeffner: bool = False, *args, **kwargs):
        # Fix für Schemdraw Auto-Rotation: Horizontale Schalter brauchen theta=0
        if flow == ComponentFlow.FLOW_H and 'theta' not in kwargs:
            kwargs['theta'] = 0
        
        super().__init__(*args, **kwargs)
        
        # Kontakte
        kontakt_abstand = 0.65
        leitungs_laenge = 0.6
        
        if flow == ComponentFlow.FLOW_V:
            # Vertikale Ausrichtung
            # Unterer Kontakt
            self.segments.append(segments.Segment([
                (0, -leitungs_laenge), (0, -kontakt_abstand/2)
            ]))
            
            # Oberer Kontakt
            self.segments.append(segments.Segment([
                (0, kontakt_abstand/2), (0, leitungs_laenge)
            ]))
            
            # Schaltmesser (schräg zur Seite, geöffnet)
            messer_laenge = 0.75 if oeffner else 0.55
            messer_ende_x = 0.15
            messer_ende_y = -kontakt_abstand/2 + messer_laenge
            
            self.segments.append(segments.Segment([
                (0, -kontakt_abstand/2), (messer_ende_x, messer_ende_y)
            ]))
            
            # Öffner-Kontakt: Senkrechter Strich vom Kontakt weg
            if oeffner:
                oeffner_laenge = 0.2
                # Vom oberen Kontakt (wo das Messer NICHT beginnt) senkrecht nach rechts
                self.segments.append(segments.Segment([
                    (0, kontakt_abstand/2),
                    (oeffner_laenge, kontakt_abstand/2)
                ]))
            
            self.anchors['start'] = (0, -leitungs_laenge)
            self.anchors['end'] = (0, leitungs_laenge)
            
            # Beschriftung rechts
            if bezeichnung:
                self.segments.append(segments.SegmentText(
                    (0.6, 0.15), bezeichnung, fontsize=10, align=('left', 'center')
                ))
        else:
            # Horizontale Ausrichtung
            # Linker Kontakt
            self.segments.append(segments.Segment([
                (-leitungs_laenge, 0), (-kontakt_abstand/2, 0)
            ]))
            
            # Rechter Kontakt
            self.segments.append(segments.Segment([
                (kontakt_abstand/2, 0), (leitungs_laenge, 0)
            ]))
            
            # Schaltmesser (schräg nach oben, geöffnet)
            messer_laenge = 0.75 if oeffner else 0.55
            messer_ende_x = -kontakt_abstand/2 + messer_laenge
            messer_ende_y = 0.15
            
            self.segments.append(segments.Segment([
                (-kontakt_abstand/2, 0), (messer_ende_x, messer_ende_y)
            ]))
            
            # Öffner-Kontakt: Senkrechter Strich vom Kontakt weg
            if oeffner:
                oeffner_laenge = 0.2
                # Vom rechten Kontakt (wo das Messer NICHT beginnt) senkrecht nach oben
                self.segments.append(segments.Segment([
                    (kontakt_abstand/2, 0),
                    (kontakt_abstand/2, oeffner_laenge)
                ]))
            
            self.anchors['start'] = (-leitungs_laenge, 0)
            self.anchors['end'] = (leitungs_laenge, 0)
            
            # Beschriftung unten
            if bezeichnung:
                self.segments.append(segments.SegmentText(
                    (0, -0.35), bezeichnung, fontsize=10, align=('center', 'top')
                ))


if __name__ == "__main__":
    """Visualisierung der Schalter."""
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=12)
    
    # Titel
    d += elm.Label().at((4, 6)).label("Schalter (DIN EN 60617)", fontsize=16)
    
    # Schalter - FLOW_V
    d += Schalter(bezeichnung="HS1", flow=ComponentFlow.FLOW_V).at((1, 4))
    d += Schalter(bezeichnung="S1", flow=ComponentFlow.FLOW_V, oeffner=True).at((3, 4))
    
    # Schalter - FLOW_H
    d += Schalter(bezeichnung="HS2", flow=ComponentFlow.FLOW_H).at((1.5, 2))
    d += Schalter(bezeichnung="S2", flow=ComponentFlow.FLOW_H, oeffner=True).at((4.5, 2))
    
    # Dokumentation rechts
    doc_x = 7
    doc_y_start = 5
    d += elm.Label().at((doc_x, doc_y_start)).label("Komponenten:", fontsize=11, loc='right')
    d += elm.Label().at((doc_x+0.2, doc_y_start-0.4)).label("• Schalter / Hauptschalter", fontsize=9, loc='right')
    d += elm.Label().at((doc_x+0.3, doc_y_start-0.7)).label("- Schräges Schaltmesser", fontsize=8, loc='right')
    d += elm.Label().at((doc_x+0.3, doc_y_start-1.0)).label("- FLOW_V (vertikal)", fontsize=8, loc='right')
    d += elm.Label().at((doc_x+0.3, doc_y_start-1.3)).label("- FLOW_H (horizontal)", fontsize=8, loc='right')
    d += elm.Label().at((doc_x+0.3, doc_y_start-1.6)).label("- Optional: allpolig", fontsize=8, loc='right')

    
    # Speichern und anzeigen
    from pathlib import Path
    output_path_png = Path("output/komponenten_schalter.png")
    output_path_svg = Path("output/komponenten_schalter.svg")
    output_path_png.parent.mkdir(parents=True, exist_ok=True)
    d.save(str(output_path_png))
    d.save(str(output_path_svg))
    print(f"Schalter gespeichert: {output_path_png} und {output_path_svg}")
