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
from src.data_loader import load_clean_data


def run():
    """
    Streamlit page: Wildlife Collision Risk Prediction

    Allows users to input a location, time, and optionally a species to get a predicted
    risk level of wildlife collision, along with safety advice and map visualization.
    """
    st.title("Wildlife Collision Risk Prediction")
    st.markdown("**Select a location and time to get predicted collision risk level and visual feedback.**")

    # -----------------------------------------
    # Load data and unique values for form
    # -----------------------------------------
    df = load_clean_data()
    uv = load_unique_values()
    counties = uv["counties"]
    species_list = uv["species"]

    # -----------------------------------------
    # Step 1: Select location (County & Municipality)
    # -----------------------------------------
    st.subheader("Step 1: Select Location")
    county = st.selectbox("County", counties, help="Choose the county where you plan to travel.")
    munis = get_municipalities_for_county(county)
    municipality = st.selectbox("Municipality", munis, help="Select a specific municipality in the county.")

    # -----------------------------------------
    # Step 2: Select time and (optional) species
    # -----------------------------------------
    st.subheader("Step 2: Select Time & Species")
    col1, col2 = st.columns(2)
    with col1:
        month = st.selectbox(
            "Month",
            list(range(1, 13)),
            index=datetime.now().month - 1,
            help="Choose the month of travel."
        )
    with col2:
        hour = st.slider(
            "Hour of Day",
            0, 23,
            datetime.now().hour,
            help="Choose the approximate hour."
        )

    species = st.selectbox(
        "Species",
        ["All species"] + [s for s in species_list if s != "All species"],
        help="Optionally filter by specific species."
    )

    # -----------------------------------------
    # Step 3: Predict collision risk
    # -----------------------------------------
    if st.button("Predict Risk"):
        with st.spinner("Predicting..."):
            # Build model input features
            X = build_feature_row(
                year=datetime.now().year,
                month=month,
                hour=hour,
                county=county,
                species=species,
                municipality=municipality,
                day_of_year=datetime.now().timetuple().tm_yday,
            )

            # Run prediction
            score, label, proba = predict_proba_label(X)

        # Risk level thresholds (more conservative)
        if score >= 0.92:
            label = "Very High"
        elif score >= 0.75:
            label = "High"
        elif score >= 0.55:
            label = "Moderate"
        elif score >= 0.35:
            label = "Low"
        else:
            label = "Very Low"

        # -----------------------------------------
        # Display result + safety advice
        # -----------------------------------------
        st.subheader("Result")
        st.metric("Risk Level", label, delta=f"score: {score:.2f}")

        advice = {
            "Very High": "🚨 Very high risk – extreme caution required!",
            "High":      "⚠️ High risk – slow down, increase distance and stay alert near roadsides.",
            "Moderate":  "🔶 Moderate risk – be extra careful at dusk/dawn and near forest crossings.",
            "Low":       "🟢 Low risk – follow signage and drive with normal attention.",
            "Very Low":  "🟦 Very low risk – low probability of collision in this area/time.",
        }
        st.info(advice.get(label, "Stay alert and follow local signage."))

        # -----------------------------------------
        # Show map centered on selected location
        # -----------------------------------------
        st.subheader("Prediction Location on Map")

        loc_df = df[(df["County"] == county) & (df["Municipality"] == municipality)].dropna(
            subset=["Lat_WGS84", "Long_WGS84"]
        )

        if not loc_df.empty:
            map_lat = loc_df["Lat_WGS84"].mean()
            map_lon = loc_df["Long_WGS84"].mean()
        else:
            map_lat, map_lon = 62.0, 15.0  # fallback center

        fig = go.Figure(go.Scattermapbox(
            lat=[map_lat],
            lon=[map_lon],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=18,
                color=(
                    'darkred' if label == "Very High" else
                    'red' if label == "High" else
                    'orange' if label == "Moderate" else
                    'green' if label == "Low" else
                    'blue'
                )
            ),
            text=f"{label} risk<br>Species: {species}<br>Time: {hour}:00<br>Score: {score:.2f}",
            hoverinfo='text'
        ))

        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_zoom=7,
            mapbox_center={"lat": map_lat, "lon": map_lon},
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            height=500,
        )

        st.plotly_chart(fig, use_container_width=True)

        # -----------------------------------------
        # Show feature vector values and probabilities
        # -----------------------------------------
        with st.expander("View top influential features"):
            st.write("These are the features that had the highest values in your prediction vector:")
            nonzero = X.select_dtypes(include="number").iloc[0]
            nonzero = nonzero[nonzero != 0].sort_values(ascending=False).head(10)
            st.write(nonzero.to_frame("value"))

            if proba is not None:
                st.markdown("**Prediction probabilities:**")
                st.write(proba)


# Allow direct run
if __name__ == "__main__":
    run()
