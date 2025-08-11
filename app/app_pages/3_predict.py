# app_pages/3_predict.py
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from src.predictor import (
    load_unique_values,
    get_municipalities_for_county,
    build_feature_row,
    predict_proba_label,
)

def run():
    st.title("🔮 Wildlife Collision Risk Prediction")
    st.markdown("**Select location and time – get collision risk level and map.**")

    uv = load_unique_values()
    counties = uv["counties"]
    species_list = uv["species"]
    weekday_opts = uv["weekdays"]

    # --- Step 1: Select Location ---
    st.subheader("1️⃣ Select Location")
    county = st.selectbox("County", counties)
    munis = get_municipalities_for_county(county)
    municipality = st.selectbox("Municipality", munis)

    # --- Step 2: Select Time & Species ---
    st.subheader("2️⃣ Select Time & Species")
    col1, col2, col3 = st.columns(3)
    with col1:
        month = st.selectbox("Month", list(range(1, 13)), index=datetime.now().month - 1)
    with col2:
        hour = st.slider("Hour of Day", 0, 23, datetime.now().hour)
    with col3:
        weekday = st.selectbox("Weekday", weekday_opts, index=datetime.now().weekday())

    species = st.selectbox("Species", ["All species"] + [s for s in species_list if s != "All species"])

    # --- Prediction ---
    if st.button("Predict Risk"):
        with st.spinner("Predicting..."):
            X = build_feature_row(
                year=datetime.now().year,
                month=month,
                hour=hour,
                weekday=weekday,
                county=county,
                species=species,
                municipality=municipality,
                day_of_year=datetime.now().timetuple().tm_yday,
            )
            score, label, _ = predict_proba_label(X)

        st.subheader("📊 Result")
        st.metric("Risk Level", label, delta=f"score: {score:.2f}")

        advice = {
            "High":   "⚠️ High risk – slow down, increase distance and stay alert near roadsides.",
            "Medium": "🔶 Moderate risk – be extra careful at dusk/dawn and near forest crossings.",
            "Low":    "🟢 Low risk – follow signage and drive with normal attention.",
        }
        st.info(advice.get(label, "Stay alert and follow local signage."))

        # --- Map ---
        st.subheader("🗺️ Prediction Location on Map")

        # fallback coordinates to center of Sweden for visual reference
        map_lat, map_lon = 62.0, 15.0

        fig = go.Figure(go.Scattermapbox(
            lat=[map_lat],
            lon=[map_lon],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=18,
                color='red' if label == "High" else ('orange' if label == "Medium" else 'green')
            ),
            text=f"{label} risk<br>Species: {species}<br>Time: {hour}:00<br>Score: {score:.2f}",
            hoverinfo='text'
        ))

        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_zoom=6,
            mapbox_center={"lat": map_lat, "lon": map_lon},
            margin={"r":0,"t":0,"l":0,"b":0},
            height=500,
        )

        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    run()
