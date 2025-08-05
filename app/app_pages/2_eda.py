import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("Exploratory Data Analysis")
    st.markdown("This section explores the hypotheses using visual analysis.")

    # Ladda data
    df = pd.read_csv("data/cleaned_data.csv")

    st.subheader("Hypothesis 1: Wildlife collisions increase during autumn")

    species_options = ["All species"] + sorted(df["Species"].dropna().unique().tolist())
    selected_species = st.selectbox("Select species to view monthly collisions:", species_options)

    if selected_species == "All species":
        df_selected = df.copy()
        title_species = "All Species"
    else:
        df_selected = df[df["Species"] == selected_species]
        title_species = selected_species

    monthly_counts = df_selected["Manad"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=monthly_counts.index, y=monthly_counts.values, ax=ax)
    ax.set_title(f"Number of {title_species} Collisions per Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Collisions")
    st.pyplot(fig)


    st.markdown("""
    *Interpretation:*  
    This visualization helps confirm whether certain species, such as moose, show increased collision rates in autumn. Similar patterns may or may not be visible for other species.
    """)

    st.subheader("Hypothesis 2: Collisions are more common at dawn and dusk")

    # Konvertera tid till timme
    df["Hour"] = pd.to_datetime(df["Tid"], errors="coerce").dt.hour

    species_options_2 = ["All species"] + sorted(df["Species"].dropna().unique().tolist())
    species_for_time = st.selectbox("Select species to view hourly collisions:", species_options_2)

    if species_for_time == "All species":
        df_species_time = df.copy()
        title_species = "All Species"
    else:
        df_species_time = df[df["Species"] == species_for_time]
        title_species = species_for_time

    hourly_counts = df_species_time["Hour"].value_counts().sort_index()

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=hourly_counts.index, y=hourly_counts.values, ax=ax2)
    ax2.set_title(f"Number of {title_species} Collisions by Hour of Day")
    ax2.set_xlabel("Hour of Day")
    ax2.set_ylabel("Number of Collisions")
    st.pyplot(fig2)

    st.markdown("""
    *Interpretation:*  
    This chart helps verify if collision frequency is higher during early morning and evening hours, as assumed for crepuscular species like deer or moose.
    """)

    st.subheader("📌 Hypothesis 3: Certain counties have more collisions")

    species_options_3 = ["All species"] + sorted(df["Species"].dropna().unique().tolist())
    selected_species_3 = st.selectbox("Select species to view collision distribution by county:", species_options_3)

    if selected_species_3 == "All species":
        df_selected_3 = df.copy()
        title_species = "All Species"
    else:
        df_selected_3 = df[df["Species"] == selected_species_3]
        title_species = selected_species_3

    county_counts = df_selected_3["Lan"].value_counts().sort_values(ascending=False)

    fig3, ax3 = plt.subplots(figsize=(10, 8))
    sns.barplot(y=county_counts.index, x=county_counts.values, ax=ax3)
    ax3.set_title(f"{title_species} Collisions per County")
    ax3.set_xlabel("Number of Collisions")
    ax3.set_ylabel("County")
    st.pyplot(fig3)

    st.markdown("""
    *Interpretation:*  
    This chart shows the regional distribution of wildlife collisions. Some counties consistently report more incidents, possibly due to road density, habitat, or traffic volume.
    """)