# 🌾 AGRI-INTELLIGENCE // National Agronomic Command Center for India

An industry-grade, animated, dual-stack agricultural intelligence platform combining **historical crop production records (1997–2020)** with **ICAR & NBSS&LUP agronomic science**, **Open-Meteo live 2026 satellite meteorology**, and a **cyberpunk glassmorphism web interface (React 19 + Vite)** alongside a **Streamlit modern dashboard**.

---

## 📌 Project Overview

Agriculture is the backbone of India's economy, yet yield and crop suitability vary drastically across agro-climatic zones, soil classifications, and seasonal rainfall distributions.

This project delivers an interactive command center bridging **19,689 real-world agricultural observations** across **30 Indian States/UTs** and **55 crops** with authoritative agronomic science:
- **ICAR** (Indian Council of Agricultural Research)
- **NBSS&LUP** (National Bureau of Soil Survey and Land Use Planning)
- **DES** (Directorate of Economics and Statistics, Ministry of Agriculture & Farmers Welfare)
- **TNAU** (Tamil Nadu Agricultural University Agritech Portal)
- **Open-Meteo Global WMO** (Real-time live 2026 satellite meteorological feed)

---

## 🚀 Key Features

### 1. ⚡ Cyberpunk Glassmorphic Dashboard
- **Visuals:** Credit-card style KPI cards, glowing yearly inflow bar charts, commodity donuts, agronomic radar, and rainfall spline wave.
- **1-Click "Exclude Coconut (Tonnes Only)" Toggle:** Solves the national reporting discrepancy where Coconut is recorded in *nuts* (308 Billion) while food crops are measured in *metric tonnes* (Rice: 2.2B MT, Wheat: 1.8B MT).
- **Multi-Theme Engine:** Seamless switching between Cyberpunk Dark, Slate Neumorphic, and Clean Light.
- **Micro-Interaction Sound Synthesizer:** Web Audio API procedural audio with mute/unmute control.

### 2. 🗺️ Survey of India Spatial Cartography
- **Survey of India SVG Boundaries:** Official administrative boundaries rendered with hardware-accelerated D3-Geo projections.
- **1997–2020 Animated Timeline Scrubber:** Auto-play and manual scrubbing through 24 years of state-wise production shifts.
- **Heatmaps & Tooltips:** Choropleths for Production, Mean Yield, and Annual Rainfall with 1-click drill-down to State Explorer.

### 3. 📍 State Explorer & Live 2026 Satellite Weather Feed
- **Live 2026 Weather Integration:** Connects to Open-Meteo API for all 30 state capitals (ambient temperature, humidity, precipitation, and surface wind speed).
- **Automated Agro-Advisories:** Dynamic notices generated in real time (e.g. *Optimal Field Conditions*, *Pathogen / Humidity Vigilance*, *Thermal Evapotranspiration Stress*).
- **Soil Taxonomy (ICAR-NBSS&LUP):** Dominant regional soils (Alluvial Loam, Black Regur, Red Sandy Loam, Laterite, etc.) and Planning Commission agro-climatic zones.

### 4. 🔮 ICAR Feasibility Simulator & Recommendation Engine
- **Algorithmic Matching Engine:** Evaluates soil suitability, water availability (mm), temperature range (°C), and season against 55 ICAR crop profiles.
- **Match Score & Confetti:** Generates feasibility percentages (0–100%) and instant recommendations for maximum harvest yield.

### 5. ⚔️ Head-to-Head Crop Battle (Resource Efficiency Comparator)
- **Side-by-Side Radar:** Compares any two crops on Water Economy, Heat Resilience, Harvest Speed, Yield Potential, and Soil Adaptability.
- **Water Savings Metric:** Demonstrates critical crop diversification tradeoffs (e.g., Rice vs. Millets/Bajra saving up to 67% irrigation water).

### 6. 🌱 Crop Intelligence & 4-Stage Lifecycle Progression
- **55 Crops:** Searchable database with duration days, reporting units, and optimal temperature/water windows.
- **Interactive Lifecycle Visualizer:** 4-stage biological progression (*Germination $\rightarrow$ Vegetative $\rightarrow$ Flowering/Filling $\rightarrow$ Physiological Ripeness*) with management guidelines.

### 7. 📋 Filterable Data Table & CSV Export
- Search and filter records by State, Crop, or Category with one-click CSV download.

---

## 🛠️ Dual-Stack Technology Architecture

| Layer | Technologies | Role |
| :--- | :--- | :--- |
| **Primary Frontend** | React 19, Vite 8, Tailwind CSS, Framer Motion, Recharts, D3-Geo | 60 FPS animated glassmorphism command center with Web Audio synthesis |
| **Live Telemetry** | Open-Meteo Global WMO Satellite API | Real-time 2026 meteorological feed for 30 state capitals |
| **Data Pipeline** | Python 3.11, Pandas, NumPy, JSON Exporter | Pre-aggregates 19,689 rows into dual-slice JSON (`agri_data.json`) |
| **Companion App** | Streamlit, Plotly Express & Graph Objects | Python companion dashboard (`app_modern.py`) |
| **Cartography** | Survey of India GeoJSON (36 boundaries) | Official administrative boundary definitions |

---

## 📁 Repository Structure

```text
Agriculture_dashboard/
├── .streamlit/
│   └── config.toml               # Streamlit theme configuration
├── data/
│   └── india_states.geojson      # Verified Survey of India administrative boundaries
├── frontend/                     # Full React 19 + Vite Production Web Application
│   ├── public/
│   │   ├── favicon.svg           # Custom SVG favicon
│   │   └── icons.svg
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx            # Dynamic navigation, theme & coconut toggle
│   │   │   ├── DashboardView.jsx     # Cyberpunk KPI cards, charts, spline wave
│   │   │   ├── SpatialMapView.jsx    # D3-Geo SVG map with timeline playback
│   │   │   ├── StateExplorerView.jsx # State taxonomy & Live 2026 weather feed
│   │   │   ├── CropIntelligenceView.jsx # 55 crops & 4-stage lifecycle visualizer
│   │   │   ├── CropSimulatorView.jsx # ICAR predictive feasibility simulator
│   │   │   ├── CropBattleView.jsx    # Head-to-head resource efficiency comparator
│   │   │   └── DataTableView.jsx     # Searchable records & instant CSV export
│   │   ├── data/
│   │   │   ├── agri_data.json        # Pre-calculated dual-slice metrics (with/without coconut)
│   │   │   └── india_states.json     # Cartography GeoJSON bundle
│   │   ├── App.jsx                   # Central state machine & view router
│   │   ├── soundEffects.js           # Web Audio API procedural synthesizer
│   │   ├── stateCapitals.js          # Lat/Lon coordinates for 30 state capitals
│   │   ├── utils.js                  # Number formatters & helpers
│   │   └── main.jsx
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── agronomy_data.py              # Authentic ICAR & NBSS&LUP crop and soil profiles
├── app.py                        # Streamlit base application
├── app_modern.py                 # Streamlit modern glassmorphism dashboard
├── crop_yield.csv                # Historical production dataset (19,689 rows, 1997–2020)
├── export_frontend_data.py       # Data pipeline exporting optimized JSON for React
├── requirements.txt              # Python dependencies
├── test_app_logic.py             # Automated test suite
├── .gitignore                    # Exclusions for node_modules, dist, and pycache
└── README.md                     # Documentation
```

---

## 🚀 Quickstart Guide

### 1. Run the Primary React Application (Recommended)
```powershell
cd d:\Agriculture_dashboard\frontend
npm install
npm run dev
```
👉 Open browser at: **`http://localhost:3000`**

### 2. Run the Python Streamlit Companion
```powershell
cd d:\Agriculture_dashboard
pip install -r requirements.txt
python -m streamlit run app_modern.py --server.port 8501
```
👉 Open browser at: **`http://localhost:8501`**

### 3. Re-generate Frontend Data Pipeline (Optional)
If you update `crop_yield.csv` or `agronomy_data.py`:
```powershell
python export_frontend_data.py
```

---

## 🔬 Scientific & Institutional Citations
- **ICAR:** Indian Council of Agricultural Research (*Handbook of Agriculture, 6th Edition*)
- **NBSS&LUP:** National Bureau of Soil Survey & Land Use Planning (Soils of India Series)
- **DES:** Directorate of Economics and Statistics, Ministry of Agriculture & Farmers Welfare
- **TNAU:** Tamil Nadu Agricultural University Agritech Portal (Crop Production Guide)
- **FAO:** Food and Agriculture Organization (*Irrigation and Drainage Paper No. 56 / 33*)
- **Open-Meteo:** Global Meteorological Organization open-access satellite weather API
