import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px

def run():

    st.title("🔮 Wildlife Collision Risk Prediction")

    st.write("Click on a location (cluster) on the map below, and select time to predict collision risk.")

    # === Ladda modellen
    with open("model/model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("model/model_columns.pkl", "rb") as f:
        model_columns = pickle.load(f)

    # === Ladda data med clusterdetaljer
    @st.cache_data
    def load_data():
        df = pd.read_csv("data/cleaned_with_clusters.csv")
        df = df.dropna(subset=["Lat_WGS84", "Lon_WGS84", "Cluster_ID"])
        df["Cluster_ID"] = df["Cluster_ID"].astype(int)
        return df

    df_all = load_data()

    # === Beräkna centroider
    centroids = df_all.groupby("Cluster_ID")[["Lat_WGS84", "Lon_WGS84"]].mean().reset_index()

    # === Karta där man väljer cluster
    st.subheader("🗺️ Select a Cluster")
    selected_cluster = st.selectbox("Or click on a location below:", centroids["Cluster_ID"].sort_values().tolist())

    fig = px.scatter_mapbox(
        centroids,
        lat="Lat_WGS84",
        lon="Lon_WGS84",
        hover_name="Cluster_ID",
        color=centroids["Cluster_ID"] == selected_cluster,
        zoom=4.5,
        height=500,
        color_discrete_map={True: "red", False: "gray"}
    )
    fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

    # === Formulär: tid
    st.subheader("⏰ Select Time")
    hour = st.slider("Hour of Day (0–23):", 0, 23, 8)
    month = st.slider("Month (1–12):", 1, 12, 10)
    weekday = st.selectbox("Weekday:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    # === Förbered input till modell
    input_dict = {
        "Cluster_ID": selected_cluster,
        "Hour": hour,
        "Month": month,
        **{f"Weekday_{day}": int(day == weekday) for day in ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
    }
    input_df = pd.DataFrame([input_dict])

    # Säkerställ alla kolumner finns
    for col in model_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model_columns]

    # === Prediktion
    prediction = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0][1]

    if prediction == 1:
        st.error(f"⚠️ High Risk! (probability: {proba:.2%})")
    else:
        st.success(f"✅ Low Risk (probability: {proba:.2%})")

    # === Visa alla krockar i detta kluster
    st.subheader("🗺️ Collisions in Selected Cluster")
    df_cluster = df_all[df_all["Cluster_ID"] == selected_cluster]

    fig2 = px.scatter_mapbox(
        df_cluster,
        lat="Lat_WGS84",
        lon="Lon_WGS84",
        hover_data=["Species", "Time"] if "Species" in df_cluster.columns else True,
        zoom=6,
        opacity=0.4,
        height=500
    )
    fig2.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":20,"l":0,"b":0})
    st.plotly_chart(fig2)
