# Manchester United 2026/27 Tactical Investigation Dashboard

An interactive Streamlit analytics dashboard investigating the root causes of Manchester United's
poor start to the 2026/27 season, built with Streamlit, Plotly and Pandas.

## Design
The UI replicates the Google Stitch **"United Intel · Tactical Lab"** concept (Tactical Intelligence & Telemetry
design system): obsidian surfaces, Plus Jakarta Sans + Geist typography, Material Symbols icons, a left-rail
navigation, a sticky scope/filter/export top bar, and Stitch-style KPI strips, HTML/SVG charts and telemetry tables.
Every figure is computed from the project dataset (Stitch's placeholder numbers are not used).

## Features
- Executive KPI overview (record, goals, xG / xGA, possession)
- Match-by-match results & form breakdown
- Attacking analytics and top goal contributors
- Defensive & transition deficiency analysis
- 22-player squad performance matrix
- **Interactive per-issue tactics boards** — toggle tactical layers and inspect players on a football pitch map

## Run locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Data
All figures are self-contained in `streamlit_app.py` (illustrative dataset for a portfolio project).
