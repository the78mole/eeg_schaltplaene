"""Start-Seite der Streamlit App."""

import streamlit as st

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
