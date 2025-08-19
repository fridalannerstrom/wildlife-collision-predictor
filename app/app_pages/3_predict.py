# app_pages/3_predict.py

import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

from src.predictor import (
    load_unique_values,
    get_municipalities_for_county,
    build_feature_row,
    predict_proba_label,
    load_model,
    load_model_columns,
)

from src.data_loader import load_clean_data


def adjust_score(score: float) -> float:
    return score ** 2.5


def run():
    st.title("Wildlife Collision Risk Prediction")
    st.markdown(
        "**Select a location and time to get predicted collision risk level "
        "and visual feedback.**"
    )

    uv = load_unique_values()
    counties = uv["counties"]
    species_list = uv["species"]

    st.subheader("Step 1: Select Location")
    county = st.selectbox("County", counties, help="Choose the county where you plan to travel.")
    munis = get_municipalities_for_county(county)
    municipality = st.selectbox("Municipality", munis, help="Select a specific municipality in the county.")

    st.subheader("Step 2: Select Time & Species")
    col1, col2 = st.columns(2)
    with col1:
        month = st.selectbox("Month", list(range(1, 13)), index=datetime.now().month - 1)
    with col2:
        hour = st.slider("Hour of Day", 0, 23, datetime.now().hour)

    species = st.selectbox("Species", ["All species"] + [s for s in species_list if s != "All species"])

    show_map = st.checkbox("Show map", value=False)

    if st.button("Predict Risk"):
        with st.spinner("Predicting..."):
            try:
                df = load_clean_data()
                now = datetime.now()
                year = now.year
                day_of_year = now.timetuple().tm_yday
                weekday = now.strftime('%A')

                X = build_feature_row(
                    year=year,
                    month=month,
                    hour=hour,
                    county=county,
                    species=species,
                    municipality=municipality,
                    day_of_year=day_of_year,
                    weekday=weekday,
                )

                model = load_model()
                model_columns = load_model_columns()
                score, label, proba, X_encoded = predict_proba_label(X, model)

                adjusted_score = adjust_score(score)

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

                st.subheader("Result")
                st.metric("Risk Level", label, delta=f"adjusted: {adjusted_score:.2f}")
                st.caption(f"⚙️ Raw model score: {score:.2f}")

                advice = {
                    "Very High": "🚨 Very high risk predicted for this time and location. Avoid travel if possible or proceed with extreme caution.",
                    "High": "⚠️ High risk of wildlife collision at the selected time and place. Reduce speed and stay extremely alert.",
                    "Moderate": "🔶 Moderate risk detected. Be attentive and watch for wildlife near the road, especially around forest areas.",
                    "Low": "🟢 Low risk based on your selected input. Stay alert and follow local signage.",
                    "Very Low": "🟦 Very low collision risk predicted for this time and location. Drive with normal caution.",
                }
                st.info(advice.get(label, "Stay alert and follow local signage."))

                if show_map:
                    st.subheader("Prediction Location on Map")
                    loc_df = df[(df["County"] == county) & (df["Municipality"] == municipality)].dropna(
                        subset=["Lat_WGS84", "Long_WGS84"]
                    )

                    if not loc_df.empty:
                        map_lat = loc_df["Lat_WGS84"].mean()
                        map_lon = loc_df["Long_WGS84"].mean()
                    else:
                        map_lat, map_lon = 62.0, 15.0

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
                        text=f"{label} risk<br>Species: {species}<br>Time: {hour}:00<br>Score: {adjusted_score:.2f}",
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

                with st.expander("View top influential features"):
                    nonzero = X_encoded.select_dtypes(include="number").iloc[0]
                    nonzero = nonzero[nonzero != 0].sort_values(ascending=False).head(10)
                    st.write(nonzero.to_frame("value"))

                    if proba is not None:
                        st.markdown("**Prediction probabilities:**")
                        st.write(proba)

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    run()
