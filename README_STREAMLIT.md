# 🌐 Streamlit Web-App

Interaktive Web-Anwendung zur Generierung von Schaltplänen für PV-Anlagen.

## Features

- ⚙️ **Interaktive Parameter-Eingabe** - Alle Werte individuell anpassbar
- 📊 **Live-Vorschau** - Sofortige Visualisierung des Schaltplans
- 💾 **Download-Funktionen** - Export als SVG (Vektorgrafik) oder PNG (300 DPI)
- 🔋 **Zwei Templates verfügbar**:
  - PV-Anlage mit Batteriespeicher
  - PV-Anlage ohne Speicher (Überschusseinspeisung)

## Installation & Start

```bash
# Dependencies installieren (falls noch nicht geschehen)
uv sync

# Streamlit App starten
uv run streamlit run app.py
```

Die App öffnet sich automatisch im Browser unter `http://localhost:8501`

## Verwendung

1. **Template auswählen** - Wählen Sie in der Seitenleiste zwischen den verfügbaren Templates
2. **Parameter anpassen** - Passen Sie die Werte für Ihre PV-Anlage an
3. **Generieren** - Klicken Sie auf "Schaltplan generieren"
4. **Download** - Laden Sie den Schaltplan als SVG oder PNG herunter

## Struktur

```
├── app.py                          # Haupt-App (Landing Page)
├── pages/
│   ├── 1_PV_mit_Speicher.py       # Template: PV mit Batteriespeicher
│   └── 2_PV_ohne_Speicher.py      # Template: PV ohne Speicher
└── .streamlit/
    └── config.toml                 # Streamlit Konfiguration
```

## Konfigurierbare Parameter

### PV-Anlage mit Speicher
- F1 Nennstrom (HAK-Sicherung)
- F2 Nennstrom und Charakteristik
- Zählernummer
- Wechselrichter Leistung
- PV-Generator Leistung
- Batteriespeicher Kapazität
- Hausverbrauch

### PV-Anlage ohne Speicher
- F1 Nennstrom (HAK-Sicherung)
- F2 Nennstrom und Charakteristik
- Zählernummer
- Wechselrichter Leistung
- PV-Generator Leistung
- Hausverbrauch

## Technologie

- **Streamlit** - Web-Framework für Python
- **Schemdraw** - Schaltplan-Generierung
- **PIL/Pillow** - Bildverarbeitung

## Deployment

Für Deployment auf Streamlit Cloud oder anderen Plattformen:

1. Repository auf GitHub pushen
2. Mit Streamlit Cloud verbinden
3. `app.py` als Hauptdatei auswählen
4. Dependencies aus `pyproject.toml` werden automatisch installiert
