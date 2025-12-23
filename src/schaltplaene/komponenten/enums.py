"""
Gemeinsame Enums für alle Komponenten.
"""

from enum import Enum


class ComponentFlow(Enum):
    """Flussrichtung/Orientierung von Komponenten."""
    FLOW_V = 0  # Vertikal (Anschlüsse oben/unten)
    FLOW_H = 1  # Horizontal (Anschlüsse links/rechts)
