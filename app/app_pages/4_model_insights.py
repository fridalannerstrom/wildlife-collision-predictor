import streamlit as st
import pandas as pd

def run():
    """
    Streamlit page: Model Insights

    Describes how the model was trained, what features it uses, how it performs,
    and how it compares to a baseline model.
    """
    st.title("Model Insights")
    st.markdown("""
This page provides insights into the machine learning model powering the prediction system,
including its purpose, design, training process, performance, and limitations.
""")

    # -----------------------------
    # Model Summary
    # -----------------------------
    st.subheader("Model Summary")
    st.markdown("""
The prediction model is a **supervised machine learning classifier** trained on wildlife collision data
reported across Sweden between 2015 and 2023.

It uses a pipeline with:
- **One-hot encoding** for categorical features
- **Scaling** for numerical values
- A **classification algorithm** (Random Forest)

Features used for prediction include:
- County, Municipality, Species
- Month, Hour, Day of Year, Weekday
- Latitude & Longitude (approximate)

The model is exported as `model.pkl` and loaded dynamically in the Streamlit app.
""")

    # -----------------------------
    # Hypotheses
    # -----------------------------
    st.subheader("Model Hypotheses")
    st.markdown("""
The model is designed to reflect real-world behavioral patterns among wildlife, based on the following hypotheses:

**Hypothesis 1:** Moose collision rates increase during autumn.  
*Reason:* Mating season increases movement.

**Hypothesis 2:** Collisions are more common at dawn and dusk.  
*Reason:* Many species are crepuscular.

**Hypothesis 3:** Some counties report consistently high collision risk.  
*Reason:* Differences in traffic volume, habitat, and wildlife populations.
""")

    # -----------------------------
    # Training Data
    # -----------------------------
    st.subheader("Training Data")
    st.markdown("""
The model was trained on a **cleaned dataset** (`cleaned_data.csv`) containing more than **100,000 rows**
of reported wildlife collisions.

Original data included:
- Date and time of collision
- Species
- Location: County, Municipality, Latitude/Longitude
- Outcome (e.g. Euthanized, Dead at crash site)

Engineered features:
- **Month, Hour, Day_of_Year, Weekday**
- Cleaned categories for county, species, etc.
""")

    # -----------------------------
    # Baseline vs. Final Model
    # -----------------------------
    st.subheader("Baseline vs. Final Model")

    st.markdown("""
To validate model performance, a **baseline model** (`DummyClassifier`) was trained using a naive strategy
that always predicts the most frequent class ("no collision").

| Model              | Accuracy | F1 Score |
|--------------------|----------|----------|
| Baseline (Dummy)   | 41%      | 0.00     |
| Final Model (RF)   | 83%      | 0.82     |

➡️ This shows the final model learned meaningful patterns far beyond chance level.
""")

    # -----------------------------
    # Prediction Categories
    # -----------------------------
    st.subheader("Risk Classification Thresholds")
    st.markdown("""
Predictions are converted into 5 risk categories based on **adjusted model score**:

| Risk Level   | Adjusted Score Range |
|--------------|----------------------|
| Very Low     | < 0.35               |
| Low          | 0.35 – 0.55          |
| Moderate     | 0.55 – 0.75          |
| High         | 0.75 – 0.92          |
| Very High    | ≥ 0.92               |

The adjustment helps calibrate overconfident probabilities and ensures better distribution across categories.
""")

    # -----------------------------
    # Final note
    # -----------------------------
    st.success("You can test the live model predictions under the 'Prediction' page using real-time inputs.")

if __name__ == "__main__":
    run()