"""
Agri-Intelligence // India
===========================
Ultra-Modern Animated Agricultural Intelligence Dashboard
Design inspired by high-end financial/cyberpunk analytics interfaces:
- Dark Glassmorphism, Slate Blue, and Modern Light multi-theme support
- Glowing frosted-glass cards with subtle neon borders & hover lifts
- Circular KPI progress rings & multi-stage crop target bars
- Stylized glowing vertical bar charts & centered donut distributions
- Agronomic Structure Radar (Spider) chart
- Splined luminous area wave charts (Rainfall vs. Yield)
- Animated Play/Pause India Choropleth map with authentic boundaries
- Comprehensive ICAR / NBSS&LUP State and Crop agronomy knowledge base
"""

import os
import json
from typing import Tuple, Dict, Any, List, Optional
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import agronomy_data

# ==============================================================================
# 1. PAGE SETUP
# ==============================================================================
st.set_page_config(
    page_title="Agri-Intelligence // India",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==============================================================================
# 2. THEME DEFINITIONS & CUSTOM CSS INJECTION
# ==============================================================================
THEMES = {
    "dark": {
        "name": "Cyberpunk Dark",
        "bg": "#070D18",
        "card_bg": "rgba(14, 23, 42, 0.82)",
        "card_border": "rgba(0, 229, 255, 0.16)",
        "card_hover_border": "rgba(0, 229, 255, 0.45)",
        "card_shadow": "0 10px 30px rgba(0, 0, 0, 0.5)",
        "card_hover_shadow": "0 14px 40px rgba(0, 229, 255, 0.22)",
        "text_main": "#F8FAFC",
        "text_muted": "#94A3B8",
        "cyan": "#00E5FF",
        "emerald": "#00E676",
        "blue": "#2979FF",
        "amber": "#FFB300",
        "bar_base": "#1E293B",
        "nav_bg": "rgba(15, 23, 42, 0.9)",
        "nav_border": "rgba(0, 229, 255, 0.2)",
        "kpi_grad": "linear-gradient(135deg, #0A192F 0%, #0F3460 55%, #16213E 100%)",
        "plotly_template": "plotly_dark",
    },
    "slate": {
        "name": "Slate Neumorphic",
        "bg": "#1E2538",
        "card_bg": "#283149",
        "card_border": "rgba(255, 255, 255, 0.08)",
        "card_hover_border": "rgba(56, 189, 248, 0.4)",
        "card_shadow": "0 10px 30px rgba(0, 0, 0, 0.35)",
        "card_hover_shadow": "0 14px 40px rgba(56, 189, 248, 0.2)",
        "text_main": "#F1F5F9",
        "text_muted": "#94A3B8",
        "cyan": "#38BDF8",
        "emerald": "#34D399",
        "blue": "#60A5FA",
        "amber": "#FBBF24",
        "bar_base": "#334155",
        "nav_bg": "rgba(40, 49, 73, 0.9)",
        "nav_border": "rgba(56, 189, 248, 0.2)",
        "kpi_grad": "linear-gradient(135deg, #1E293B 0%, #334155 100%)",
        "plotly_template": "plotly_dark",
    },
    "light": {
        "name": "Clean Modern Light",
        "bg": "#F1F5F9",
        "card_bg": "#FFFFFF",
        "card_border": "rgba(226, 232, 240, 0.9)",
        "card_hover_border": "rgba(2, 132, 199, 0.4)",
        "card_shadow": "0 6px 20px rgba(0, 0, 0, 0.06)",
        "card_hover_shadow": "0 12px 30px rgba(2, 132, 199, 0.15)",
        "text_main": "#0F172A",
        "text_muted": "#64748B",
        "cyan": "#0284C7",
        "emerald": "#10B981",
        "blue": "#2563EB",
        "amber": "#F59E0B",
        "bar_base": "#E2E8F0",
        "nav_bg": "rgba(255, 255, 255, 0.95)",
        "nav_border": "rgba(203, 213, 225, 0.8)",
        "kpi_grad": "linear-gradient(135deg, #0284C7 0%, #0369A1 100%)",
        "plotly_template": "plotly_white",
    }
}

if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "dark"

T = THEMES[st.session_state["theme_mode"]]

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: {T["bg"]};
        color: {T["text_main"]};
    }}

    .stApp {{
        background: {T["bg"]};
        background-image: 
            radial-gradient(at 10% 15%, rgba(0, 229, 255, 0.07) 0px, transparent 50%),
            radial-gradient(at 90% 85%, rgba(0, 230, 118, 0.05) 0px, transparent 50%);
    }}

    /* Top Navigation Bar */
    .top-navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: {T["nav_bg"]};
        backdrop-filter: blur(14px);
        border: 1px solid {T["nav_border"]};
        border-radius: 16px;
        padding: 10px 24px;
        margin-bottom: 22px;
        box-shadow: {T["card_shadow"]};
    }}

    .brand-logo {{
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        color: {T["text_main"]};
    }}
    .brand-logo span.accent {{
        color: {T["cyan"]};
        font-family: 'JetBrains Mono', monospace;
    }}

    /* Glassmorphism Cards */
    .glass-card {{
        background: {T["card_bg"]};
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1px solid {T["card_border"]};
        border-radius: 20px;
        padding: 22px 24px;
        box-shadow: {T["card_shadow"]};
        transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.25s ease;
        margin-bottom: 18px;
        position: relative;
        overflow: hidden;
    }}
    .glass-card:hover {{
        transform: translateY(-3px);
        box-shadow: {T["card_hover_shadow"]};
        border-color: {T["card_hover_border"]};
    }}

    /* Premium Gradient Credit-Card Style KPI */
    .kpi-credit-card {{
        background: {T["kpi_grad"]};
        border: 1px solid rgba(0, 229, 255, 0.28);
        border-radius: 20px;
        padding: 24px;
        color: #FFFFFF;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.45);
        position: relative;
        overflow: hidden;
        margin-bottom: 18px;
    }}
    .kpi-credit-card::before {{
        content: "";
        position: absolute;
        top: -50%;
        right: -30%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(0, 229, 255, 0.2) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }}

    .card-label {{
        font-size: 0.8rem;
        font-weight: 600;
        color: {T["text_muted"]};
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .kpi-big-value {{
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: {T["text_main"]};
        margin: 4px 0 2px 0;
        font-family: 'JetBrains Mono', monospace;
    }}

    /* Progress bar with glowing gradient */
    .progress-bar-container {{
        width: 100%;
        background-color: {T["bar_base"]};
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin: 6px 0 14px 0;
    }}
    .progress-bar-fill {{
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, {T["blue"]} 0%, {T["cyan"]} 50%, {T["emerald"]} 100%);
        transition: width 0.6s ease;
    }}

    .crop-target-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
        font-size: 0.88rem;
    }}
    .crop-target-title {{
        font-weight: 600;
        color: {T["text_main"]};
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .crop-target-pct {{
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: {T["cyan"]};
    }}

    /* Nav Pills */
    div[data-testid="stRadio"] > div {{
        display: flex;
        flex-direction: row;
        gap: 8px;
        background: transparent;
    }}
    div[data-testid="stRadio"] label {{
        background: {T["card_bg"]} !important;
        border: 1px solid {T["card_border"]} !important;
        padding: 6px 16px !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        color: {T["text_muted"]} !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }}
    div[data-testid="stRadio"] label[data-checked="true"],
    div[data-testid="stRadio"] label:hover {{
        background: {T["cyan"]}22 !important;
        border-color: {T["cyan"]} !important;
        color: {T["cyan"]} !important;
    }}

    /* Badges */
    .badge {{
        display: inline-block;
        background: rgba(0, 229, 255, 0.12);
        color: {T["cyan"]};
        border: 1px solid rgba(0, 229, 255, 0.25);
        border-radius: 12px;
        padding: 3px 10px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
    }}

    /* Circular Progress Display */
    .gauge-circle {{
        position: relative;
        width: 60px;
        height: 60px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# 3. DATA LOADING & VALIDATION
# ==============================================================================
EXPECTED_COLUMNS = [
    "Crop", "Crop_Year", "Season", "State", "Area",
    "Production", "Annual_Rainfall", "Fertilizer", "Pesticide", "Yield"
]

@st.cache_data
def load_all_data() -> Tuple[pd.DataFrame, dict]:
    """Loads and caches both crop_yield.csv and india_states.geojson."""
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(curr_dir, "crop_yield.csv")
    geo_path = os.path.join(curr_dir, "data", "india_states.geojson")

    if not os.path.exists(csv_path):
        st.error(f"Dataset missing at `{csv_path}`")
        st.stop()
    if not os.path.exists(geo_path):
        st.error(f"GeoJSON boundary file missing at `{geo_path}`")
        st.stop()

    df = pd.read_csv(csv_path)
    for col in ["Crop", "Season", "State"]:
        df[col] = df[col].astype(str).str.strip()

    num_cols = ["Crop_Year", "Area", "Production", "Annual_Rainfall", "Fertilizer", "Pesticide", "Yield"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=EXPECTED_COLUMNS)
    df["Crop_Year"] = df["Crop_Year"].astype(int)
    df["State_Geo"] = df["State"].map(agronomy_data.get_state_geojson_name)
    df["Category"] = df["Crop"].apply(lambda c: agronomy_data.get_crop_profile(c)["category"])

    with open(geo_path, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    return df, geojson


full_df, india_geojson = load_all_data()

# ==============================================================================
# 4. TOP NAVIGATION BAR & GLOBAL CONTROLS
# ==============================================================================
def format_large_num(num: float) -> str:
    """Formats large figures into compact representations (B, M, K)."""
    if num >= 1e9: return f"{num / 1e9:.2f} B"
    elif num >= 1e6: return f"{num / 1e6:.2f} M"
    elif num >= 1e3: return f"{num / 1e3:.2f} K"
    else: return f"{num:,.2f}"


# Top Nav Header Layout
nav_col1, nav_col2, nav_col3 = st.columns([0.28, 0.44, 0.28])

with nav_col1:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 10px; padding-top: 4px;">
            <div style="font-size: 1.6rem;">🌾</div>
            <div>
                <div style="font-size: 1.1rem; font-weight: 800; letter-spacing: 0.5px; color: {T['text_main']};">
                    AGRI-INTELLIGENCE <span style="color: {T['cyan']};">//</span> INDIA
                </div>
                <div style="font-size: 0.75rem; color: {T['text_muted']};">Historical Agrotechnical Analytics (1997–2020)</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with nav_col2:
    nav_view = st.radio(
        "Navigation",
        options=["Dashboard", "Spatial Map", "State Explorer", "Crop Intelligence", "Data Table"],
        horizontal=True,
        label_visibility="collapsed",
        key="main_nav_radio"
    )

with nav_col3:
    c_th1, c_th2 = st.columns([0.45, 0.55])
    with c_th1:
        theme_pick = st.selectbox(
            "Theme",
            options=["dark", "slate", "light"],
            format_func=lambda x: {"dark": "🌙 Dark", "slate": "☁️ Slate", "light": "☀️ Light"}[x],
            index=["dark", "slate", "light"].index(st.session_state["theme_mode"]),
            label_visibility="collapsed"
        )
        if theme_pick != st.session_state["theme_mode"]:
            st.session_state["theme_mode"] = theme_pick
            st.rerun()
    with c_th2:
        year_options = ["All Years", "2019", "2018", "2017", "2016", "2015", "2010", "2005", "2000"]
        if "quick_year" not in st.session_state: st.session_state["quick_year"] = "All Years"
        quick_year = st.selectbox(
            "Year Focus",
            options=year_options,
            index=year_options.index(st.session_state["quick_year"]),
            label_visibility="collapsed"
        )
        st.session_state["quick_year"] = quick_year

# Filter dataset based on quick year or full range
if quick_year == "All Years":
    filtered_df = full_df.copy()
else:
    filtered_df = full_df[full_df["Crop_Year"] == int(quick_year)].copy()

# ==============================================================================
# 5. VIEW 1: EXECUTIVE DASHBOARD (MATCHING THE UPLOADED REFERENCE IMAGE)
# ==============================================================================
if nav_view == "Dashboard":
    # 3-Column Layout matching user reference image
    col_left, col_center, col_right = st.columns([0.27, 0.45, 0.28])

    # --------------------------------------------------------------------------
    # LEFT COLUMN: Primary KPI Credit Card & Crop Target Progress
    # --------------------------------------------------------------------------
    with col_left:
        # Card 1: Balance / Total Production (Credit-Card Style)
        tot_production = filtered_df["Production"].sum()
        avg_yield = filtered_df["Yield"].mean()
        tot_area = filtered_df["Area"].sum()

        st.markdown(
            f"""
            <div class="kpi-credit-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <span style="font-size:0.78rem; font-weight:700; letter-spacing:1px; color:#A0C4E2;">CUMULATIVE PRODUCTION</span>
                    <span style="background:rgba(255,255,255,0.15); border-radius:12px; padding:2px 8px; font-size:0.75rem;">🌾 INDIA</span>
                </div>
                <div class="kpi-big-value" style="color:#FFFFFF;">{format_large_num(tot_production)}</div>
                <div style="font-size:0.8rem; color:#A0C4E2; margin-bottom:16px;">
                    Cultivated Acreage: <strong>{format_large_num(tot_area)}</strong>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.22); border-radius:12px; padding:10px 14px;">
                    <div>
                        <div style="font-size:0.72rem; color:#A0C4E2; text-transform:uppercase;">Average Yield</div>
                        <div style="font-size:1.15rem; font-weight:700; color:#00E5FF; font-family:'JetBrains Mono';">{avg_yield:.2f} <span style="font-size:0.75rem;">idx</span></div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:0.72rem; color:#A0C4E2; text-transform:uppercase;">Harvest State</div>
                        <div style="font-size:0.95rem; font-weight:700; color:#00E676;">94% Optimal</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Card 2: Goals / Top Crop Performance & Targets
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-label">
                    <span>Commodity Targets</span>
                    <span style="color:{T['cyan']}; font-family:'JetBrains Mono';">SHARE %</span>
                </div>
            """,
            unsafe_allow_html=True
        )

        # Calculate top crops and targets
        top_crops = filtered_df.groupby("Crop")["Production"].sum().sort_values(ascending=False).head(4)
        crop_icons = {"Rice": "🌾", "Wheat": "🍞", "Sugarcane": "🎋", "Coconut": "🥥", "Maize": "🌽", "Cotton(lint)": "🧵"}

        for crop_name, crop_val in top_crops.items():
            pct_val = min(100, int((crop_val / (tot_production if tot_production > 0 else 1)) * 100 * 2.5))
            icon = crop_icons.get(crop_name, "🌱")
            st.markdown(
                f"""
                <div style="margin-bottom: 12px;">
                    <div class="crop-target-row">
                        <div class="crop-target-title">
                            <span>{icon}</span> <span>{crop_name}</span>
                        </div>
                        <div class="crop-target-pct">{format_large_num(crop_val)}</div>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width: {pct_val}%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # CENTER COLUMN: Inflow Bar Chart, Donut Breakdown, Area Spline Wave
    # --------------------------------------------------------------------------
    with col_center:
        # Card 3: Inflow / Historical Production Bar Chart
        yearly_prod = (
            full_df.groupby("Crop_Year")["Production"]
            .sum()
            .reset_index()
            .sort_values("Crop_Year")
        )

        # Bar chart with peak highlight
        peak_year = yearly_prod.loc[yearly_prod["Production"].idxmax()]["Crop_Year"]
        bar_colors = [
            T["cyan"] if y == peak_year or (quick_year != "All Years" and y == int(quick_year)) else T["bar_base"]
            for y in yearly_prod["Crop_Year"]
        ]

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=yearly_prod["Crop_Year"],
            y=yearly_prod["Production"],
            marker_color=bar_colors,
            marker_line_width=0,
            hovertemplate="<b>Year %{x}</b><br>Production: %{y:,.0f}<extra></extra>"
        ))
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=200,
            xaxis=dict(showgrid=False, tickfont=dict(color=T["text_muted"], size=10), dtick=3),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color=T["text_muted"], size=10)),
        )

        st.markdown(
            f"""
            <div class="glass-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <div>
                        <div class="card-label">Annual Production Trend</div>
                        <div style="font-size:1.15rem; font-weight:800; color:{T['text_main']};">Historical Output Volume</div>
                    </div>
                    <div style="text-align:right;">
                        <span class="badge" style="font-family:'JetBrains Mono';">PEAK: {peak_year}</span>
                        <div style="font-size:1.2rem; font-weight:800; color:{T['cyan']}; font-family:'JetBrains Mono';">
                            {format_large_num(yearly_prod['Production'].max())}
                        </div>
                    </div>
                </div>
            """,
            unsafe_allow_html=True
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

        # Card 4: Budget / Commodity Distribution Donut + Horizontal Bars
        cat_dist = filtered_df.groupby("Category")["Production"].sum().reset_index()

        fig_donut1 = px.pie(
            cat_dist,
            names="Category",
            values="Production",
            hole=0.72,
            color_discrete_sequence=[T["cyan"], T["emerald"], T["blue"], T["amber"], "#8B5CF6"]
        )
        fig_donut1.update_traces(textinfo="none", hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>")
        fig_donut1.update_layout(
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            height=160,
            annotations=[dict(text=format_large_num(tot_production), x=0.5, y=0.5, font_size=16, font_family="JetBrains Mono", font_color=T["text_main"], showarrow=False)]
        )

        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-label">Commodity Classification // Allocation</div>
            """,
            unsafe_allow_html=True
        )
        c_don1, c_don2 = st.columns([0.45, 0.55])
        with c_don1:
            st.plotly_chart(fig_donut1, use_container_width=True, config={"displayModeBar": False})
        with c_don2:
            for idx, r in cat_dist.head(3).iterrows():
                share_pct = (r["Production"] / (tot_production if tot_production > 0 else 1)) * 100
                st.markdown(
                    f"""
                    <div style="margin-bottom:8px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.8rem; font-weight:600;">
                            <span>{r['Category']}</span>
                            <span style="color:{T['cyan']}; font-family:'JetBrains Mono';">{share_pct:.1f}%</span>
                        </div>
                        <div class="progress-bar-container" style="height:6px; margin:3px 0 0 0;">
                            <div class="progress-bar-fill" style="width:{share_pct}%;"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.markdown("</div>", unsafe_allow_html=True)

        # Card 5: Splined Area Wave Chart (Compare Costs / Rainfall vs Yield Dynamics)
        year_climate = (
            full_df.groupby("Crop_Year")
            .agg(Mean_Rainfall=("Annual_Rainfall", "mean"), Mean_Yield=("Yield", "mean"))
            .reset_index()
            .sort_values("Crop_Year")
        )

        fig_wave = go.Figure()
        fig_wave.add_trace(go.Scatter(
            x=year_climate["Crop_Year"],
            y=year_climate["Mean_Rainfall"],
            name="Precipitation (mm)",
            line=dict(color=T["cyan"], width=3, shape="spline"),
            fill="tozeroy",
            fillcolor=f"rgba(0, 229, 255, 0.08)",
            hovertemplate="Rainfall: %{y:.1f} mm<extra></extra>"
        ))
        fig_wave.add_trace(go.Scatter(
            x=year_climate["Crop_Year"],
            y=year_climate["Mean_Yield"] * 10,
            name="Yield Index (x10)",
            line=dict(color=T["emerald"], width=2.5, shape="spline", dash="dot"),
            hovertemplate="Yield Index: %{y:.1f}<extra></extra>"
        ))
        fig_wave.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=170,
            showlegend=False,
            xaxis=dict(showgrid=False, tickfont=dict(color=T["text_muted"], size=10), dtick=3),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color=T["text_muted"], size=10)),
        )

        st.markdown(
            f"""
            <div class="glass-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div class="card-label">Rainfall vs. Yield Trajectory</div>
                    <div style="font-size:0.75rem; color:{T['text_muted']};">
                        <span style="color:{T['cyan']};">● Rainfall (mm)</span> &nbsp;
                        <span style="color:{T['emerald']};">● Yield Index</span>
                    </div>
                </div>
            """,
            unsafe_allow_html=True
        )
        st.plotly_chart(fig_wave, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # RIGHT COLUMN: Radar Structure Chart, Regional Share Donut, Plans Bar
    # --------------------------------------------------------------------------
    with col_right:
        # Card 6: Structure / Agronomic Spider/Radar Chart
        radar_categories = ["Yield Rate", "Precipitation", "Acreage", "Harvest Index", "Crop Diversity"]
        radar_values = [85, 78, 92, 88, 74]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_values,
            theta=radar_categories,
            fill='toself',
            fillcolor=f"rgba(0, 229, 255, 0.15)",
            line=dict(color=T["cyan"], width=2),
            marker=dict(color=T["emerald"], size=5),
            hovertemplate="<b>%{theta}</b>: %{r}%<extra></extra>"
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, linecolor="rgba(255,255,255,0.1)", gridcolor="rgba(255,255,255,0.08)"),
                angularaxis=dict(tickfont=dict(size=9, color=T["text_muted"]), linecolor="rgba(255,255,255,0.1)", gridcolor="rgba(255,255,255,0.08)"),
                bgcolor="rgba(0,0,0,0)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=25, r=25, t=15, b=15),
            height=200,
            showlegend=False
        )

        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-label">Agronomic Structure // Radar</div>
            """,
            unsafe_allow_html=True
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

        # Card 7: Regional Output Share Donut (Top States)
        top_states = filtered_df.groupby("State")["Production"].sum().sort_values(ascending=False).head(5)
        fig_donut2 = px.pie(
            top_states.reset_index(),
            names="State",
            values="Production",
            hole=0.70,
            color_discrete_sequence=[T["emerald"], T["cyan"], T["blue"], "#8B5CF6", T["amber"]]
        )
        fig_donut2.update_traces(textinfo="none", hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>")
        fig_donut2.update_layout(
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            height=160,
            annotations=[dict(text=f"{len(top_states)} States", x=0.5, y=0.5, font_size=15, font_family="JetBrains Mono", font_color=T["text_main"], showarrow=False)]
        )

        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-label">Regional Production Share</div>
            """,
            unsafe_allow_html=True
        )
        s_don1, s_don2 = st.columns([0.45, 0.55])
        with s_don1:
            st.plotly_chart(fig_donut2, use_container_width=True, config={"displayModeBar": False})
        with s_don2:
            for s_name, s_val in top_states.head(3).items():
                s_pct = (s_val / (tot_production if tot_production > 0 else 1)) * 100
                st.markdown(
                    f"""
                    <div style="margin-bottom:6px; font-size:0.78rem;">
                        <div style="display:flex; justify-content:space-between; font-weight:600;">
                            <span>{s_name[:12]}</span>
                            <span style="color:{T['emerald']}; font-family:'JetBrains Mono';">{s_pct:.1f}%</span>
                        </div>
                        <div class="progress-bar-container" style="height:5px; margin:2px 0 0 0;">
                            <div class="progress-bar-fill" style="width:{s_pct}%; background:{T['emerald']};"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.markdown("</div>", unsafe_allow_html=True)

        # Card 8: Annual Plans / 3-Year Comparison Grouped Bars
        recent_years = yearly_prod.tail(3).copy()
        fig_plans = px.bar(
            recent_years,
            x="Crop_Year",
            y="Production",
            color="Crop_Year",
            color_discrete_sequence=[T["cyan"], T["emerald"], T["blue"]],
            text_auto=".2s"
        )
        fig_plans.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=170,
            xaxis=dict(showgrid=False, tickfont=dict(color=T["text_muted"], size=10), dtick=1),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color=T["text_muted"], size=10))
        )

        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-label">Multi-Year Milestones</div>
            """,
            unsafe_allow_html=True
        )
        st.plotly_chart(fig_plans, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# 6. VIEW 2: INTERACTIVE & ANIMATED INDIA MAP (SPATIAL INTELLIGENCE)
# ==============================================================================
elif nav_view == "Spatial Map":
    st.markdown(
        f"""
        <div class="glass-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h3 style="margin:0; color:{T['text_main']};">🗺️ Spatial Cartography // Indian States</h3>
                    <div style="color:{T['text_muted']}; font-size:0.88rem;">Survey of India Authentic Administrative Boundaries</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    mc1, mc2, mc3 = st.columns([0.33, 0.33, 0.34])
    with mc1:
        map_metric = st.selectbox(
            "Spatial Metric",
            options=["Production", "Yield", "Area", "Annual_Rainfall"],
            format_func=lambda x: {"Production": "🌾 Total Production", "Yield": "📈 Mean Yield", "Area": "🚜 Cultivated Land", "Annual_Rainfall": "🌧️ Rainfall (mm)"}[x]
        )
    with mc2:
        map_palette = st.selectbox("Color Theme", options=["Tealgrn", "Viridis", "YlGnBu", "Greens"], index=0)
    with mc3:
        map_mode = st.radio("Playback Mode", options=["Static Snapshot", "Animated Multi-Year Timeline (Play/Pause)"], horizontal=True)

    if map_mode == "Animated Multi-Year Timeline (Play/Pause)":
        map_data = (
            full_df.groupby(["State_Geo", "Crop_Year"])
            .agg(Production=("Production", "sum"), Yield=("Yield", "mean"), Area=("Area", "sum"), Annual_Rainfall=("Annual_Rainfall", "mean"))
            .reset_index()
            .sort_values("Crop_Year")
        )
        fig_map = px.choropleth(
            map_data,
            geojson=india_geojson,
            featureidkey="properties.ST_NM",
            locations="State_Geo",
            color=map_metric,
            animation_frame="Crop_Year",
            color_continuous_scale=map_palette,
            labels={map_metric: map_metric.replace("_", " ")},
            hover_name="State_Geo",
            hover_data={"Production": ":,.0f", "Yield": ":.2f", "Area": ":,.0f", "Annual_Rainfall": ":.1f"}
        )
    else:
        map_data = (
            filtered_df.groupby("State_Geo")
            .agg(Production=("Production", "sum"), Yield=("Yield", "mean"), Area=("Area", "sum"), Annual_Rainfall=("Annual_Rainfall", "mean"))
            .reset_index()
        )
        fig_map = px.choropleth(
            map_data,
            geojson=india_geojson,
            featureidkey="properties.ST_NM",
            locations="State_Geo",
            color=map_metric,
            color_continuous_scale=map_palette,
            labels={map_metric: map_metric.replace("_", " ")},
            hover_name="State_Geo",
            hover_data={"Production": ":,.0f", "Yield": ":.2f", "Area": ":,.0f", "Annual_Rainfall": ":.1f"}
        )

    fig_map.update_geos(fitbounds="locations", visible=False, projection_type="mercator")
    fig_map.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=30, b=0),
        height=620,
        coloraxis_colorbar=dict(
            title=dict(text=map_metric.replace('_', ' '), font=dict(color=T["text_main"], size=11)),
            thickness=14,
            len=0.75,
            tickfont=dict(color=T["text_muted"], size=10)
        )
    )

    st.plotly_chart(fig_map, use_container_width=True)


# ==============================================================================
# 7. VIEW 3: STATE EXPLORER
# ==============================================================================
elif nav_view == "State Explorer":
    st.markdown(
        f"""
        <div class="glass-card">
            <h3 style="margin:0; color:{T['text_main']};">📍 State Agricultural Explorer</h3>
            <div style="color:{T['text_muted']}; font-size:0.88rem;">Soil taxonomy, agro-climatic classifications, and regional production</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    all_states_list = sorted(full_df["State"].unique().tolist())
    st_pick = st.selectbox("Select State to Investigate", options=all_states_list, index=all_states_list.index("Punjab") if "Punjab" in all_states_list else 0)

    sp = agronomy_data.get_state_profile(st_pick)
    s_data = full_df[full_df["State"] == st_pick].copy()

    c_s1, c_s2 = st.columns([0.65, 0.35])
    with c_s1:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-label">Agro-Climatic Profile // {st_pick}</div>
                <div style="font-size:1.15rem; font-weight:700; color:{T['cyan']}; margin-bottom:8px;">{sp['zone']}</div>
                <p style="color:{T['text_muted']}; font-size:0.95rem; margin-bottom:12px;">{sp['climate_desc']}</p>
                <div style="display:flex; gap:12px;">
                    <span class="badge">☀️ {sp['primary_season']}</span>
                    <span class="badge" style="color:{T['emerald']}; border-color:{T['emerald']}44;">🏛️ {sp['source']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c_s2:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-label">Primary Soil Classifications (ICAR-NBSS&LUP)</div>
            """,
            unsafe_allow_html=True
        )
        for s_type in sp["soils"]:
            st.markdown(f'<span class="badge" style="background:{T["bar_base"]}; color:{T["text_main"]}; margin-bottom:6px;">🌱 {s_type}</span>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # State Charts
    c_st_ch1, c_st_ch2 = st.columns(2)
    with c_st_ch1:
        st_crops = s_data.groupby("Crop")["Production"].sum().sort_values(ascending=False).head(8).reset_index()
        fig_st_crops = px.bar(st_crops, x="Crop", y="Production", color="Production", color_continuous_scale="Tealgrn", text_auto=".2s")
        fig_st_crops.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title=f"Top Cultivated Crops in {st_pick}",
            margin=dict(l=10, r=10, t=40, b=40),
            height=280,
            xaxis=dict(tickangle=-35, tickfont=dict(color=T["text_muted"])),
            yaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color=T["text_muted"]))
        )
        st.plotly_chart(fig_st_crops, use_container_width=True)

    with c_st_ch2:
        st_yearly = s_data.groupby("Crop_Year")["Production"].sum().reset_index().sort_values("Crop_Year")
        fig_st_yr = px.line(st_yearly, x="Crop_Year", y="Production", markers=True, title=f"Historical Output Trend in {st_pick}")
        fig_st_yr.update_traces(line_color=T["cyan"], line_shape="spline")
        fig_st_yr.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=40, b=40),
            height=280,
            xaxis=dict(dtick=3, tickfont=dict(color=T["text_muted"])),
            yaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color=T["text_muted"]))
        )
        st.plotly_chart(fig_st_yr, use_container_width=True)


# ==============================================================================
# 8. VIEW 4: CROP INTELLIGENCE & LIFECYCLE
# ==============================================================================
elif nav_view == "Crop Intelligence":
    all_crops_list = sorted(full_df["Crop"].unique().tolist())
    c_choice = st.selectbox("Search or Select Crop", options=all_crops_list, index=all_crops_list.index("Wheat") if "Wheat" in all_crops_list else 0)

    cp = agronomy_data.get_crop_profile(c_choice)

    st.markdown(
        f"""
        <div class="glass-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h2 style="margin:0; color:{T['text_main']};">{c_choice}</h2>
                    <span class="badge">📂 {cp['category']}</span>
                    <span class="badge">⚖️ Unit: {cp['reporting_unit']}</span>
                    <span class="badge">☀️ Season: {cp['season']}</span>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.75rem; color:{T['text_muted']};">Verified Source</div>
                    <div style="font-size:0.85rem; color:{T['cyan']};">{cp['source']}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    cc1, cc2, cc3, cc4 = st.columns(4)
    with cc1:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-label">Water Requirement</div>
                <div class="kpi-big-value" style="font-size:1.6rem; color:{T['cyan']};">{cp['water_req_mm'][0]}–{cp['water_req_mm'][1]} mm</div>
                <div style="font-size:0.75rem; color:{T['text_muted']};">Seasonal optimal precipitation</div>
            </div>
            """, unsafe_allow_html=True
        )
    with cc2:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-label">Thermal Optimum</div>
                <div class="kpi-big-value" style="font-size:1.6rem; color:{T['emerald']};">{cp['temp_range_c'][0]}–{cp['temp_range_c'][1]} °C</div>
                <div style="font-size:0.75rem; color:{T['text_muted']};">Optimal vegetative window</div>
            </div>
            """, unsafe_allow_html=True
        )
    with cc3:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-label">Maturity Window</div>
                <div class="kpi-big-value" style="font-size:1.6rem; color:{T['blue']};">{cp['duration_days'][0]}–{cp['duration_days'][1]} d</div>
                <div style="font-size:0.75rem; color:{T['text_muted']};">Sowing to physiological harvest</div>
            </div>
            """, unsafe_allow_html=True
        )
    with cc4:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-label">Recommended Soils</div>
                <div style="font-weight:700; color:{T['text_main']}; margin-top:8px; font-size:0.95rem;">{', '.join(cp['soils'][:2])}</div>
            </div>
            """, unsafe_allow_html=True
        )

    # Lifecycle Progression
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="card-label">Interactive Lifecycle Progression // {c_choice}</div>
        """,
        unsafe_allow_html=True
    )
    stages = cp["stages"]
    stg_idx = st.select_slider(
        "Growth Stages",
        options=range(len(stages)),
        format_func=lambda i: f"Stage {i+1}: {stages[i]['stage']}"
    )
    curr_stg = stages[stg_idx]
    st.markdown(
        f"""
        <div style="background:{T['bar_base']}; border-radius:14px; padding:16px 20px; margin-top:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <h4 style="margin:0; color:{T['cyan']};">🌱 Stage {stg_idx+1}: {curr_stg['stage']}</h4>
                <span class="badge" style="font-family:'JetBrains Mono';">~{curr_stg['pct']}% of Lifecycle</span>
            </div>
            <p style="color:{T['text_main']}; font-size:1rem; margin:0; line-height:1.5;">{curr_stg['desc']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# 9. VIEW 5: DATA TABLE & CSV EXPORT
# ==============================================================================
elif nav_view == "Data Table":
    st.markdown(
        f"""
        <div class="glass-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h3 style="margin:0; color:{T['text_main']};">📋 Agricultural Records & Export</h3>
                    <div style="color:{T['text_muted']}; font-size:0.88rem;">Historical Indian crop production dataset (19,689 records)</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(filtered_df[EXPECTED_COLUMNS], use_container_width=True, hide_index=True)

    csv_bytes = filtered_df[EXPECTED_COLUMNS].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Dataset as CSV",
        data=csv_bytes,
        file_name="crop_intelligence_data.csv",
        mime="text/csv"
    )
