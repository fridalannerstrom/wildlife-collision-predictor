# 🦌🚗 Wildlife Collision Predictor


## Overview
This Streamlit-powered machine learning app predicts **wildlife collision risk** on Swedish roads based on:
- Location (county + municipality)
- Time (month, hour)
- Animal species

The app outputs a **five-tier risk level**, color-coded for clarity, and displays the selected location on an interactive map. It also includes an **explainable AI panel**, interactive EDA visualizations, and a comprehensive model insights section.

👉 [**Try the app live here**](https://wildlife-collision-risk-app-832a274b12fb.herokuapp.com/)

---

## Motivation
Wildlife-vehicle collisions are a serious issue in Sweden, particularly in forested regions. This project was built to:
- Explore real collision patterns in Sweden
- Provide practical insights to drivers, municipalities, and insurers
- Showcase a real-world ML application that informs public safety and conservation

---

## Features
- ✅ **Cascading dropdowns**: County → Municipality (based on cleaned data mapping)
- ✅ **Time-based input**: Month, Hour
- ✅ **Species filtering**: Moose, deer, boar, etc.
- ✅ **Five-tier risk classification**: Very Low → Very High
- ✅ **Color-coded advice box** based on predicted risk
- ✅ **Interactive map** using Plotly and OpenStreetMap
- ✅ **Explainable AI**: expandable section showing feature values & raw probabilities
- ✅ **Tested pipeline** with automated unit tests for key functionality

![Prediction Page Screenshot](images/predict_page.png)

![Prediction Page Result Screenshot](images/predict_result.png)

---

## Folder Structure
```
├── app.py                  # Entry point
├── app_pages/              # Streamlit pages (EDA, Predict, Model Insights, Hypotheses)
├── src/                    # Core logic
│   ├── predictor.py        # Model loading, prediction, feature construction
│   └── data_loader.py      # Data reading and preprocessing
├── model/                  # Trained model + engineered columns
├── data/                   # Cleaned data (excluded from GitHub)
├── notebooks/              # Jupyter Notebooks for EDA, cleaning, modeling
├── tests/                  # Automated unit tests
├── requirements.txt
└── README.md
```

---

## How It Works

### 1. User Input
The user selects:
- A *county* and *municipality*
- Month and hour
- An optional species (e.g. Moose)

⚠️ Although weekday was initially considered as a feature, it was removed from the final model. The reasoning is simple: wildlife behavior doesn’t change depending on whether it’s a Monday or a Saturday. What truly affects collision risk are natural rhythms like time of day and seasonal patterns — not human constructs like weekdays. Including weekday added noise without contributing to predictive accuracy.

### 2. Feature Vector Construction
- Features are combined into a one-row `DataFrame`
- Raw values are passed into the trained pipeline (which handles one-hot encoding + scaling)

### 3. Prediction
- The Random Forest classifier returns a probability score (0–1)
- Score is adjusted using a power curve (`score ** 2.5`) to reduce overconfidence
- Score is mapped to one of five risk levels:
```
[0.00–0.35]   = Very Low
[0.35–0.55]   = Low
[0.55–0.75]   = Moderate
[0.75–0.92]   = High
[0.92–1.00]   = Very High
```

### 4. Display
- `st.metric()` shows the **risk label** and **adjusted score**
- Color-coded `st.info()` offers safety advice (e.g., slow down, stay alert)
- A Plotly map centers on average GPS location for the municipality
- Expandable panel displays top 10 numeric features and raw prediction probabilities

---

## Modeling
### Target: Wildlife Collision Risk
- Binary classification task (collision likely / not likely)
- Trained on real collision data from [viltolycka.se](https://www.viltolycka.se/statistik/)

### Features
- **Categorical:** County, Municipality, Species, Weekday
- **Temporal:** Month, Hour
- **Spatial:** Latitude and Longitude

### Model Pipeline
- `ColumnTransformer` with:
  - `OneHotEncoder` (categorical)
  - `StandardScaler` (numerical)
- `RandomForestClassifier`
- GridSearchCV tuning over 6 hyperparameters, each with 3 values:
  - `n_estimators`, `max_depth`, `min_samples_split`, `min_samples_leaf`, `max_features`, `bootstrap`

### Performance
| Model              | Accuracy | F1 Score |
|--------------------|----------|----------|
| Baseline (Dummy)   | 41%      | 0.00     |
| Final Model (RF)   | 83%      | 0.82     |

![Classification Report and Confusion Matrix](images/model.png)

The confusion matrix confirms strong performance across all classes, particularly for "Very High" and "Very Low" risk levels. Some overlap is expected between adjacent categories such as "Low" and "Moderate".

---

## Hypotheses
The following hypotheses were formulated and validated using visual analytics:

### Hypothesis 1: Moose collisions increase in autumn
- Supported by clear spike in September–November

### Hypothesis 2: Collisions more common at dawn/dusk
- Supported by hourly histogram of moose and deer collisions

### Hypothesis 3: Certain counties report more collisions consistently
- Värmland, Uppsala, and Jämtland stand out across years

![Moose Collisions per Month](images/moose_collisions.png)

---

## Deployment
- Hosted on **Heroku** via `Procfile`, `setup.sh`, and `requirements.txt`
- Model files downloaded dynamically from **GitHub Releases**
- `.csv` files are excluded from Git and GitHub to stay under the 100MB limit

---

## Run Locally
```bash
# 1. Clone repo
$ git clone https://github.com/yourusername/wildlife-collision-predictor.git
$ cd wildlife-collision-predictor

# 2. Install dependencies
$ pip install -r requirements.txt

# 3. Launch app
$ streamlit run app.py

# 4. Run tests
$ pytest tests/
```

---

## Automated Testing
This project includes a suite of automated tests using **pytest** to ensure correctness and maintainability.

### Test Summary
| File                         | Purpose                                                                 |
|------------------------------|-------------------------------------------------------------------------|
| `test_predictor.py`          | Verifies model input shape, output format, and engineered columns       |
| `test_data_loader.py`        | Ensures data loads correctly and has essential fields like "County"     |
| `test_get_municipalities.py` | Confirms that cascading dropdown logic works as expected                |
| `test_utils.py` *(optional)* | Planned for reusable utility tests                                      |

### Example Assertion Checks
- `build_feature_row()` contains expected columns
- `predict_proba_label()` returns correct data types (score, label, proba)
- `load_model_columns()` includes both `cat_` and `num_` prefixed features

### How to Run
```bash
pytest tests/
```
All tests pass ✅

---

## Work Log Highlights

### Setup & Cleaning
- Combined 10 Excel files with over 635,000 rows
- Cleaned, renamed, and translated columns (e.g. "Viltlag" → "Species")
- Parsed and extracted Month, Hour, Weekday, Day of Year

### Modeling
- Ran multiple pipelines and models in `modeling.ipynb`
- Chose Random Forest as best tradeoff between performance and interpretability

### Baseline Risk Table
- Created min-max normalized `risk_score` per county/species/month/hour
- Saved to `baseline_risk.csv` for interpretability

### Dashboard
- Four Streamlit pages:
  - `Project Hypotheses`
  - `Exploratory Data Analysis`
  - `Risk Prediction`
  - `Model Insights`
- Added expandable explainability and confidence reporting

---

## Known Issues & Limitations

Despite being a functional and well-tested app, there are a few known limitations that could be addressed in future iterations:

- **Performance (Speed):**  
  The app is currently slow, especially during initial load or prediction. This is partly due to:
  - Large CSV files being read at runtime instead of stored in a database or cached.
  - Model file download/loading from GitHub Release (especially cold start on Heroku).
  - Use of Plotly map visualizations, which can be heavy in browser rendering.

- **Simplified Feature Set:**  
  Some potentially important features are missing (e.g. **traffic density**, **road type**, **vegetation type**) due to lack of available data.

- **Imbalanced Data:**  
  Wildlife collisions are sparse events. Even though oversampling was not used, class imbalance could affect generalization.

- **No persistent database:**  
  The app doesn't use a database — all predictions are ephemeral. This limits its use in real monitoring or historical trend analysis.

- **Static dropdowns:**  
  Users must manually select county and municipality from dropdowns. A more intuitive UX might allow clicking directly on the map or using GPS.

---

## Learnings & Reflections
- Streamlit made rapid UI prototyping easy and powerful
- GitHub Releases is a smart workaround for model file hosting
- Learned the importance of data cleaning, encoding, and feature alignment
- Building custom tests gave me confidence before deployment

---

## Future Work
If I were to continue developing this app, here are some areas I’d prioritize:

1. **Speed Optimization**
   - Cache model and data loading using `@st.cache_data` or similar.
   - Host data and model files on faster services (e.g. Amazon S3, Firebase).
   - Replace full-data filtering with pre-aggregated lookup tables or API endpoints.

2. **Add More Predictive Features**
   - Integrate road type (e.g. highway, forest road).
   - Add real-time traffic or weather data to refine predictions.
   - Include species-specific movement patterns if available.

3. **Map-First Interaction**
   - Let users click a location on the map and get prediction directly.
   - Implement bounding-box selection or route-based predictions.

4. **Trend & Reporting Tools**
   - Allow exporting reports or weekly risk summaries per region.
   - Add heatmaps or risk trends over time.

5. **Model Retraining Pipeline**
   - Set up scripts to automate model retraining as new collision data is added.
   - Version models properly and track performance over time.

6. **Use a Database**
   - Store prediction logs or allow users to save predictions for analysis.
   - Enable user accounts for personalized dashboards or areas of interest.

7. **Admin Dashboard**
   - For municipalities or researchers: ability to monitor top risk areas, download data, and simulate what-if scenarios.

8. **Mobile Adaptation**
   - Optimize layout for mobile.
   - Consider building a native app with same backend logic using a framework like Flutter or React Native.

---

## Data Notice
Collision data is provided by Trafikverket/Viltolycksradet and used for non-commercial, educational purposes.

---


> "Drive slow, watch the forest — and maybe one day, this app will help you avoid a moose." 🦌🚗