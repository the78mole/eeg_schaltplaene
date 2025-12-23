"""Streamlit App für Schaltplan-Templates.

Interaktive Web-App zur Generierung von Schaltplänen für PV-Anlagen.
"""

import streamlit as st

# Definiere die Seiten
start_page = st.Page(
    page="pages/start.py",
    title="Start",
    icon="🏠",
    default=True
)

pv_mit_speicher = st.Page(
    page="pages/1_PV_mit_Speicher.py",
    title="PV mit Speicher",
    icon="🔋"
)

pv_ohne_speicher = st.Page(
    page="pages/2_PV_ohne_Speicher.py",
    title="PV ohne Speicher",
    icon="☀️"
)

# Navigation mit Gruppierung
pg = st.navigation(
    {
        "Home": [start_page],
        "Templates": [pv_mit_speicher, pv_ohne_speicher]
    }
)

# Setze Seiten-Konfiguration
st.set_page_config(
    page_title="Schaltplan Generator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Führe die ausgewählte Seite aus
pg.run()

st.info("👈 Wählen Sie ein Template in der Seitenleiste aus!")
