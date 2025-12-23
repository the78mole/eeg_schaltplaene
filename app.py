"""Streamlit App für Schaltplan-Templates.

Interaktive Web-App zur Generierung von Schaltplänen für PV-Anlagen.
"""

import streamlit as st

st.set_page_config(
    page_title="Schaltplan Generator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚡ Schaltplan Generator für PV-Anlagen")
st.markdown("""
Willkommen beim interaktiven Schaltplan-Generator!

Wählen Sie in der Seitenleiste ein Template aus, um loszulegen.

### Verfügbare Templates:
- **PV-Anlage mit Speicher** - Komplettes System mit Batteriespeicher
- **PV-Anlage ohne Speicher** - Einfache Überschusseinspeisung

### Features:
- ⚙️ Individuelle Parameteranpassung
- 📊 Live-Vorschau des Schaltplans
- 💾 Download als SVG oder PNG
- 🔄 Automatische Aktualisierung bei Änderungen
""")

st.info("👈 Wählen Sie ein Template in der Seitenleiste aus!")
