import streamlit as st
import pandas as pd
import pickle
import numpy as np

def run():
    st.title("🔮 Wildlife Collision Risk Prediction")

    st.write("Enter time and location details to predict if it's a high-risk situation.")

    # === Ladda modellen och kolumner ===
    with open("model/model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("model/model_columns.pkl", "rb") as f:
        model_columns = pickle.load(f)

    # === Användarinmatning ===
    cluster_id = st.number_input("Cluster ID (0–99):", min_value=0, max_value=99, value=0)
    hour = st.slider("Hour of Day (0–23):", 0, 23, 8)
    month = st.slider("Month (1–12):", 1, 12, 10)
    weekday = st.selectbox("Weekday:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    # === Skapa input-DataFrame ===
    input_dict = {
        "Cluster_ID": cluster_id,
        "Hour": hour,
        "Month": month,
        # Weekday kolumner one-hot
        **{f"Weekday_{day}": int(day == weekday) for day in ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}  # Monday excluded
    }

    input_df = pd.DataFrame([input_dict])

    # Lägg till saknade kolumner om någon fattas
    for col in model_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model_columns]

    # === Prediktion ===
    prediction = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0][1]

    if prediction == 1:
        st.error(f"⚠️ High Risk! (probability: {proba:.2%})")
    else:
        st.success(f"✅ Low Risk (probability: {proba:.2%})")

    import plotly.express as px

    # === Ladda cleaned data med alla punkter ===
    @st.cache_data
    def load_cluster_data():
        df = pd.read_csv("data/cleaned_with_clusters.csv")
        df = df.dropna(subset=["Lat_WGS84", "Lon_WGS84", "Cluster_ID"])
        df["Cluster_ID"] = df["Cluster_ID"].astype(int)
        return df

    df_clusters = load_cluster_data()

    # === Filtrera till valt cluster
    selected_df = df_clusters[df_clusters["Cluster_ID"] == cluster_id]

    # === Skapa karta med alla krockar i klustret
    fig = px.scatter_mapbox(
        selected_df,
        lat="Lat_WGS84",
        lon="Lon_WGS84",
        hover_data=["Species", "Time"] if "Species" in selected_df.columns else True,
        zoom=6,
        height=500,
        opacity=0.4
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":20,"l":0,"b":0})

    st.markdown("### 🗺️ Collisions in Selected Cluster")
    st.plotly_chart(fig)
