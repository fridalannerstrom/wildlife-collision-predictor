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

    # Välj art
    selected_species = st.selectbox("Select species to view monthly collisions:", df["Species"].unique())

    # Filtrera
    df_selected = df[df["Species"] == selected_species]
    monthly_counts = df_selected["Manad"].value_counts().sort_index()

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=monthly_counts.index, y=monthly_counts.values, ax=ax)
    ax.set_title(f"Number of {selected_species} Collisions per Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Collisions")
    st.pyplot(fig)

    st.markdown("""
    *Interpretation:*  
    This visualization helps confirm whether certain species, such as moose, show increased collision rates in autumn. Similar patterns may or may not be visible for other species.
    """)