import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def run():
    st.title("📊 Exploratory Data Analysis")
    st.subheader("Hypothesis 1: Moose collisions increase in autumn")

    # Ladda data
    df = pd.read_csv("data/cleaned_data.csv")

    # Filtrera älg
    df_alg = df[df['Viltslag'] == 'Älg']

    # Grupp per månad
    monthly_counts = df_alg['Manad'].value_counts().sort_index()

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=monthly_counts.index, y=monthly_counts.values, ax=ax)
    ax.set_title("Number of Moose Collisions per Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Collisions")

    st.pyplot(fig)