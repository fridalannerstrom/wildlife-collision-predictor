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


def adjust_score(score: float) -> float:
    """
    Apply a non-linear adjustment to model score to reduce overconfidence
    and spread out predicted risk levels more realistically.
    """
    return score ** 2.5  # tweak this if needed


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
        month = st.selectbox("Month", list(range(1, 13)), index=datetime.now().month - 1)
    with col2:
        hour = st.slider("Hour of Day", 0, 23, datetime.now().hour)

    species = st.selectbox(
        "Species",
        ["All species"] + [s for s in species_list if s != "All species"]
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
            score, _, proba = predict_proba_label(X)
            adjusted_score = adjust_score(score)

        # Use adjusted score for final label
        if adjusted_score >= 0.92:
            label = "Very High"
        elif adjusted_score >= 0.75:
            label = "High"
        elif adjusted_score >= 0.55:
            label = "Moderate"
        elif adjusted_score >= 0.35:
            label = "Low"
        else:
            label = "Very Low"

        # -----------------------------------------
        # Display result + safety advice
        # -----------------------------------------
        st.subheader("Result")
        st.metric("Risk Level", label, delta=f"adjusted: {adjusted_score:.2f}")
        st.caption(f"⚙️ Raw model score: {score:.2f}")

        advice = {
            "Very High": "🚨 Very high risk – avoid t
