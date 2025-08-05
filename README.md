
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

### 📁 1. Combined all Excel files
- Used `glob` and `pandas.read_excel()` to read all `.xlsx` files (2015–2024).
- Skipped metadata rows in each file using `skiprows=6`.
- Concatenated all data into one DataFrame (`~635,000 rows`).

### 🧼 2. Cleaned column names
- Stripped whitespace and standardized names using `.str.strip()` and `.str.replace()`.
- Replaced Swedish characters (`å`, `ä`, `ö`) with ASCII-friendly alternatives (`a`, `a`, `o`).

### 🗑️ 3. Dropped unnecessary columns
- Removed columns such as `Unnamed: 9`, `Unnamed: 10`, `Unnamed: 13`, and `Kalla_fil` which contained only missing or duplicated information.

### 🗓️ 4. Parsed and extracted date/time features
- Converted the `Datum` column to datetime format.
- Created new features:
  - `Månad` (month)
  - `Veckodag` (weekday name)
  - `Dag_pa_aret` (day of year)

### 🦌 5. Preserved essential columns for analysis
We kept only relevant columns such as:
- `Viltslag` (species)
- `Datum`, `Tid`, `Veckodag`, `Månad`, `År`
- `Län`, `Kommun`
- `Lat_WGS84`, `Long_WGS84` (for mapping)
- `Vad_har_skett_med_viltet`, `Kön`, `Årsunge` (for outcome analysis and potential feature use)

### 💾 6. Saved cleaned dataset
The cleaned DataFrame was exported to a lightweight `.csv` file: data/cleaned_data.csv
This file serves as the foundation for all further analysis, modeling, and dashboard visualizations.