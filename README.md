
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
```
### 📈 Results
Accuracy: TBD

Feature Importance:

Cluster_ID ≈ 70%

Hour ≈ 25%

Other features (weekday/month) had minor influence

This confirms that location and time of day are the primary drivers of collision risk.

### 💾 Model Export
The trained model will be saved as model.pkl and used in the Streamlit dashboard to:

Predict risk for user-input values

Visualize model insights (coming in “Model Insights” section);

---

## 🧠 Model Training and Prediction

After performing EDA and clustering GPS coordinates into 100 regional clusters using KMeans, we proceeded to build a classification model to **predict high-risk wildlife collision scenarios**.

### 🎯 Problem Definition

We defined "High Risk" as the top 20% of cluster+hour combinations with the highest collision frequency. Each data point was labeled as `High_Risk = 1` or `0` accordingly.  

The goal was to train a model that predicts whether a specific time/location combination (based on cluster, hour, weekday, month) represents a high-risk situation.

### 🧪 Features Used

The final features selected based on feature importance were:

- `Cluster_ID` (clustered GPS region)
- `Hour` (of day)
- `Month`
- `Weekday` (converted to one-hot encoding)

### ⚙️ Model Pipeline

We used a Random Forest Classifier from `scikit-learn`:

- Train/test split: 80/20
- Model evaluation metrics: Accuracy, Precision, Recall, F1 Score
- Feature importance was plotted and guided feature selection

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Features and target
X = df[["Cluster_ID", "Hour", "Month", "Weekday_Monday", ...]]
y = df["High_Risk"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

# Model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
```

---

## 🧪 Interactive Prediction (Streamlit)

In the **"Predict"** page of the Streamlit app, users can now interactively:

1. Choose a location (by selecting cluster or clicking on a map)
2. Choose time parameters (hour, month, weekday)
3. View the predicted risk level (with probability)
4. View the cluster region on an interactive map (with highlighted region)
5. View historical collisions from that cluster

This allows stakeholders (like traffic planners or drivers) to simulate upcoming routes and times and get a real-time estimate of collision risk.

---

## 🗺️ New Map Feature

We replaced the confusing “Cluster ID” dropdown with an **interactive map**, where the user can:

- Click on a cluster point to select it
- Immediately see predicted risk
- Visually understand where that cluster lies

We use `plotly.express.scatter_mapbox` to show cluster centroids and historical collisions for the selected region.

---

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

## ✅ Summary of What We Achieved

- ✅ Cleaned and merged 10 years of real collision data
- ✅ Translated all variables to English
- ✅ Clustered GPS coordinates using KMeans
- ✅ Engineered time-based features
- ✅ Defined high-risk collisions and trained model
- ✅ Built full Streamlit app with:
  - Interactive EDA
  - Species insights
  - Risk prediction based on location + time
  - Map with visual cluster selection
- ✅ Cleaned Git history and maintained a shareable GitHub repo