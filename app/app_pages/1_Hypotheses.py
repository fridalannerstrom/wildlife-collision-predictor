import streamlit as st

def run():
    st.title("Project Hypotheses")

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

---

These hypotheses guide the analysis and prediction strategy in the dashboard.
""")
