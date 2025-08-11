import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from src.data_loader import load_clean_data
from src.predictor import load_model

def run():
    st.title("🧠 Model Insights")
    st.markdown("""
    This page provides insight into the model's training, performance, and behavior.
    """)

    # ---- 1. Model Description ----
    st.subheader("📦 Model Description")
    st.markdown("""
    - **Type:** Logistic Regression  
    - **Target:** Predict wildlife collision risk (Low, Medium, High)  
    - **Training Data:** Cleaned dataset of wildlife collisions in Sweden  
    - **Features used:**  
        - Time-related: hour, weekday, month, day of year  
        - Location-related: county, municipality, coordinates  
        - Animal species  
    """)

    # ---- 2. Model Performance (static for now) ----
    st.subheader("📈 Model Performance (on training data)")
    st.markdown("""
    Since the main goal was deployment and explainability, the model was evaluated using:
    
    - **Accuracy:** ~82%  
    - **Precision/Recall (High risk):** ~0.85 / ~0.78  
    - **Cross-validation:** 5-fold CV with similar results

    > ⚠️ Note: these numbers are approximations for demonstration. In production, you would use a proper evaluation set.
    """)

    # ---- 3. Feature Importance ----
    st.subheader("🔍 Top 10 Most Influential Features")
    model = load_model()

    if hasattr(model, "coef_"):
        coefs = model.coef_[0]
        feature_names = model.feature_names_in_ if hasattr(model, "feature_names_in_") else range(len(coefs))
        importance_df = pd.DataFrame({"feature": feature_names, "coefficient": coefs})
        top10 = importance_df.reindex(importance_df.coefficient.abs().sort_values(ascending=False).index).head(10)

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="coefficient", y="feature", data=top10, ax=ax)
        ax.set_title("Top 10 Most Important Features (Logistic Regression Coefficients)")
        st.pyplot(fig)
    else:
        st.info("Feature importance not available for this model.")
    
    # ---- 4. Model Limitations ----
    st.subheader("🚧 Limitations")
    st.markdown("""
    - The model may reflect data imbalance (e.g., more moose collisions in Värmland).
    - It does not yet include traffic volume, road types, or weather – which could greatly improve accuracy.
    - Coordinates are only averaged per municipality, which limits map precision.

    > Despite these limitations, the model offers explainable, interpretable predictions suitable for public-facing use.
    """)