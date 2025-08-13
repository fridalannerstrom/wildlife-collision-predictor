import streamlit as st
import pandas as pd

def run():
    st.title("🧠 Model Insights")
    st.markdown("""
This page provides background on the machine learning model, hypotheses behind the predictions, and how the model was built and evaluated.
""")

    # --- Model Summary ---
    st.subheader("📌 Model Summary")
    st.markdown("""
The prediction model is a supervised machine learning classifier trained on several years of wildlife collision data across Sweden.

It uses features such as:
- **County**
- **Municipality**
- **Species**
- **Month**
- **Hour of day**
- **Weekday**
- **Day of Year**

The model was trained using a pipeline that included one-hot encoding of categorical features and a classification algorithm (e.g. Random Forest or similar).  

The trained model is saved as `model/model.pkl` and the list of training columns as `model/model_columns.pkl`.
""")

    # --- Hypotheses ---
    st.subheader("📊 Hypotheses Behind the Model")
    st.markdown("""
### Hypothesis 1  
**Moose collision rates increase during autumn months (September–November).**  
*Rationale:* Moose are more active during mating season, increasing road crossings and collision risk.

---

### Hypothesis 2  
**Wildlife collisions are more common at dawn and dusk.**  
*Rationale:* Many animals are crepuscular (active at dawn/dusk), which aligns with times of reduced visibility for drivers.

---

### Hypothesis 3  
**Certain counties experience more wildlife collisions regardless of time of year.**  
*Rationale:* Geographic and environmental differences (e.g. forest coverage, traffic density) may result in consistent regional risk patterns.
""")

    # --- Data Info ---
    st.subheader("📁 Training Data")
    st.markdown("""
The model was trained on a cleaned dataset (`cleaned_data.csv`) containing over 100,000 rows of reported wildlife collisions. The raw dataset included:
- Date and time of collision
- Animal species
- Location (county, municipality, coordinates)
- Outcome (e.g., euthanized, dead at crash site)

After cleaning, new features like **Month**, **Hour**, and **Day_of_Year** were extracted to support time-based predictions.
""")

    # --- Performance Note ---
    st.subheader("⚙️ Model Performance")
    st.markdown("""
Due to project scope and runtime constraints, the final model was evaluated manually and validated through real-time predictions in the app.

The risk levels are classified into five categories based on prediction probability:
- Very Low (score < 0.33)
- Low
- Moderate
- High
- Very High (score > 0.85)
""")

    st.success("Model predictions are live in the Prediction page – try different inputs to explore!")


if __name__ == "__main__":
    run()