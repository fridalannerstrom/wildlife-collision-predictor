import streamlit as st

def run():
    """
    Displays the main project hypotheses that guide both the data analysis and 
    machine learning model. Each hypothesis is motivated by ecological and traffic factors.
    """
    st.title("📌 Project Hypotheses")

    st.markdown("""
This page presents the **main hypotheses** that shaped the exploratory data analysis (EDA) and model development.  
Each hypothesis is rooted in either ecological behavior or traffic-related assumptions.

---

### 🦌 Hypothesis 1: Moose collisions increase during autumn  
**Statement:** Moose collision rates increase during autumn months (September–November).  
**Rationale:** Moose are more active during mating season in the fall, which increases road crossings and collision risk.

---

### 🌅 Hypothesis 2: Collisions are more common at dawn and dusk  
**Statement:** Wildlife collisions occur more frequently during early morning and evening hours.  
**Rationale:** Many wild animals are crepuscular (active at dawn/dusk), which overlaps with times of low driver visibility.

---

### 🗺️ Hypothesis 3: Certain counties report consistently high collision rates  
**Statement:** Some counties have higher wildlife collision rates regardless of season or time.  
**Rationale:** Geographic and environmental factors like forest density, road placement, or animal population could cause persistent risk patterns.

---

These hypotheses serve as the foundation for both the **EDA page** and the **prediction model**.

*See the EDA page for visual analysis supporting or refuting each hypothesis.*
""")