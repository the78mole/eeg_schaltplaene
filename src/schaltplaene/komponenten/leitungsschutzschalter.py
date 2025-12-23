"""
Leitungsschutzschalter-Komponenten.
"""

import schemdraw
import schemdraw.elements as elm
from schemdraw.elements import Element
from schemdraw import segments

try:
    from .enums import ComponentFlow
except ImportError:
    from enums import ComponentFlow


class Leitungsschutzschalter(Element):
    """
    Leitungsschutzschalter (LS-Schalter) nach DIN EN 60617.
    
    Darstellung mit Schaltmesser und Pfeil (magnetische/thermische Auslösung).
    
    Args:
        bezeichnung: Bezeichnung (z.B. "LS1", "Q1")
        nennstrom_a: Nennstrom in Ampere
        charakteristik: Auslösecharakteristik (B, C, D)
        flow: Orientierung des Schalters (FLOW_V oder FLOW_H)
        debug: Debug-Modus zur Anzeige der Anchors
    """
    
    def __init__(self, bezeichnung: str = "LS", nennstrom_a: int = None, 
                 charakteristik: str = "B", flow: ComponentFlow = ComponentFlow.FLOW_V, 
                 debug: bool = False, *args, **kwargs):
        
        # Theta-Fix für horizontale Ausrichtung
        if flow == ComponentFlow.FLOW_H and 'theta' not in kwargs:
            kwargs['theta'] = 0
            
        super().__init__(*args, **kwargs)
        
        leitungs_laenge = 0.6
        kontakt_abstand = 0.65
        
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
            messer_laenge = 0.55
            messer_ende_x = 0.15
            messer_ende_y = -kontakt_abstand/2 + messer_laenge
            
            self.segments.append(segments.Segment([
                (0, -kontakt_abstand/2), (messer_ende_x, messer_ende_y)
            ]))
            
            # Pfeil am Kontaktmesser (senkrecht nach außen, zum Ende hin verschoben)
            pfeil_pos = 0.7  # Position entlang des Messers (70%)
            pfeil_x = messer_ende_x * pfeil_pos
            pfeil_y = -kontakt_abstand/2 + messer_laenge * pfeil_pos
            pfeil_laenge = 0.2
            
            # Pfeil senkrecht zum Messer nach außen (rechts)
            pfeil_end_x = pfeil_x + pfeil_laenge
            pfeil_end_y = pfeil_y - pfeil_laenge * 0.3  # Ausgleich für Messerwinkel
            
            # Pfeilschaft
            self.segments.append(segments.Segment([
                (pfeil_x, pfeil_y), (pfeil_end_x, pfeil_end_y)
            ]))
            
            # Ausgefüllte Pfeilspitze (Dreieck) - senkrecht zur Pfeilrichtung
            spitze_laenge = 0.08
            spitze_breite = 0.05
            
            # Pfeilrichtung
            pfeil_dx = pfeil_end_x - pfeil_x
            pfeil_dy = pfeil_end_y - pfeil_y
            pfeil_len = (pfeil_dx**2 + pfeil_dy**2)**0.5
            
            # Normierte Richtungen
            pfeil_dx_norm = pfeil_dx / pfeil_len
            pfeil_dy_norm = pfeil_dy / pfeil_len
            
            # Senkrechte Richtung (90° gedreht)
            perp_dx = -pfeil_dy_norm
            perp_dy = pfeil_dx_norm
            
            # Punkte der Pfeilspitze
            basis_x = pfeil_end_x - spitze_laenge * pfeil_dx_norm
            basis_y = pfeil_end_y - spitze_laenge * pfeil_dy_norm
            
            self.segments.append(segments.Segment([
                (pfeil_end_x, pfeil_end_y),
                (basis_x + spitze_breite * perp_dx, basis_y + spitze_breite * perp_dy),
                (basis_x - spitze_breite * perp_dx, basis_y - spitze_breite * perp_dy),
                (pfeil_end_x, pfeil_end_y)
            ], fill='black'))
            
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
                    (0.6, 0.15), bezeichnung, fontsize=10, align=('left', 'center')
                ))
            
            if nennstrom_a:
                label_text = f"{charakteristik}{nennstrom_a}"
                self.segments.append(segments.SegmentText(
                    (0.6, -0.15), label_text, fontsize=8, align=('left', 'center')
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
            messer_laenge = 0.55
            messer_ende_x = -kontakt_abstand/2 + messer_laenge
            messer_ende_y = 0.15
            
            self.segments.append(segments.Segment([
                (-kontakt_abstand/2, 0), (messer_ende_x, messer_ende_y)
            ]))
            
            # Pfeil am Kontaktmesser (senkrecht nach außen, zum Ende hin verschoben)
            pfeil_pos = 0.7  # Position entlang des Messers (70%)
            pfeil_x = -kontakt_abstand/2 + messer_laenge * pfeil_pos
            pfeil_y = messer_ende_y * pfeil_pos
            pfeil_laenge = 0.2
            
            # Pfeil senkrecht zum Messer nach außen (oben)
            pfeil_end_x = pfeil_x - pfeil_laenge * 0.3  # Ausgleich für Messerwinkel
            pfeil_end_y = pfeil_y + pfeil_laenge
            
            # Pfeilschaft
            self.segments.append(segments.Segment([
                (pfeil_x, pfeil_y), (pfeil_end_x, pfeil_end_y)
            ]))
            
            # Ausgefüllte Pfeilspitze (Dreieck) - senkrecht zur Pfeilrichtung
            spitze_laenge = 0.08
            spitze_breite = 0.05
            
            # Pfeilrichtung
            pfeil_dx = pfeil_end_x - pfeil_x
            pfeil_dy = pfeil_end_y - pfeil_y
            pfeil_len = (pfeil_dx**2 + pfeil_dy**2)**0.5
            
            # Normierte Richtungen
            pfeil_dx_norm = pfeil_dx / pfeil_len
            pfeil_dy_norm = pfeil_dy / pfeil_len
            
            # Senkrechte Richtung (90° gedreht)
            perp_dx = -pfeil_dy_norm
            perp_dy = pfeil_dx_norm
            
            # Punkte der Pfeilspitze
            basis_x = pfeil_end_x - spitze_laenge * pfeil_dx_norm
            basis_y = pfeil_end_y - spitze_laenge * pfeil_dy_norm
            
            self.segments.append(segments.Segment([
                (pfeil_end_x, pfeil_end_y),
                (basis_x + spitze_breite * perp_dx, basis_y + spitze_breite * perp_dy),
                (basis_x - spitze_breite * perp_dx, basis_y - spitze_breite * perp_dy),
                (pfeil_end_x, pfeil_end_y)
            ], fill='black'))
            
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
            
            # Beschriftung unten
            if bezeichnung:
                self.segments.append(segments.SegmentText(
                    (0, -0.35), bezeichnung, fontsize=10, align=('center', 'top')
                ))
            
            if nennstrom_a:
                label_text = f"{charakteristik}{nennstrom_a}"
                self.segments.append(segments.SegmentText(
                    (0, -0.55), label_text, fontsize=7, align=('center', 'top')
                ))


if __name__ == "__main__":
    """Visualisierung der Leitungsschutzschalter."""
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=12)
    
    # Titel
    d += elm.Label().at((4, 5)).label("Leitungsschutzschalter (DIN EN 60617)", fontsize=16)
    
    # FLOW_V Varianten
    d += Leitungsschutzschalter(nennstrom_a=16, charakteristik="B", bezeichnung="LS1", flow=ComponentFlow.FLOW_V).at((1, 3))
    d += Leitungsschutzschalter(nennstrom_a=25, charakteristik="C", bezeichnung="LS2", flow=ComponentFlow.FLOW_V).at((3, 3))
    
    # FLOW_H Varianten
    d += Leitungsschutzschalter(nennstrom_a=20, charakteristik="B", bezeichnung="LS3", flow=ComponentFlow.FLOW_H).at((1.5, 1))
    d += Leitungsschutzschalter(nennstrom_a=32, charakteristik="C", bezeichnung="LS4", flow=ComponentFlow.FLOW_H, debug=True).at((4.5, 1))
    
    # Dokumentation rechts
    doc_x = 7
    doc_y_start = 4
    d += elm.Label().at((doc_x, doc_y_start)).label("Komponenten:", fontsize=11, loc='right')
    d += elm.Label().at((doc_x+0.2, doc_y_start-0.4)).label("• Leitungsschutzschalter", fontsize=9, loc='right')
    d += elm.Label().at((doc_x+0.3, doc_y_start-0.7)).label("- Schaltmesser mit Pfeil", fontsize=8, loc='right')
    d += elm.Label().at((doc_x+0.3, doc_y_start-1.0)).label("- Charakteristik B/C/D", fontsize=8, loc='right')
    d += elm.Label().at((doc_x+0.3, doc_y_start-1.3)).label("- FLOW_V / FLOW_H", fontsize=8, loc='right')
    
    # Speichern und anzeigen
    from pathlib import Path
    output_path_png = Path("output/komponenten_leitungsschutzschalter.png")
    output_path_svg = Path("output/komponenten_leitungsschutzschalter.svg")
    output_path_png.parent.mkdir(parents=True, exist_ok=True)
    d.save(str(output_path_png))
    d.save(str(output_path_svg))
    print(f"Leitungsschutzschalter gespeichert: {output_path_png} und {output_path_svg}")
