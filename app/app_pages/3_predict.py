# app_pages/3_predict.py
import streamlit as st
import pandas as pd
from datetime import datetime
from src.predictor import (
    load_unique_values,
    get_municipalities_for_county,
    build_feature_row,
    predict_proba_label,
)

def run():
    st.title("🔮 Wildlife Collision Risk Prediction")
    st.write("Välj län och kommun (kaskad), tid och art – modellen ger risknivå.")

    uv = load_unique_values()
    counties = uv["counties"]
    species_list = uv["species"]
    weekday_opts = uv["weekdays"]

    colL, colR = st.columns(2)
    with colL:
        # 1) County
        default_county = "Värmlands län" if "Värmlands län" in counties else counties[0]
        county = st.selectbox("County", counties, index=counties.index(default_county))

        # 2) Municipality, filtrerad på valt county
        munis = get_municipalities_for_county(county)
        municipality = st.selectbox("Municipality", munis, index=0 if munis else None)

        species = st.selectbox(
            "Species",
            ["All species"] + [s for s in species_list if s != "All species"],
        )
    with colR:
        now = datetime.now()
        month = st.slider("Month", 1, 12, now.month)
        hour = st.slider("Hour of day", 0, 23, now.hour)
        default_wd = now.strftime("%A")
        wd_index = weekday_opts.index(default_wd) if default_wd in weekday_opts else 0
        weekday = st.selectbox("Weekday", weekday_opts, index=wd_index)

    with st.expander("Optional: coordinates (for future map-click wiring)"):
        lat = st.number_input("Lat_WGS84", value=0.0, format="%.6f")
        lon = st.number_input("Long_WGS84", value=0.0, format="%.6f")
        doy = st.number_input("Day_of_Year", min_value=1, max_value=366, value=now.timetuple().tm_yday)

    if st.button("Predict risk"):
        with st.spinner("Predicting..."):
            X = build_feature_row(
                year=now.year,
                month=month,
                hour=hour,
                weekday=weekday,
                county=county,
                species=species,
                municipality=municipality,           # <--- skicka in
                lat_wgs84=(lat if lat != 0.0 else None),
                long_wgs84=(lon if lon != 0.0 else None),
                day_of_year=doy,
            )
            score, label, proba = predict_proba_label(X)

        st.subheader("Result")
        if isinstance(score, float):
            st.metric("Risk level", label, delta=f"score: {score:.2f}")
        else:
            st.metric("Predicted class", label)

        advice = {
            "High":   "High risk – sänk hastigheten, öka avståndet och scanna vägrenar aktivt.",
            "Medium": "Måttlig risk – var extra uppmärksam vid gryning/skymning och i skogspassager.",
            "Low":    "Låg risk – följ skyltning, håll normal uppmärksamhet.",
        }
        st.info(advice.get(label, "Var uppmärksam och följ lokala skyltar."))

        with st.expander("Explain / probabilities"):
            st.write("Feature vector shape:", X.shape)
            nonzero = X.iloc[0][X.iloc[0] != 0].sort_values(ascending=False).head(12)
            st.write(nonzero.to_frame("value"))
            if proba is not None:
                st.write("Raw predict_proba:", proba)

# Valfritt: gör sidan körbar direkt vid behov
if __name__ == "__main__":
    run()