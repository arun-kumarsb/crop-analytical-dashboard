"""
Export Structured Datasets for High-Performance React Frontend
==============================================================
Extracts, aggregates, and transforms crop_yield.csv, agronomy_data.py,
and india_states.geojson into optimized JSON data files for the React application.
"""

import os
import json
import numpy as np
import pandas as pd
import agronomy_data

def aggregate_dataset(df_sub):
    total_production = float(df_sub["Production"].sum())
    total_area = float(df_sub["Area"].sum())
    avg_yield = float(df_sub["Yield"].mean())
    avg_rainfall = float(df_sub["Annual_Rainfall"].mean())
    states_count = int(df_sub["State"].nunique())
    crops_count = int(df_sub["Crop"].nunique())

    # Yearly Trend Data
    yearly = df_sub.groupby("Crop_Year").agg(
        production=("Production", "sum"),
        area=("Area", "sum"),
        yield_avg=("Yield", "mean"),
        rainfall=("Annual_Rainfall", "mean"),
        count=("Crop", "count")
    ).reset_index().sort_values("Crop_Year")
    yearly["prev_prod"] = yearly["production"].shift(1)
    yearly["yoy_growth"] = ((yearly["production"] - yearly["prev_prod"]) / yearly["prev_prod"]) * 100
    yearly_list = yearly.replace({np.nan: None}).to_dict(orient="records")

    # Commodity Category Distribution
    cat_summary = df_sub.groupby("Category").agg(
        production=("Production", "sum"),
        area=("Area", "sum"),
        crop_count=("Crop", "nunique")
    ).reset_index().sort_values("production", ascending=False)
    cat_summary["share_pct"] = (cat_summary["production"] / (total_production if total_production > 0 else 1)) * 100
    category_list = cat_summary.to_dict(orient="records")

    # Top Crops Summary & Targets
    crop_summary = df_sub.groupby("Crop").agg(
        production=("Production", "sum"),
        area=("Area", "sum"),
        yield_avg=("Yield", "mean"),
        rainfall_avg=("Annual_Rainfall", "mean"),
        states_count=("State", "nunique"),
        category=("Category", "first")
    ).reset_index().sort_values("production", ascending=False)
    crop_summary["share_pct"] = (crop_summary["production"] / (total_production if total_production > 0 else 1)) * 100
    top_crops_list = crop_summary.head(20).to_dict(orient="records")

    # Top States Summary
    state_summary = df_sub.groupby("State").agg(
        production=("Production", "sum"),
        area=("Area", "sum"),
        yield_avg=("Yield", "mean"),
        rainfall_avg=("Annual_Rainfall", "mean"),
        crops_count=("Crop", "nunique"),
        state_geo=("State_Geo", "first")
    ).reset_index().sort_values("production", ascending=False)
    state_summary["share_pct"] = (state_summary["production"] / (total_production if total_production > 0 else 1)) * 100
    state_list = state_summary.to_dict(orient="records")

    # State-by-Year Production for Animated Map
    state_year_map = df_sub.groupby(["State_Geo", "Crop_Year"]).agg(
        production=("Production", "sum"),
        yield_avg=("Yield", "mean"),
        rainfall=("Annual_Rainfall", "mean")
    ).reset_index()
    state_year_dict = {}
    for _, row in state_year_map.iterrows():
        yr = str(int(row["Crop_Year"]))
        st_name = row["State_Geo"]
        if yr not in state_year_dict:
            state_year_dict[yr] = {}
        state_year_dict[yr][st_name] = {
            "production": float(row["production"]),
            "yield": float(row["yield_avg"]),
            "rainfall": float(row["rainfall"])
        }

    # Multi-Year Milestones (Comparing Recent 4 Years)
    milestones = yearly.tail(4)[["Crop_Year", "production", "yield_avg", "rainfall"]].to_dict(orient="records")

    return {
        "kpis": {
            "total_production": total_production,
            "total_area": total_area,
            "avg_yield": avg_yield,
            "avg_rainfall": avg_rainfall,
            "states_count": states_count,
            "crops_count": crops_count,
            "year_min": int(yearly["Crop_Year"].min()) if len(yearly) > 0 else 1997,
            "year_max": int(yearly["Crop_Year"].max()) if len(yearly) > 0 else 2020,
        },
        "yearly": yearly_list,
        "categories": category_list,
        "top_crops": top_crops_list,
        "states": state_list,
        "state_yearly": state_year_dict,
        "milestones": milestones,
    }

def build_frontend_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "crop_yield.csv")
    geo_path = os.path.join(base_dir, "data", "india_states.geojson")
    out_dir = os.path.join(base_dir, "frontend", "src", "data")
    os.makedirs(out_dir, exist_ok=True)

    print("Reading crop_yield.csv...")
    df = pd.read_csv(csv_path)
    for c in ["Crop", "Season", "State"]:
        df[c] = df[c].astype(str).str.strip()

    num_cols = ["Crop_Year", "Area", "Production", "Annual_Rainfall", "Fertilizer", "Pesticide", "Yield"]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna()
    df["Crop_Year"] = df["Crop_Year"].astype(int)
    df["Category"] = df["Crop"].apply(lambda c: agronomy_data.get_crop_profile(c)["category"])
    df["State_Geo"] = df["State"].map(agronomy_data.get_state_geojson_name)

    # 1. Full Dataset Aggregations (All Commodities including Coconut)
    all_data = aggregate_dataset(df)

    # 2. Food & Cash Crops Only Aggregations (Metric Tonnes Only - Coconut Excluded)
    df_no_coconut = df[df["Crop"] != "Coconut"]
    no_coconut_data = aggregate_dataset(df_no_coconut)

    # 3. Agronomic Profiles for all 55 crops
    all_crops = sorted(df["Crop"].unique().tolist())
    crop_profiles = {}
    for crop in all_crops:
        p = agronomy_data.get_crop_profile(crop)
        crop_profiles[crop] = {
            "category": p["category"],
            "unit": p["reporting_unit"],
            "soils": p["soils"],
            "water_req_mm": p["water_req_mm"],
            "temp_range_c": p["temp_range_c"],
            "season": p["season"],
            "duration_days": p["duration_days"],
            "stages": p["stages"],
            "source": p["source"]
        }

    # 4. State Agro Profiles for all 30 states
    all_states = sorted(df["State"].unique().tolist())
    state_profiles = {}
    for st_name in all_states:
        sp = agronomy_data.get_state_profile(st_name)
        # Top 5 crops for this state
        st_crops = df[df["State"] == st_name].groupby("Crop")["Production"].sum().sort_values(ascending=False).head(5)
        state_profiles[st_name] = {
            "zone": sp["zone"],
            "climate_desc": sp["climate_desc"],
            "primary_season": sp["primary_season"],
            "soils": sp["soils"],
            "source": sp["source"],
            "top_crops": [{"crop": c, "production": float(v)} for c, v in st_crops.items()]
        }

    # Combine into main payload
    payload = {
        **all_data,
        "no_coconut": no_coconut_data,
        "crop_profiles": crop_profiles,
        "state_profiles": state_profiles,
        "all_crops": all_crops,
        "all_states": all_states,
    }

    out_file = os.path.join(out_dir, "agri_data.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Exported agri_data.json ({os.path.getsize(out_file) / 1024:.1f} KB)")

    # Copy GeoJSON into frontend
    if os.path.exists(geo_path):
        with open(geo_path, "r", encoding="utf-8") as f:
            geo_data = json.load(f)
        with open(os.path.join(out_dir, "india_states.json"), "w", encoding="utf-8") as f:
            json.dump(geo_data, f)
        print("Copied india_states.json into frontend data directory.")

if __name__ == "__main__":
    build_frontend_data()
