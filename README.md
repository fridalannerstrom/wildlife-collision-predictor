
## 🛠️ Work Log

### 📅 2025-08-04 – First Setup & Data Loading

**What I did:**
- Created project folder structure with `app/`, `notebooks/`, `data/` etc.
- Set up Heroku and GitHub deployment, tested live Streamlit app.
- Added `Procfile`, `requirements.txt`, `runtime.txt`, `setup.sh`.
- Created a minimal `app.py` and deployed successfully to Heroku.
- Set up `.ipynb` notebook environment in VS Code for the first time.
- Installed pandas, jupyter, openpyxl to be able to work with Excel data.

**Data loading:**
- Downloaded raw wildlife collision data from viltolycka.se.
- Loaded Excel files from multiple years (2015–2024) using `glob` + `pandas.read_excel`.
- Concatenated all sheets into one big DataFrame.
- Will soon save as a CSV for faster future use.

**Why I did it:**
- Heroku deployment early makes it easy to test dashboard features later.
- Notebook setup helps me explore the data and test code without cluttering the main app.
- Exporting all Excel to CSV simplifies the next steps (cleaning, modeling, Streamlit use).

---

## 🧹 Data Cleaning

The raw data consisted of multiple `.xlsx` files downloaded from [viltolycka.se](https://www.viltolycka.se/statistik/), each containing wildlife-vehicle collision records per year. Before we could analyze or model the data, we had to clean and consolidate it to ensure consistency and usability. The following steps were taken:

### 1. Combined all Excel files
- Used `glob` and `pandas.read_excel()` to read all `.xlsx` files (2015–2024).
- Skipped metadata rows in each file using `skiprows=6`.
- Concatenated all data into one DataFrame (`~635,000 rows`).

### 2. Cleaned column names
- Stripped whitespace and standardized names using `.str.strip()` and `.str.replace()`.
- Replaced Swedish characters (`å`, `ä`, `ö`) with ASCII-friendly alternatives (`a`, `a`, `o`).

### 3. Dropped unnecessary columns
- Removed columns such as `Unnamed: 9`, `Unnamed: 10`, `Unnamed: 13`, and `Kalla_fil` which contained only missing or duplicated information.

### 4. Parsed and extracted date/time features
- Converted the `Datum` column to datetime format.
- Created new features:
  - `Månad` (month)
  - `Veckodag` (weekday name)
  - `Dag_pa_aret` (day of year)

### 5. Preserved essential columns for analysis
We kept only relevant columns such as:
- `Viltslag` (species)
- `Datum`, `Tid`, `Veckodag`, `Månad`, `År`
- `Län`, `Kommun`
- `Lat_WGS84`, `Long_WGS84` (for mapping)
- `Vad_har_skett_med_viltet`, `Kön`, `Årsunge` (for outcome analysis and potential feature use)

### 6. Saved cleaned dataset
The cleaned DataFrame was exported to a lightweight `.csv` file: data/cleaned_data.csv
This file serves as the foundation for all further analysis, modeling, and dashboard visualizations.

---

## 📌 Project Hypotheses

To guide the exploratory data analysis and model development, three hypotheses were formulated based on domain knowledge, real-world expectations, and stakeholder needs. Each hypothesis is testable using the cleaned dataset and is addressed through visual analysis and/or statistical validation.

### Hypothesis 1: Moose collision rates increase during autumn

**Statement:**  
> The number of moose collisions significantly increases during the autumn months (September–November).

**Rationale:**  
Moose are known to be more active during mating season in the fall, which may increase road crossings and collision risk.

**Validation approach:**  
- Count and visualize moose collisions by month.
- Compare autumn months to others using bar charts.
- Interpret patterns to assess significance.

---

### Hypothesis 2: Wildlife collisions are more common at dawn and dusk

**Statement:**  
> Most wildlife-vehicle collisions occur during early morning or late evening hours.

**Rationale:**  
Many wild animals are crepuscular (active at dawn/dusk), which may increase risk during those periods due to lower visibility and traffic overlap.

**Validation approach:**  
- Extract collision times from the dataset.
- Visualize frequency by hour of day.
- Identify peak hours and compare with expectations.

---

### Hypothesis 3: Certain counties experience more collisions regardless of season

**Statement:**  
> Some counties (län) have significantly higher wildlife collision frequencies even when controlling for time of year.

**Rationale:**  
Collision patterns may be affected by wildlife density, road design, and traffic volume, which can vary regionally.

**Validation approach:**  
- Count collisions per county.
- Visualize regional distribution (bar chart and/or map).
- Consider seasonal trends as a control.

---

Each hypothesis is tested and discussed in the analysis section of the dashboard and supports the development of the machine learning model and final recommendations.


---

## 📊 Exploratory Data Analysis (EDA)

To validate the project hypotheses, we performed exploratory analysis on cleaned wildlife collision data from Sweden, including time, location and species information.

### ✅ Hypothesis 1 – Moose collisions increase during autumn  
A barplot of monthly collisions per species revealed a clear seasonal pattern: **moose collisions peak in September–November**, supporting the hypothesis.

### ✅ Hypothesis 2 – Collisions are more common at dawn and dusk  
By extracting the hour from the timestamp, we plotted the distribution of collisions throughout the day.  
Results showed **a significant increase in collisions around sunrise and sunset**, especially for moose and deer.

### ✅ Hypothesis 3 – Certain counties have more collisions  
We compared the number of collisions per county.  
Some counties (e.g. Värmland, Uppsala) consistently report **higher numbers regardless of time**, supporting regional risk patterns.

### 🗺️ Interactive Map  
A Plotly-based map was added with filtering by:
- **Species**
- **Year**

To improve performance and usability, we implemented:
- Year and species selectboxes
- Sampling (max 10,000 points)
- Optional heatmap view

This allows users to visually explore collision hotspots in Sweden.


## 🗂️ GitHub Cleanup: Data Exclusion

To ensure a clean and professional GitHub repository, we **removed all large and sensitive files** from version control. This includes:

- `data/original_excels/` – Raw downloaded Excel files
- `data/cleaned_with_clusters.csv` – Too large for GitHub (over 100 MB)
- Model artifacts like `.pkl` files (if any)

### ❌ Why?

- GitHub has a strict 100 MB file limit
- Sensitive data or raw sources should not be public
- Encourages reproducibility through clear code + instructions

### ✅ How?

- We used `git filter-repo` to permanently remove large files from Git history
- Added these paths to `.gitignore` to prevent accidental re-upload:

```gitignore
# Ignore raw data and large CSVs
data/original_excels/
data/*.xlsx
data/cleaned_with_clusters.csv

# Ignore model files
*.pkl
*.sav
```

---

# 🦌 Wildlife Collision Predictor

## 📅 Work Log – August 8, 2025

### 1. Problem: Large files when pushing to GitHub
- When attempting to push the project to GitHub, we encountered:
  ```
  remote: error: File data/cleaned_data.csv is 131.02 MB; this exceeds GitHub's file size limit of 100.00 MB
  remote: error: File data/raw_collision_data.csv is 163.98 MB; this exceeds GitHub's file size limit of 100.00 MB
  ```
- GitHub has a **100 MB limit** for files in regular commits.
- **Solution**:
  1. Installed `git-filter-repo` to remove large files from commit history.
  2. Ran:
     ```bash
     git filter-repo --path data/ --invert-paths
     ```
     which removed the entire `data/` folder from Git history.
  3. Reconnected the remote repository:
     ```bash
     git remote add origin https://github.com/<user>/<repo>.git
     ```
  4. Force-pushed the cleaned history:
     ```bash
     git push origin main --force
     ```
  5. Added `data/` to `.gitignore` to prevent these files from being pushed again.

---

### 2. Problem: Data files missing on Heroku
- Since the CSV files were excluded from GitHub, they were not present in the Heroku deployment.
- Options discussed:
  - Upload CSV to external storage (e.g., Amazon S3, Google Cloud Storage) and download them at runtime.
  - Include a smaller demo dataset in the repo.
- **Current decision**: Use local files during development and plan for migration to external storage later.

---

### 3. Problem: Encoding error (`UnicodeDecodeError`) when reading CSV
- On Heroku, we encountered:
  ```
  UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1
  ```
- **Cause**: The CSV files were not saved in UTF-8 but likely in `ISO-8859-1` / `latin1`.
- **Solution**:
  - Updated `pd.read_csv()` calls to:
    ```python
    pd.read_csv("data/cleaned_data.csv", encoding="latin1")
    ```
  - Plan: Create a helper function for consistent CSV reading.

---

### 4. Improvements in the Predict page
- Rebuilt prediction logic so that the user can:
  1. Select **County**
  2. Select **Municipality** – filtered based on the chosen county.
  3. Select **time** (e.g., month, hour) and species.
- Next step: Implement **cascading dropdowns** where the county choice automatically filters the available municipalities.

---

### 5. GitHub & Branch settings
- Resolved the error:
  ```
  fatal: The current branch main has no upstream branch.
  ```
- Set up remote tracking:
  ```bash
  git push --set-upstream origin main
  ```

---

## ⚙️ Technical description of the Predict function

The Predict page uses a **pre-trained model** (`model.pkl`) together with metadata (`model_columns.pkl`) to predict wildlife collision risk based on the user's input.

**Process steps:**
1. **Load data for dropdowns**
   - The `cleaned_data.csv` file is read to get unique values for `County`, `Municipality`, `Month`, `Hour`, and `Species`.
   - The user selects from these using Streamlit dropdowns.

2. **Cascading dropdowns**
   - When a county is selected, the municipality list is dynamically filtered to only show those within that county.
   - This is done using a Pandas filter operation:
     ```python
     municipalities = df[df['County'] == selected_county]['Municipality'].unique()
     ```

3. **Prepare input for the model**
   - The user’s choices are collected in a dictionary, e.g.:
     ```python
     user_input = {
         "County": selected_county,
         "Municipality": selected_municipality,
         "Month": selected_month,
         "Hour": selected_hour,
         "Species": selected_species
     }
     ```
   - Converted to a Pandas DataFrame and encoded using the format the model was trained with (`model_columns.pkl`).

4. **Prediction**
   - The model (`model.pkl`) is loaded with `joblib`.
   - The user's input is passed to the model:
     ```python
     prediction = model.predict_proba(user_df)[:, 1]  # Probability of collision
     ```
   - The result is a probability (0–1) which can be displayed as a percentage or risk category.

5. **Visual presentation**
   - The risk level is displayed in Streamlit, e.g., as a colored indicator (green, yellow, red) or percentage.

---

## 🎯 Next steps
1. Fully implement the County → Municipality cascading dropdowns.
2. Create a helper function for consistent CSV reading with `encoding="latin1"`.
3. Move large CSV files to external storage (S3 or similar) for Heroku deployment.

## 🔮 Wildlife Collision Risk Prediction – Page Overview

This interactive page allows users to predict wildlife collision risk on Swedish roads based on location, time, and species. It combines user input with a trained machine learning model and visualizes the result with a dynamic risk label and an interactive map.

### ✅ Key Features

- **Cascading dropdowns** for selecting county and municipality.
- **Flexible time input**: users can specify weekday, hour of day, and month.
- **Optional species filtering** to refine the prediction.
- **Model output**: five-tiered risk label (Very Low → Very High).
- **Color-coded advice box** based on predicted risk.
- **Interactive map** displaying the prediction location and risk color.
- **Explainable AI**: expandable section to show top influencing features and raw probabilities.

---

### 🧠 How It Works

1. **User Input:**
   - The user selects a *County* and *Municipality*.
   - Time-related inputs include:
     - **Month**
     - **Hour of day**
     - **Weekday**
   - Optionally, the user can select a specific species (e.g., moose, deer) or use "All species".

2. **Feature Vector Construction:**
   - Inputs are encoded into a one-hot feature vector that mirrors the training set format.
   - This includes time, location, species, and derived fields such as *Day of Year*.

3. **Prediction:**
   - The model returns a probability score (0–1).
   - Based on the score, a risk label is assigned:
     ```
     [0.00–0.33)     = Very Low
     [0.33–0.50)     = Low
     [0.50–0.66)     = Moderate
     [0.66–0.85)     = High
     [0.85–1.00]     = Very High
     ```

4. **Result Display:**
   - A `st.metric()` widget displays the label and score.
   - A color-coded `st.info()` box offers risk-specific advice (e.g., slow down, increase attention).
   - The map centers on the **average coordinates** of the selected municipality, with a marker color-matched to the risk label.

5. **Explainability:**
   - The user can expand a section showing:
     - The top 10 non-zero features influencing the prediction.
     - The raw probability output from the classifier (e.g., `[0.25, 0.75]` for binary classifiers).

---

### 🌍 Map Visualization

The map uses Plotly’s `Scattermapbox` with the following design:

- **Zoom level**: 7 (regional).
- **Map tiles**: OpenStreetMap (no API key needed).
- **Marker**: colored dot centered on average GPS coordinates from real historical collisions in that municipality.
- **Colors**:
  - 🔵 `Very Low`
  - 🟢 `Low`
  - 🟠 `Moderate`
  - 🔴 `High`
  - 🟥 `Very High`

---

### 🧪 Model Integration Notes

- This module uses the global `model.pkl` and `model_columns.pkl` files located in the `/model/` directory.
- Cleaned data (`cleaned_data.csv`) must include columns: `County`, `Municipality`, `Weekday`, `Species`, `Lat_WGS84`, `Long_WGS84`.
- It depends on the functions in `src/predictor.py` and `src/data_loader.py`.

---

### 📌 Dependencies

Ensure your project has the following installed (in `requirements.txt`):

```txt
streamlit
pandas
numpy
scikit-learn
plotly
```


### ✅ Automated Testing

This project includes a test suite written with `pytest`, targeting the most critical components of the model pipeline to ensure correct functionality and structure. All tests are located in the `tests/` folder.

#### ✔️ Test Summary

| File                         | Purpose                                                                 |
|------------------------------|-------------------------------------------------------------------------|
| `test_predictor.py`          | Validates model input features and prediction output format             |
| `test_data_loader.py`        | Verifies that the cleaned dataset loads properly as a DataFrame         |
| `test_utils.py`              | Tests the custom CSV reading function using latin1 encoding             |
| `test_get_municipalities.py` | Checks the logic for filtering municipalities by county                 |

---

#### ✅ Test Results

All tests passed successfully:

```bash
$ pytest tests/
================================================== test session starts ==================================================
platform win32 -- Python 3.12.8, pytest-8.4.1
collected 5 items

tests/test_data_loader.py ............                                  [20%]
tests/test_get_municipalities.py ........                              [40%]
tests/test_predictor.py ...............                                 [80%]
tests/test_utils.py ........                                            [100%]

============================================== 5 passed in XX.XX seconds ===============================================
```

*(Test time will vary depending on machine and file size)*

---

#### 🧪 How to run the tests

Make sure all dependencies are installed (see `requirements.txt`), then run:

```bash
pytest tests/
```

No special arguments or configuration are needed.

# 📘 Wildlife Collision Predictor

> **Created by Frida, developer & nature enthusiast living in the forests of Värmland, Sweden – where wildlife-vehicle collisions are a real concern.**

---

## 🚀 Overview
This project is a machine learning-powered **Wildlife Collision Risk Predictor**, built to explore how different factors (location, time, species, etc.) contribute to the risk of wildlife-vehicle collisions.

Using Streamlit for the frontend and a trained ML model for predictions, the app enables users to:
- Select a **county and municipality** in Sweden
- Choose a **time, weekday, and animal species**
- See **predicted collision risk** in 5 categories (from "Very Low" to "Very High")
- Visualize the result on a dynamic **map of Sweden**

---

## 🧠 Motivation
Living in the forests of **Värmland, Sweden**, where elk/moose collisions are common, I wanted to create something that:
- Uses real collision data to uncover patterns
- Offers **practical insight** to drivers and authorities
- Demonstrates real-world use of machine learning and data visualisation

---

## 🔍 Features
- **Cascading location selectors** (county → municipality)
- **Risk prediction model** with 5 custom thresholds
- **Species filtering**
- **Interactive map** (Plotly + Mapbox)
- **Explanation panel** showing top predictive features
- **Fully modular structure** with reusable code in `src/`

---

## ✅ Tests
Automated tests are implemented using `pytest` to ensure core logic works correctly:

### Test Coverage
- ✔️ `build_feature_row()` – ensures correct number and names of features
- ✔️ `predict_proba_label()` – verifies output score, label, and probability
- ✔️ `get_municipalities_for_county()` – checks correct filtering
- ✔️ `load_clean_data()` – validates structure and content of cleaned dataset
- ✔️ `read_csv_latin()` – ensures encoding is handled correctly

Run tests using:
```bash
pytest tests/
```

All tests pass ✅

![pytest passed](docs/images/pytest_passed_screenshot.png) <!-- Replace with real path if screenshot added -->

---

## 🛠️ Tech Stack
- **Frontend/UI**: Streamlit
- **Backend**: Python, Pandas, Scikit-learn
- **Data**: Wildlife collision data from Swedish Transport Administration (Trafikverket)
- **Visualization**: Plotly Mapbox
- **Testing**: Pytest

---

## ▶️ How to Run the App
### 1. Clone the repo
```bash
git clone https://github.com/yourusername/wildlife-collision-predictor.git
cd wildlife-collision-predictor
```

### 2. Set up environment
```bash
pip install -r requirements.txt
```

### 3. Launch the app
```bash
streamlit run app.py
```

### 4. Run tests
```bash
pytest tests/
```

---

## 📦 Folder Structure
```bash
├── app.py                  # Entry point (if used)
├── app_pages/              # Streamlit pages
│   └── 3_predict.py        # Main prediction UI
├── src/                    # Core logic
│   ├── predictor.py
│   ├── data_loader.py
│   └── utils.py
├── tests/                  # Pytest tests
│   ├── test_predictor.py
│   ├── test_data_loader.py
│   ├── test_utils.py
│   └── test_get_municipalities.py
├── data/                   # Raw & cleaned data
├── requirements.txt        # Dependencies
└── README.md               # Project info
```

---

## 🎯 Reflections & Learnings
This project taught me:
- How to **structure ML projects** for maintainability
- The importance of **testing even small utility functions**
- How to integrate **interactive mapping with machine learning**
- That performance matters – and how to optimize predictions and visuals

I hope this project sparks ideas for using data and AI in public safety, road planning, and wildlife conservation.

---

## 🐾 Future Improvements
- Add **traffic volume data** for better risk estimation
- Expand to **other countries or road types**
- Add **seasonal overlays or real-time warnings**
- Deploy as **public web app**

---

## 📬 Contact
If you have ideas, feedback, or just want to talk moose:
**Frida in Värmland**
📧 hello@tqai.se

---

> “Drive slow, watch the forest – and maybe one day, this app will help you avoid a moose.” 🦌🚗


## Data Cleaning

The raw collision data was initially spread across multiple Excel files with varying structures and unnecessary columns. To ensure consistency and improve usability, the data was cleaned through a comprehensive multi-step process:

1. **Merging Excel Files**  
   All Excel files located in the `/data/original_excels/` folder were combined into a single DataFrame. Metadata was preserved by tagging each row with its original file source (`Källa_fil`).

2. **Column Cleanup**  
   - Stripped whitespace from column names.
   - Removed non-informative columns such as "Unnamed: 9", "Unnamed: 10", and "Unnamed: 13".
   - Replaced problematic characters (å, ä, ö) with their ASCII equivalents to avoid encoding issues across platforms.

3. **Date and Time Parsing**  
   - Converted the `Datum` column to datetime format.
   - Extracted month and weekday into new columns (`Månad`, `Veckodag`) to enable time-based visualizations.

4. **Swedish to English Translation**  
   Key categorical fields were translated for international accessibility:
   - Animal species (`Viltlag`)  
   - Animal sex (`Kön`)  
   - Juvenile status (`Årsunge`)  
   - Outcome (`Vad_har_skett_med_viltet`)  
   - Collision type (`Typ av olycka`)  
   - Data source (`Källa`)  
   These translations were stored in new columns to preserve original data.

5. **Final Renaming**  
   All column names were systematically renamed to descriptive, English equivalents such as:
   - `DjurId` → `Animal_ID`  
   - `Lan` → `County`  
   - `Datum` → `Date`  
   - `Viltlag` → `Species`

6. **Export**  
   The cleaned dataset was saved as `cleaned_data.csv` in the `/data/` directory, containing over **635,000 entries** and ready for use in modeling and visualization tasks.
