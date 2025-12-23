"""Streamlit Page: PV-Anlage ohne Speicher."""

import streamlit as st
import schemdraw
from io import BytesIO
from PIL import Image
import streamlit.components.v1 as components

from schaltplaene.templates.pv_system_ueberschuss import PvSystemUeberschuss

st.set_page_config(
    page_title="PV-Anlage ohne Speicher",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ PV-Anlage ohne Speicher")
st.markdown("Generieren Sie einen Schaltplan für eine PV-Anlage mit Überschusseinspeisung (ohne Batteriespeicher).")

# Sidebar für Parameter
st.sidebar.header("⚙️ Parameter")

st.sidebar.subheader("Netzanschluss")
f1_nennstrom = st.sidebar.number_input(
    "F1 Nennstrom (A)",
    min_value=10,
    max_value=200,
    value=50,
    step=5,
    help="Nennstrom der Schmelzsicherung F1 (HAK)"
)

f2_nennstrom = st.sidebar.number_input(
    "F2 Nennstrom (A)",
    min_value=10,
    max_value=100,
    value=35,
    step=5,
    help="Nennstrom des Leitungsschutzschalters F2"
)

f2_charakteristik_auswahl = st.sidebar.selectbox(
    "F2 Charakteristik",
    options=["E", "Cs", "Andere..."],
    index=0,  # Standard: E
    help="Auslösecharakteristik des Leitungsschutzschalters"
)

# Wenn "Andere..." gewählt wurde, Freitextfeld anzeigen
if f2_charakteristik_auswahl == "Andere...":
    f2_charakteristik = st.sidebar.text_input(
        "Bitte Charakteristik eingeben",
        value="B",
        help="Geben Sie die gewünschte Charakteristik ein"
    )
else:
    f2_charakteristik = f2_charakteristik_auswahl

st.sidebar.subheader("Zähler")
z1_zaehler_nr = st.sidebar.text_input(
    "Z1 Zählernummer",
    value="1EMH00xxx",
    help="Zählernummer für den Netzzähler"
)

st.sidebar.subheader("PV-Anlage")
wechselrichter_kw = st.sidebar.number_input(
    "Wechselrichter Leistung (kW)",
    min_value=1.0,
    max_value=30.0,
    value=10.0,
    step=0.5,
    help="Nennleistung des Wechselrichters"
)

pv_leistung_kwp = st.sidebar.number_input(
    "PV-Generator Leistung (kWp)",
    min_value=1.0,
    max_value=50.0,
    value=12.0,
    step=0.5,
    help="Nennleistung der PV-Module"
)

st.sidebar.subheader("Verbrauch")
hausverbrauch_kw = st.sidebar.number_input(
    "Hausverbrauch (kW)",
    min_value=1.0,
    max_value=50.0,
    value=15.0,
    step=1.0,
    help="Typischer Hausverbrauch"
)

st.sidebar.subheader("Schaltplan")
titel = st.sidebar.text_input(
    "Titel des Schaltplans",
    value="PV-Anlage ohne Speicher - Überschusseinspeisung",
    help="Text, der als Titel auf dem Schaltplan angezeigt wird"
)

# Generiere Button
if st.sidebar.button("🔄 Schaltplan generieren", type="primary"):
    with st.spinner("Generiere Schaltplan..."):
        try:
            # Template erstellen
            template = PvSystemUeberschuss(
                f1_nennstrom_a=f1_nennstrom,
                f2_nennstrom_a=f2_nennstrom,
                f2_charakteristik=f2_charakteristik,
                z1_zaehler_nr=z1_zaehler_nr,
                hausverbrauch_kw=hausverbrauch_kw,
                wechselrichter_kw=wechselrichter_kw,
                pv_leistung=f"{pv_leistung_kwp}kWp"
            )
            
            # Schaltplan erstellen
            drawing = template.erstelle_schaltplan(titel=titel)
            
            # SVG generieren
            svg_data = drawing.get_imagedata('svg')
            
            # PNG generieren
            png_data = drawing.get_imagedata('png')
            
            # In Session State speichern
            st.session_state['svg_data'] = svg_data
            st.session_state['png_data'] = png_data
            st.session_state['generated'] = True
            
            st.success("✅ Schaltplan erfolgreich generiert!")
            
        except Exception as e:
            st.error(f"❌ Fehler beim Generieren: {str(e)}")
            st.session_state['generated'] = False

# Anzeige des generierten Schaltplans
if st.session_state.get('generated', False):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📊 Vorschau")
        # SVG als HTML anzeigen für beste Qualität
        svg_str = st.session_state['svg_data'].decode('utf-8')
        components.html(f'<div style="width:100%; overflow:auto;">{svg_str}</div>', height=1400, scrolling=False)
    
    with col2:
        st.subheader("💾 Downloads")
        
        # SVG Download
        st.download_button(
            label="⬇️ SVG herunterladen",
            data=st.session_state['svg_data'],
            file_name=f"pv_system_{wechselrichter_kw}kW.svg",
            mime="image/svg+xml",
            use_container_width=True
        )
        
        # PNG Download
        st.download_button(
            label="⬇️ PNG herunterladen",
            data=st.session_state['png_data'],
            file_name=f"pv_system_{wechselrichter_kw}kW.png",
            mime="image/png",
            use_container_width=True
        )
        
        st.markdown("---")
        st.markdown("""
        **Dateiformat-Infos:**
        - **SVG**: Vektorgrafik, beliebig skalierbar
        - **PNG**: Rastergrafik, 300 DPI
        """)

else:
    st.info("👈 Passen Sie die Parameter in der Seitenleiste an und klicken Sie auf 'Schaltplan generieren'")
