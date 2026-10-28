"""
Agriculture and Crop Production Intelligence Dashboard for India
================================================================
An interactive, animated, and intelligence-driven platform for exploring
Indian agricultural records (1997-2020), spatial distributions, state profiles,
and agronomic benchmarks.

Technologies: Streamlit, Pandas, Plotly Express & Graph Objects.
Agronomic Data: ICAR, NBSS&LUP, DES Ministry of Agriculture, TNAU, FAO.
Boundary Data: Authentic Survey of India / Standard Administrative GeoJSON.
"""

import os
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from typing import Tuple, Dict, Any, List, Optional
import agronomy_data

# ==============================================================================
# 1. PAGE SETUP & SOPHISTICATED AGRONOMIC STYLING
# ==============================================================================
st.set_page_config(
    page_title="Indian Agriculture Intelligence Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Palette: Forest green (#1B5E20, #2E7D32), Sage (#81C784, #E8F5E9), Warm neutral (#F9FBF7) */
    .main-title {
        color: #1B3B1B;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        margin-bottom: 2px;
    }
    .sub-title {
        color: #4A634A;
        font-size: 1.05rem;
        margin-bottom: 16px;
    }
    .metric-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F5F9F4 100%);
        border: 1px solid #D8E6D6;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        margin-bottom: 14px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(46, 125, 50, 0.12);
    }
    .metric-title {
        color: #557255;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .metric-value {
        color: #1B4D1B;
        font-size: 1.85rem;
        font-weight: 700;
        margin: 0;
    }
    .metric-subtitle {
        color: #6C826C;
        font-size: 0.82rem;
        margin-top: 4px;
    }
    .badge {
        display: inline-block;
        background-color: #E8F5E9;
        color: #1B5E20;
        border: 1px solid #C8E6C9;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 2px 4px 2px 0;
    }
    .badge-soil {
        background-color: #FFF8E1;
        color: #795548;
        border: 1px solid #FFE082;
    }
    .badge-stage {
        background-color: #E1F5FE;
        color: #0277BD;
        border: 1px solid #81D4FA;
    }
    .insight-box {
        background-color: #F3F8F2;
        border-left: 4px solid #2E7D32;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 12px;
        color: #1B3B1B;
        font-size: 0.95rem;
    }
    .notice-box {
        background-color: #FFFDE7;
        border-left: 4px solid #FBC02D;
        border-radius: 6px;
        padding: 12px 16px;
        font-size: 0.90rem;
        color: #5D4037;
        margin: 12px 0;
    }
    .lifecycle-container {
        background: #FFFFFF;
        border: 1px solid #E0EADE;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# 2. DATA INGESTION & BOUNDARY CACHING
# ==============================================================================
EXPECTED_COLUMNS = [
    "Crop", "Crop_Year", "Season", "State", "Area",
    "Production", "Annual_Rainfall", "Fertilizer", "Pesticide", "Yield"
]

@st.cache_data
def load_historical_data(filepath: str) -> pd.DataFrame:
    """Loads and cleans the 1997-2020 Indian crop production dataset."""
    if not os.path.exists(filepath):
        st.error(f"Dataset not found at `{filepath}`.")
        st.stop()

    df = pd.read_csv(filepath)

    # Clean text columns
    for col in ["Crop", "Season", "State"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Enforce numeric types
    num_cols = ["Crop_Year", "Area", "Production", "Annual_Rainfall", "Fertilizer", "Pesticide", "Yield"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=EXPECTED_COLUMNS)
    df["Crop_Year"] = df["Crop_Year"].astype(int)

    # Pre-calculate state name for GeoJSON matching
    df["State_Geo"] = df["State"].map(agronomy_data.get_state_geojson_name)

    # Add agronomic category tagging
    def get_cat(crop_name):
        return agronomy_data.get_crop_profile(crop_name)["category"]
    df["Category"] = df["Crop"].apply(get_cat)

    return df


@st.cache_data
def load_india_geojson(filepath: str) -> dict:
    """Loads and caches authentic Indian State boundary GeoJSON."""
    if not os.path.exists(filepath):
        st.error(f"GeoJSON boundary file not found at `{filepath}`.")
        st.stop()
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# ==============================================================================
# 3. SIDEBAR FILTERS WITH RESET & CATEGORY TOGGLE
# ==============================================================================
def render_sidebar_filters(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    """Renders interactive multi-criteria filters and returns filtered data and filter states."""
    st.sidebar.header("🔍 Agricultural Filters")

    min_yr = int(df["Crop_Year"].min())
    max_yr = int(df["Crop_Year"].max())

    all_categories = ["All Categories"] + sorted(df["Category"].unique().tolist())
    all_crops = sorted(df["Crop"].unique().tolist())
    all_states = sorted(df["State"].unique().tolist())
    all_seasons = sorted(df["Season"].unique().tolist())

    # Session State initializations
    if "f_yr" not in st.session_state: st.session_state["f_yr"] = (min_yr, max_yr)
    if "f_cat" not in st.session_state: st.session_state["f_cat"] = "All Categories"
    if "f_crops" not in st.session_state: st.session_state["f_crops"] = all_crops
    if "f_states" not in st.session_state: st.session_state["f_states"] = all_states
    if "f_seasons" not in st.session_state: st.session_state["f_seasons"] = all_seasons
    if "selected_state" not in st.session_state: st.session_state["selected_state"] = "Punjab"
    if "selected_crop" not in st.session_state: st.session_state["selected_crop"] = "Wheat"

    # Reset Button
    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
        st.session_state["f_yr"] = (min_yr, max_yr)
        st.session_state["f_cat"] = "All Categories"
        st.session_state["f_crops"] = all_crops
        st.session_state["f_states"] = all_states
        st.session_state["f_seasons"] = all_seasons
        st.session_state["selected_state"] = "Punjab"
        st.session_state["selected_crop"] = "Wheat"
        st.rerun()

    # 1. Year Range Slider
    year_range = st.sidebar.slider(
        "📅 Crop Year Range",
        min_value=min_yr,
        max_value=max_yr,
        value=st.session_state["f_yr"],
        step=1,
        help="Select multi-year range (1997–2020)."
    )
    st.session_state["f_yr"] = year_range

    st.sidebar.markdown("---")

    # 2. Crop Category Filter (Unit awareness helper)
    chosen_cat = st.sidebar.selectbox(
        "🌾 Crop Classification",
        options=all_categories,
        index=all_categories.index(st.session_state["f_cat"]),
        help="Filter crops by commodity group to avoid mixing distinct reporting units (e.g. Grain Tonnes vs. Coconut Nuts)."
    )
    st.session_state["f_cat"] = chosen_cat

    # Dynamic crop options based on category
    if chosen_cat == "All Categories":
        available_crops = all_crops
    else:
        available_crops = sorted(df[df["Category"] == chosen_cat]["Crop"].unique().tolist())

    # Crop multi-select
    col_c1, col_c2 = st.sidebar.columns(2)
    with col_c1:
        if st.button("All Crops", key="btn_sel_all_crops"):
            st.session_state["f_crops"] = available_crops
            st.rerun()
    with col_c2:
        if st.button("Clear", key="btn_clear_crops"):
            st.session_state["f_crops"] = []
            st.rerun()

    valid_selected_crops = [c for c in st.session_state["f_crops"] if c in available_crops]
    selected_crops = st.sidebar.multiselect(
        "🌱 Specific Crops",
        options=available_crops,
        default=valid_selected_crops if valid_selected_crops else available_crops,
        help="Choose specific crops to include."
    )
    st.session_state["f_crops"] = selected_crops

    st.sidebar.markdown("---")

    # 3. State Filter
    col_s1, col_s2 = st.sidebar.columns(2)
    with col_s1:
        if st.button("All States", key="btn_sel_all_states"):
            st.session_state["f_states"] = all_states
            st.rerun()
    with col_s2:
        if st.button("Clear", key="btn_clear_states"):
            st.session_state["f_states"] = []
            st.rerun()

    selected_states = st.sidebar.multiselect(
        "📍 States & UTs",
        options=all_states,
        default=st.session_state["f_states"],
        help="Filter by Indian states."
    )
    st.session_state["f_states"] = selected_states

    st.sidebar.markdown("---")

    # 4. Season Filter
    col_sn1, col_sn2 = st.sidebar.columns(2)
    with col_sn1:
        if st.button("All Seasons", key="btn_sel_all_seasons"):
            st.session_state["f_seasons"] = all_seasons
            st.rerun()
    with col_sn2:
        if st.button("Clear", key="btn_clear_seasons"):
            st.session_state["f_seasons"] = []
            st.rerun()

    selected_seasons = st.sidebar.multiselect(
        "⛅ Seasons",
        options=all_seasons,
        default=st.session_state["f_seasons"],
        help="Filter by agricultural seasons."
    )
    st.session_state["f_seasons"] = selected_seasons

    # Execute filtering
    mask = (
        (df["Crop_Year"] >= year_range[0]) &
        (df["Crop_Year"] <= year_range[1]) &
        (df["Crop"].isin(selected_crops)) &
        (df["State"].isin(selected_states)) &
        (df["Season"].isin(selected_seasons))
    )
    filtered_df = df[mask].copy()

    meta = {
        "year_range": year_range,
        "selected_crops": selected_crops,
        "selected_states": selected_states,
        "selected_seasons": selected_seasons,
        "category": chosen_cat
    }

    return filtered_df, meta


# ==============================================================================
# 4. KPI CARDS
# ==============================================================================
def format_large_number(num: float) -> str:
    """Formats large totals into compact, readable strings."""
    if num >= 1e9: return f"{num / 1e9:.2f} B"
    elif num >= 1e6: return f"{num / 1e6:.2f} M"
    elif num >= 1e3: return f"{num / 1e3:.2f} K"
    else: return f"{num:,.2f}"


def render_kpi_banner(filtered_df: pd.DataFrame, meta: dict):
    """Renders clean metric cards dynamically calculated from active filters."""
    if filtered_df.empty:
        total_prod = 0.0
        avg_yield = 0.0
        tot_area = 0.0
        states_cnt = 0
        crops_cnt = 0
    else:
        total_prod = filtered_df["Production"].sum()
        avg_yield = filtered_df["Yield"].mean()
        tot_area = filtered_df["Area"].sum()
        states_cnt = filtered_df["State"].nunique()
        crops_cnt = filtered_df["Crop"].nunique()

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title">Total Production</div>
                <div class="metric-value">{format_large_number(total_prod)}</div>
                <div class="metric-subtitle">Exact: {total_prod:,.0f} units</div>
            </div>""", unsafe_allow_html=True
        )
    with k2:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title">Mean Crop Yield</div>
                <div class="metric-value">{avg_yield:,.2f}</div>
                <div class="metric-subtitle">Output / Land Area index</div>
            </div>""", unsafe_allow_html=True
        )
    with k3:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title">Cultivated Area</div>
                <div class="metric-value">{format_large_number(tot_area)}</div>
                <div class="metric-subtitle">Sum of recorded acreage</div>
            </div>""", unsafe_allow_html=True
        )
    with k4:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title">Active States</div>
                <div class="metric-value">{states_cnt}</div>
                <div class="metric-subtitle">Out of 30 surveyed</div>
            </div>""", unsafe_allow_html=True
        )
    with k5:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title">Crops Filtered</div>
                <div class="metric-value">{crops_cnt}</div>
                <div class="metric-subtitle">Active varieties</div>
            </div>""", unsafe_allow_html=True
        )


# ==============================================================================
# 5. FEATURE 1 & 4: INTERACTIVE & ANIMATED INDIA MAP
# ==============================================================================
def render_interactive_map(filtered_df: pd.DataFrame, geojson_data: dict, full_df: pd.DataFrame):
    """
    Renders an interactive Choropleth of Indian states with authentic boundaries,
    metric selection, hover tooltips, and Play/Pause animated timeline across years.
    """
    st.subheader("🗺️ Interactive Agricultural Map of India")

    m_col1, m_col2, m_col3 = st.columns([0.35, 0.35, 0.30])
    with m_col1:
        metric_choice = st.selectbox(
            "Visualized Metric",
            options=["Production", "Yield", "Area", "Annual_Rainfall"],
            format_func=lambda x: {
                "Production": "🌾 Total Production",
                "Yield": "📈 Average Yield",
                "Area": "🚜 Cultivated Area",
                "Annual_Rainfall": "🌧️ Annual Rainfall (mm)"
            }[x]
        )
    with m_col2:
        color_palette = st.selectbox(
            "Color Theme",
            options=["Greens", "Viridis", "YlGnBu", "Tealgrn"],
            index=0
        )
    with m_col3:
        anim_mode = st.radio(
            "Display Mode",
            options=["Static Snapshot (Filtered Range)", "Animated Timeline (Play/Pause)"],
            horizontal=True
        )

    if filtered_df.empty:
        st.warning("No records match the current filter criteria to display on the map.")
        return

    # Aggregate by State
    agg_dict = {
        "Production": "sum",
        "Yield": "mean",
        "Area": "sum",
        "Annual_Rainfall": "mean"
    }

    if anim_mode == "Animated Timeline (Play/Pause)":
        # Group by State_Geo and Crop_Year
        map_data = (
            filtered_df.groupby(["State_Geo", "Crop_Year"])
            .agg(agg_dict)
            .reset_index()
            .sort_values("Crop_Year")
        )

        fig = px.choropleth(
            map_data,
            geojson=geojson_data,
            featureidkey="properties.ST_NM",
            locations="State_Geo",
            color=metric_choice,
            animation_frame="Crop_Year",
            color_continuous_scale=color_palette,
            title=f"Animated Year-by-Year {metric_choice} Across Indian States",
            labels={metric_choice: metric_choice.replace('_', ' ')},
            hover_name="State_Geo",
            hover_data={
                "Production": ":,.0f",
                "Yield": ":.2f",
                "Area": ":,.0f",
                "Annual_Rainfall": ":.1f",
                "Crop_Year": True
            }
        )
    else:
        # Static aggregate across selected years
        map_data = (
            filtered_df.groupby("State_Geo")
            .agg(agg_dict)
            .reset_index()
        )

        fig = px.choropleth(
            map_data,
            geojson=geojson_data,
            featureidkey="properties.ST_NM",
            locations="State_Geo",
            color=metric_choice,
            color_continuous_scale=color_palette,
            title=f"Cumulative {metric_choice} Across Indian States (Filtered Range)",
            labels={metric_choice: metric_choice.replace('_', ' ')},
            hover_name="State_Geo",
            hover_data={
                "Production": ":,.0f",
                "Yield": ":.2f",
                "Area": ":,.0f",
                "Annual_Rainfall": ":.1f"
            }
        )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator"
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor="#FFFFFF",
        height=620,
        coloraxis_colorbar=dict(
            title=metric_choice.replace('_', ' '),
            thickness=16,
            len=0.75
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # State Selector Quick-Link
    st.markdown("#### 📍 Explore a State Directly from the Map")
    state_options = sorted(filtered_df["State"].unique().tolist())
    curr_state = st.session_state.get("selected_state", state_options[0] if state_options else "Punjab")
    if curr_state not in state_options and state_options:
        curr_state = state_options[0]

    chosen_st = st.selectbox(
        "Select state to inspect in the **State Explorer** tab:",
        options=state_options,
        index=state_options.index(curr_state) if curr_state in state_options else 0,
        key="map_state_quickselect"
    )
    st.session_state["selected_state"] = chosen_st
    st.info(f"👉 Click the **📍 State Explorer** tab above to view deep agronomic analysis for **{chosen_st}**.")


# ==============================================================================
# 6. FEATURE 2: STATE EXPLORER
# ==============================================================================
def render_state_explorer(full_df: pd.DataFrame, filtered_df: pd.DataFrame):
    """
    Renders comprehensive state-level agronomic intelligence:
    - Primary soil types from ICAR-NBSS&LUP
    - Agro-climatic zone and climate profile
    - State-specific crop rankings and historical trends
    - Water requirements of major crops in this state
    """
    st.subheader("📍 Indian State Agricultural Explorer")

    all_states = sorted(full_df["State"].unique().tolist())
    def_state = st.session_state.get("selected_state", "Punjab")
    if def_state not in all_states:
        def_state = all_states[0]

    state_name = st.selectbox(
        "Choose an Indian State or Union Territory to inspect:",
        options=all_states,
        index=all_states.index(def_state),
        key="state_explorer_dropdown"
    )
    st.session_state["selected_state"] = state_name

    # Fetch authentic ICAR-NBSS&LUP State profile
    sp = agronomy_data.get_state_profile(state_name)

    # State Overview Banner
    col_so1, col_so2 = st.columns([0.65, 0.35])
    with col_so1:
        st.markdown(f"### Agriculture in {state_name}")
        st.markdown(f"**Agro-Climatic Zone:** {sp['zone']}")
        st.markdown(f"**Climate Profile:** {sp['climate_desc']}")
        st.markdown(f"**Primary Cultivation Season:** {sp['primary_season']}")
        st.caption(f"Source: {sp['source']}")
    with col_so2:
        st.markdown("**Dominant Soil Classifications (ICAR-NBSS&LUP):**")
        for soil in sp["soils"]:
            st.markdown(f'<span class="badge badge-soil">🌱 {soil}</span>', unsafe_allow_html=True)

    st.markdown("---")

    # State-specific historical data
    state_df = full_df[full_df["State"] == state_name].copy()
    if state_df.empty:
        st.warning(f"No historical records found for {state_name}.")
        return

    # State KPI Metrics
    st_prod = state_df["Production"].sum()
    st_yield = state_df["Yield"].mean()
    st_rain = state_df["Annual_Rainfall"].mean()
    st_crops = state_df["Crop"].nunique()

    k_s1, k_s2, k_s3, k_s4 = st.columns(4)
    with k_s1:
        st.metric("State Total Production", format_large_number(st_prod))
    with k_s2:
        st.metric("Average Yield", f"{st_yield:.2f}")
    with k_s3:
        st.metric("Mean Annual Rainfall", f"{st_rain:.1f} mm")
    with k_s4:
        st.metric("Recorded Crop Varieties", f"{st_crops} crops")

    st.markdown("---")

    # State Charts Layout
    sc1, sc2 = st.columns(2)

    with sc1:
        st.markdown(f"#### 🌾 Leading Crops in {state_name} by Production")
        st_crop_sum = (
            state_df.groupby("Crop")["Production"]
            .sum()
            .reset_index()
            .sort_values("Production", ascending=False)
            .head(10)
        )
        fig_st_crop = px.bar(
            st_crop_sum,
            x="Crop",
            y="Production",
            color="Production",
            color_continuous_scale="Greens",
            text_auto=".2s",
            title=f"Top 10 Crops by Total Production in {state_name}"
        )
        fig_st_crop.update_layout(
            xaxis_tickangle=-40,
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            margin=dict(l=20, r=20, t=40, b=60),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_st_crop, use_container_width=True)

    with sc2:
        st.markdown(f"#### 📈 Historical Production & Rainfall Trend in {state_name}")
        st_yearly = (
            state_df.groupby("Crop_Year")
            .agg(Production=("Production", "sum"), Rainfall=("Annual_Rainfall", "mean"))
            .reset_index()
            .sort_values("Crop_Year")
        )
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=st_yearly["Crop_Year"],
            y=st_yearly["Production"],
            name="Production",
            line=dict(color="#2E7D32", width=3),
            mode="lines+markers"
        ))
        fig_trend.update_layout(
            title=f"Annual Production in {state_name} (1997–2020)",
            xaxis=dict(title="Harvest Year", dtick=2),
            yaxis=dict(title="Production"),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            margin=dict(l=20, r=20, t=40, b=40)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    # State Crop Agronomic Table
    st.markdown(f"#### 📋 Agronomic Suitability for Major Crops Grown in {state_name}")
    major_crops_in_state = st_crop_sum["Crop"].tolist()

    records = []
    for crop in major_crops_in_state:
        p = agronomy_data.get_crop_profile(crop)
        actual_yield = state_df[state_df["Crop"] == crop]["Yield"].mean()
        records.append({
            "Crop": crop,
            "Category": p["category"],
            "State Avg Yield": f"{actual_yield:.2f}",
            "Water Need (mm)": f"{p['water_req_mm'][0]} – {p['water_req_mm'][1]}",
            "Optimal Temp (°C)": f"{p['temp_range_c'][0]} – {p['temp_range_c'][1]}",
            "Maturity (Days)": f"{p['duration_days'][0]} – {p['duration_days'][1]}",
            "Recommended Soils": ", ".join(p["soils"][:2]),
            "Benchmark Source": p["source"]
        })

    st.dataframe(pd.DataFrame(records), use_container_width=True, hide_index=True)


# ==============================================================================
# 7. FEATURE 3 & 4: CROP INTELLIGENCE & LIFECYCLE VISUALIZER
# ==============================================================================
def render_crop_intelligence(full_df: pd.DataFrame):
    """
    Renders searchable crop explorer, scientific agronomic profile,
    crop lifecycle animation/stage visualizer, and water requirements vs. rainfall.
    """
    st.subheader("🌱 Crop Intelligence & Lifecycle Explorer")

    all_crops = sorted(full_df["Crop"].unique().tolist())
    def_crop = st.session_state.get("selected_crop", "Wheat")
    if def_crop not in all_crops:
        def_crop = all_crops[0]

    chosen_crop = st.selectbox(
        "Search or select an agricultural crop to investigate:",
        options=all_crops,
        index=all_crops.index(def_crop),
        key="crop_intelligence_dropdown"
    )
    st.session_state["selected_crop"] = chosen_crop

    # Fetch crop profile from authentic agronomic database
    cp = agronomy_data.get_crop_profile(chosen_crop)

    # Crop Summary Header
    st.markdown(
        f"""
        <div style="background-color: #E8F5E9; border-radius: 8px; padding: 14px 20px; margin-bottom: 16px;">
            <h3 style="color: #1B5E20; margin: 0;">{chosen_crop}</h3>
            <span class="badge">📂 {cp['category']}</span>
            <span class="badge">⚖️ Reporting Unit: {cp['reporting_unit']}</span>
            <span class="badge">☀️ Typical Season: {cp['season']}</span>
            <span class="badge">⏱️ Duration: {cp['duration_days'][0]}–{cp['duration_days'][1]} Days</span>
            <div style="color: #4A634A; font-size: 0.85rem; margin-top: 6px;">
                Verified Source: <em>{cp['source']}</em>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Agronomic Cards
    ac1, ac2, ac3, ac4 = st.columns(4)
    with ac1:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title">Optimal Water Need</div>
                <div class="metric-value">{cp['water_req_mm'][0]}–{cp['water_req_mm'][1]} mm</div>
                <div class="metric-subtitle">Total seasonal requirement</div>
            </div>""", unsafe_allow_html=True
        )
    with ac2:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title">Temperature Range</div>
                <div class="metric-value">{cp['temp_range_c'][0]}–{cp['temp_range_c'][1]} °C</div>
                <div class="metric-subtitle">Optimal vegetative growth</div>
            </div>""", unsafe_allow_html=True
        )
    with ac3:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title">Maturity Duration</div>
                <div class="metric-value">{cp['duration_days'][0]}–{cp['duration_days'][1]} days</div>
                <div class="metric-subtitle">Sowing to physiological harvest</div>
            </div>""", unsafe_allow_html=True
        )
    with ac4:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-title">Suitable Soil Types</div>
                <div class="metric-subtitle" style="font-size:0.9rem; font-weight:600; color:#1B3B1B; margin-top:6px;">
                    {', '.join(cp['soils'][:3])}
                </div>
            </div>""", unsafe_allow_html=True
        )

    st.markdown("---")

    # Crop Lifecycle Visualizer
    st.markdown("### 🔄 Interactive Crop Lifecycle Progression")
    st.caption("Visual stage-by-stage progression from germination to harvest with field management guidelines.")

    stages = cp["stages"]
    stage_names = [f"Stage {i+1}: {s['stage']}" for i, s in enumerate(stages)]

    selected_stage_idx = st.select_slider(
        "Navigate Growth Stages:",
        options=range(len(stages)),
        format_func=lambda i: stage_names[i]
    )

    curr_stage = stages[selected_stage_idx]
    st.markdown(
        f"""
        <div class="lifecycle-container">
            <h4 style="color: #2E7D32; margin-top: 0;">🌱 {stage_names[selected_stage_idx]}</h4>
            <div style="margin-bottom: 10px;">
                <span class="badge badge-stage">⏱️ ~{curr_stage['pct']}% of Lifecycle</span>
                <span class="badge">Crop: {chosen_crop}</span>
            </div>
            <p style="color: #263238; font-size: 1.05rem; line-height: 1.5;">
                {curr_stage['desc']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Progress bar showing cumulative position
    cum_pct = sum(stages[k]["pct"] for k in range(selected_stage_idx + 1))
    st.progress(min(1.0, cum_pct / 100.0), text=f"Cumulative Growth Progress: ~{cum_pct}%")

    st.markdown("---")

    # Water Requirement vs Actual Rainfall Analysis
    st.markdown(f"### 💧 Water Requirement vs. Recorded Rainfall for {chosen_crop}")
    crop_hist = full_df[full_df["Crop"] == chosen_crop].copy()

    if crop_hist.empty:
        st.info(f"No historical records available in the dataset for {chosen_crop}.")
        return

    top_states_for_crop = (
        crop_hist.groupby("State")["Production"]
        .sum()
        .reset_index()
        .sort_values("Production", ascending=False)
        .head(6)["State"].tolist()
    )

    rain_by_state = (
        crop_hist[crop_hist["State"].isin(top_states_for_crop)]
        .groupby("State")["Annual_Rainfall"]
        .mean()
        .reset_index()
    )

    fig_water = go.Figure()
    fig_water.add_trace(go.Bar(
        x=rain_by_state["State"],
        y=rain_by_state["Annual_Rainfall"],
        name="Recorded Annual Rainfall (mm)",
        marker_color="#42A5F5"
    ))
    fig_water.add_hline(
        y=cp["water_req_mm"][0],
        line_dash="dash",
        line_color="#2E7D32",
        annotation_text=f"Min Crop Need ({cp['water_req_mm'][0]} mm)",
        annotation_position="top left"
    )
    fig_water.add_hline(
        y=cp["water_req_mm"][1],
        line_dash="dot",
        line_color="#1B5E20",
        annotation_text=f"Max Crop Need ({cp['water_req_mm'][1]} mm)",
        annotation_position="bottom left"
    )
    fig_water.update_layout(
        title=f"Average Rainfall in Top Producer States vs. {chosen_crop} Water Needs",
        yaxis_title="Precipitation / Water (mm)",
        xaxis_title="Top Cultivating States",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=20, r=20, t=50, b=40)
    )
    st.plotly_chart(fig_water, use_container_width=True)

    st.markdown(
        """
        <div class="notice-box">
            📌 <strong>Agronomic Insight (Irrigation vs. Rainfed):</strong> Where annual rainfall is lower 
            than optimal crop water requirements (e.g., Wheat in Punjab/Haryana), high yields are achieved 
            through intensive canal networks and tubewell irrigation. Conversely, in regions with rainfall 
            exceeding maximum crop requirements, drainage and flood resilience become paramount.
        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================================================================
# 8. FEATURE 4 & 6: NATIONAL PRODUCTION ANALYTICS (PRESERVED & ENHANCED)
# ==============================================================================
def render_national_analytics(filtered_df: pd.DataFrame):
    """Renders comprehensive national production charts, trends, insights, and YoY growth."""
    st.subheader("📊 National Production Analytics & Trends")

    # Data Quality Callout on Coconut and 2020
    st.markdown(
        """
        <div class="notice-box">
            🔍 <strong>Data Quality & Units Notice:</strong>
            <ul>
                <li><strong>Coconut Reporting:</strong> In Indian agricultural compilations, Coconut is officially 
                counted in <em>individual nuts / thousands of nuts</em>, while food grains (Wheat, Rice) are recorded 
                in <em>metric tonnes</em>. To avoid cross-commodity unit distortion, use the sidebar 
                <strong>Crop Classification</strong> filter.</li>
                <li><strong>2020 Historical Record:</strong> In this dataset, the year 2020 contains records exclusively 
                from a single state (Uttarakhand, 37 records). This sharp decline represents an incomplete reporting cutoff 
                in the historical compilation, not an agricultural collapse.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    if filtered_df.empty:
        st.warning("No records match the current filters.")
        return

    # Row 1: Crop Comparison & Yearly Trend
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### 🌾 Production by Crop")
        crop_summary = (
            filtered_df.groupby("Crop")["Production"]
            .sum()
            .reset_index()
            .sort_values(by="Production", ascending=False)
        )
        display_limit = 20
        chart_data = crop_summary.head(display_limit)
        fig_crop = px.bar(
            chart_data,
            x="Crop",
            y="Production",
            color="Production",
            color_continuous_scale="Greens",
            text_auto=".2s",
            title=f"Top {min(len(crop_summary), display_limit)} Crops by Production"
        )
        fig_crop.update_layout(
            xaxis_tickangle=-45,
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            margin=dict(l=20, r=20, t=40, b=60),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_crop, use_container_width=True)

    with c2:
        st.markdown("#### 📈 Yearly Production Trend")
        yearly = (
            filtered_df.groupby("Crop_Year")["Production"]
            .sum()
            .reset_index()
            .sort_values("Crop_Year")
        )
        fig_year = go.Figure()
        fig_year.add_trace(go.Scatter(
            x=yearly["Crop_Year"],
            y=yearly["Production"],
            mode="lines+markers",
            name="Total Production",
            line=dict(color="#2E7D32", width=3),
            marker=dict(size=7, color="#1B5E20"),
            hovertemplate="<b>Year %{x}</b><br>Total Production: %{y:,.0f}<extra></extra>"
        ))
        fig_year.update_layout(
            title="Chronological Production Trend Over Time",
            xaxis=dict(title="Harvest Year", dtick=2),
            yaxis=dict(title="Total Production"),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            margin=dict(l=20, r=20, t=40, b=40)
        )
        st.plotly_chart(fig_year, use_container_width=True)

    st.markdown("---")

    # Row 2: Top States & YoY Growth
    s1, s2 = st.columns(2)

    with s1:
        st.markdown("#### 🏆 Top Producer States")
        state_summary = (
            filtered_df.groupby("State")["Production"]
            .sum()
            .reset_index()
            .sort_values(by="Production", ascending=False)
        )
        top_states = state_summary.head(10).sort_values("Production", ascending=True)
        fig_st = px.bar(
            top_states,
            x="Production",
            y="State",
            orientation="h",
            color="Production",
            color_continuous_scale="Tealgrn",
            text_auto=".2s",
            title="Top 10 States by Total Production"
        )
        fig_st.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            margin=dict(l=20, r=20, t=40, b=40),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_st, use_container_width=True)

    with s2:
        st.markdown("#### 📊 Year-over-Year (YoY) Growth Rate (%)")
        if len(yearly) >= 2:
            yearly["Prev_Prod"] = yearly["Production"].shift(1)
            yearly["YoY_Growth"] = ((yearly["Production"] - yearly["Prev_Prod"]) / yearly["Prev_Prod"]) * 100
            yoy_chart = yearly.dropna(subset=["YoY_Growth"]).copy()
            yoy_chart["Direction"] = np.where(yoy_chart["YoY_Growth"] >= 0, "Positive", "Negative")

            fig_yoy = px.bar(
                yoy_chart,
                x="Crop_Year",
                y="YoY_Growth",
                color="Direction",
                color_discrete_map={"Positive": "#2E7D32", "Negative": "#D32F2F"},
                text_auto=".1f",
                title="Annual Production Percentage Change"
            )
            fig_yoy.update_layout(
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                margin=dict(l=20, r=20, t=40, b=40),
                xaxis=dict(dtick=2),
                yaxis=dict(title="Growth (%)")
            )
            st.plotly_chart(fig_yoy, use_container_width=True)
        else:
            st.info("YoY growth requires at least two distinct years.")

    st.markdown("---")

    # Row 3: Automated Insights & Rainfall vs Yield Correlation
    i1, i2 = st.columns([0.45, 0.55])

    with i1:
        st.markdown("#### 💡 Automated Agricultural Insights")
        tot_prod = filtered_df["Production"].sum()
        crop_totals = filtered_df.groupby("Crop")["Production"].sum()
        state_totals = filtered_df.groupby("State")["Production"].sum()

        if not crop_totals.empty and tot_prod > 0:
            top_c = crop_totals.idxmax()
            top_c_prod = crop_totals.max()
            top_c_pct = (top_c_prod / tot_prod) * 100
            st.markdown(f'<div class="insight-box">🥇 <strong>Dominant Crop:</strong> {top_c} constitutes <strong>{top_c_prod:,.0f}</strong> ({top_c_pct:.1f}%) of filtered output.</div>', unsafe_allow_html=True)

        if not state_totals.empty and tot_prod > 0:
            top_s = state_totals.idxmax()
            top_s_prod = state_totals.max()
            st.markdown(f'<div class="insight-box">🏛️ <strong>Leading State:</strong> {top_s} leads cumulative production with <strong>{top_s_prod:,.0f}</strong> units.</div>', unsafe_allow_html=True)

        if len(yearly) >= 2:
            st_yr, end_yr = yearly.iloc[0]["Crop_Year"], yearly.iloc[-1]["Crop_Year"]
            st_v, end_v = yearly.iloc[0]["Production"], yearly.iloc[-1]["Production"]
            if st_v > 0:
                pct = ((end_v - st_v) / st_v) * 100
                st.markdown(f'<div class="insight-box">📅 <strong>Trajectory:</strong> Output changed by <strong>{pct:+.1f}%</strong> from {st_yr} to {end_yr}.</div>', unsafe_allow_html=True)

    with i2:
        st.markdown("#### 🌧️ Annual Rainfall vs. Crop Yield")
        corr_df = filtered_df.dropna(subset=["Annual_Rainfall", "Yield"]).copy()
        if len(corr_df) >= 2:
            std_r = corr_df["Annual_Rainfall"].std()
            std_y = corr_df["Yield"].std()
            if std_r == 0 or std_y == 0 or np.isnan(std_r) or np.isnan(std_y):
                corr_val = None
                corr_str = "Undefined (constant values)"
            else:
                corr_val = corr_df["Annual_Rainfall"].corr(corr_df["Yield"])
                corr_str = f"r = {corr_val:.3f}" if not np.isnan(corr_val) else "Low variance"

            st.caption(f"Pearson Correlation: **{corr_str}** | Sample size: **{len(corr_df):,}** observations")

            plot_pts = corr_df.sample(n=min(len(corr_df), 2500), random_state=42)
            fig_scatter = px.scatter(
                plot_pts,
                x="Annual_Rainfall",
                y="Yield",
                color="Crop",
                opacity=0.7,
                title="Rainfall (mm) vs. Crop Yield",
                labels={"Annual_Rainfall": "Annual Rainfall (mm)", "Yield": "Yield Index"}
            )
            fig_scatter.update_layout(
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                margin=dict(l=20, r=20, t=40, b=40)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)


# ==============================================================================
# 9. DATA TABLE & CSV EXPORT (PRESERVED)
# ==============================================================================
def render_data_table_tab(filtered_df: pd.DataFrame):
    """Renders tabular data viewer and one-click CSV export."""
    st.subheader("📋 Filtered Historical Dataset & Export")
    st.write(f"Displaying **{len(filtered_df):,}** records matching current filters:")

    st.dataframe(
        filtered_df[EXPECTED_COLUMNS],
        use_container_width=True,
        hide_index=True
    )

    csv_data = filtered_df[EXPECTED_COLUMNS].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_crop_intelligence.csv",
        mime="text/csv",
        help="Export all currently filtered agricultural records."
    )


# ==============================================================================
# 10. MAIN APPLICATION CONTROLLER
# ==============================================================================
def main():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(curr_dir, "crop_yield.csv")
    geojson_path = os.path.join(curr_dir, "data", "india_states.geojson")

    # Ingest Data and Authentic Boundaries
    full_df = load_historical_data(dataset_path)
    india_geojson = load_india_geojson(geojson_path)

    # Header
    st.markdown('<h1 class="main-title">🌾 Indian Agriculture Intelligence Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-title">Spatial mapping, state agronomic profiles, crop intelligence, and multi-decade production analysis (1997–2020).</p>',
        unsafe_allow_html=True
    )

    # Sidebar Filter Controls
    filtered_df, meta = render_sidebar_filters(full_df)

    # KPI Banner
    render_kpi_banner(filtered_df, meta)

    st.markdown("---")

    # Main Navigation Tabs
    tab_map, tab_state, tab_crop, tab_analytics, tab_table = st.tabs([
        "🗺️ India Map & Spatial Intelligence",
        "📍 State Explorer",
        "🌱 Crop Intelligence & Lifecycle",
        "📊 National Production Analytics",
        "📋 Data Table & Export"
    ])

    with tab_map:
        render_interactive_map(filtered_df, india_geojson, full_df)

    with tab_state:
        render_state_explorer(full_df, filtered_df)

    with tab_crop:
        render_crop_intelligence(full_df)

    with tab_analytics:
        render_national_analytics(filtered_df)

    with tab_table:
        render_data_table_tab(filtered_df)


if __name__ == "__main__":
    main()
