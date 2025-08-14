import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from src.data_loader import load_clean_data


def run():
    """
    Streamlit page: Exploratory Data Analysis (EDA)

    This page explores the three main project hypotheses using visualizations:
    1. Moose collisions increase during autumn.
    2. Wildlife collisions are more common at dawn and dusk.
    3. Certain counties report more wildlife collisions.
    """

    st.title("Exploratory Data Analysis")
    st.markdown("This section explores the hypotheses using visual analysis.")

    # -----------------------------
    # Load cleaned dataset
    # -----------------------------
    df = load_clean_data()

    # -----------------------------
    # Hypothesis 1: Autumn risk
    # -----------------------------
    st.subheader("Hypothesis 1: Wildlife collisions increase during autumn")

    species_options = ["All species"] + sorted(
        df["Species"].dropna().unique()
    )

    selected_species = st.selectbox(
        "Select species to view monthly collisions:",
        species_options
    )

    if selected_species == "All species":
        df_selected = df
    else:
        df_selected = df[df["Species"] == selected_species]

    monthly_counts = (
        df_selected["Month"]
        .value_counts()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=monthly_counts.index, y=monthly_counts.values, ax=ax)
    ax.set_title(f"Number of {selected_species} Collisions per Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Collisions")
    st.pyplot(fig)

    st.markdown("""
    *Interpretation:*
    This visualization helps confirm whether certain species, such as moose,
    show increased collision rates in autumn. Similar patterns may or may not
    be visible for other species.
    """)

    # -----------------------------
    # Hypothesis 2: Time of day
    # -----------------------------
    st.subheader("Hypothesis 2: Collisions are more common at dawn and dusk")

    df["Hour"] = pd.to_datetime(df["Time"], errors="coerce").dt.hour

    species_for_time = st.selectbox(
        "Select species to view hourly collisions:",
        species_options
    )

    df_time = (
        df if species_for_time == "All species"
        else df[df["Species"] == species_for_time]
    )

    hourly_counts = (
        df_time["Hour"]
        .value_counts()
        .sort_index()
    )

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=hourly_counts.index, y=hourly_counts.values, ax=ax2)
    ax2.set_title(f"Number of {species_for_time} Collisions by Hour of Day")
    ax2.set_xlabel("Hour of Day")
    ax2.set_ylabel("Number of Collisions")
    st.pyplot(fig2)

    st.markdown(
        """
        *Interpretation:*
        This chart helps verify if collision frequency is higher during early
        morning and evening hours, as assumed for crepuscular species like deer
        or moose.
        """
    )

    # -----------------------------
    # Hypothesis 3: County distribution
    # -----------------------------
    st.subheader(
        "Hypothesis 3: Certain counties have more collisions"
    )

    selected_species_3 = st.selectbox(
        "Select species to view collision distribution by county:",
        species_options
    )

    df_county = (
        df if selected_species_3 == "All species"
        else df[df["Species"] == selected_species_3]
    )

    county_counts = (
        df_county["County"]
        .value_counts()
        .sort_values(ascending=False)
    )

    fig3, ax3 = plt.subplots(figsize=(10, 8))
    sns.barplot(y=county_counts.index, x=county_counts.values, ax=ax3)
    ax3.set_title(f"{selected_species_3} Collisions per County")
    ax3.set_xlabel("Number of Collisions")
    ax3.set_ylabel("County")
    st.pyplot(fig3)

    st.markdown(
        """
        *Interpretation:*
        This chart shows the regional distribution of wildlife collisions.
        Some counties consistently report more incidents, possibly due
        to road density, habitat, or traffic volume.
        """
    )

    # -----------------------------
    # Interactive map
    # -----------------------------
    st.subheader("Interactive Collision Map (Filtered)")

    years = sorted(df["Year"].dropna().unique())
    selected_year = st.selectbox("Select year:", years, index=len(years)-1)
    selected_species_map = st.selectbox("Select species:", species_options)

    # Filter dataset
    df_map = df[df["Year"] == selected_year]
    if selected_species_map != "All species":
        df_map = df_map[df_map["Species"] == selected_species_map]

    # Drop missing GPS
    df_map = df_map.dropna(subset=["Lat_WGS84", "Long_WGS84"])

    if len(df_map) > 10000:
        df_map = df_map.sample(10000, random_state=42)

    fig_map = px.scatter_mapbox(
        df_map,
        lat="Lat_WGS84",
        lon="Long_WGS84",
        color="Species",
        hover_data=[
            "Date",
            "County",
            "Municipality"
        ],
        zoom=4.5,
        height=600,
        title=(
            f"Wildlife Collisions in {selected_year} "
            f"({selected_species_map})"
        )
    )

    fig_map.update_layout(mapbox_style="open-street-map")
    fig_map.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    st.plotly_chart(fig_map)
