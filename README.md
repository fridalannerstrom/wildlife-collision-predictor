
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

---

## 🤖 Predictive Modeling

To predict **wildlife collision risk** for a given time and place, we built a binary classification model:

### 🎯 Objective  
Predict whether a given combination of **location (GPS cluster)** and **time (hour)** is considered a **high-risk situation**.

### 🧪 Target Variable: `High_Risk`  
We defined "high-risk" zones as the **top 20% most collision-prone cluster-hour combinations** in the dataset.

### 🧠 Feature Engineering  
We created the following features:
- `Cluster_ID` – derived using KMeans clustering (n=100) on GPS coordinates  
- `Hour` – extracted from timestamp  
- `Month`, `Weekday` – categorical time features  
- One-hot encoding was used for `Weekday`

### 🧱 Model  
We trained a **RandomForestClassifier** with:

```python
RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
📈 Results
Accuracy: TBD

Feature Importance:

Cluster_ID ≈ 70%

Hour ≈ 25%

Other features (weekday/month) had minor influence

This confirms that location and time of day are the primary drivers of collision risk.

💾 Model Export
The trained model will be saved as model.pkl and used in the Streamlit dashboard to:

Predict risk for user-input values

Visualize model insights (coming in “Model Insights” section)