"""Templates für vollständige Schaltpläne.

Dieses Modul enthält vorgefertigte Templates für häufig verwendete
Schaltplan-Konfigurationen, die einfach parametrisiert werden können.
"""

# Lazy imports zur Vermeidung von RuntimeWarnings bei python -m Ausführung
def __getattr__(name):
    if name == 'PvSpeicherSystemUeberschuss':
        from .pv_speicher_system_ueberschuss import PvSpeicherSystemUeberschuss
        return PvSpeicherSystemUeberschuss
    elif name == 'PvSystemUeberschuss':
        from .pv_system_ueberschuss import PvSystemUeberschuss
        return PvSystemUeberschuss
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ['PvSpeicherSystemUeberschuss', 'PvSystemUeberschuss']
