import os
import pickle
import joblib
import numpy as np
import pandas as pd
from urllib.request import urlretrieve
from src.data_loader import load_clean_data

# ---- Sökvägar ----
MODEL_PATH = os.path.join("model", "model.pkl.xz")  # komprimerad modell
COLUMNS_PATH = os.path.join("model", "model_columns.pkl")

# ---- URL:er till dina GitHub Release-filer ----
MODEL_URL = "https://github.com/fridalannerstrom/wildlife-collision-predictor/releases/download/model/model.pkl"
COLUMNS_URL = "https://github.com/fridalannerstrom/wildlife-collision-predictor/releases/download/model/model_columns.pkl"


_model = None
_model_cols = None
_unique_values_cache = None

# ---- Ladda modell från disk eller GitHub ----
def _download_if_missing(path: str, url: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        print(f"⬇️ Downloading {url} ...")
        urlretrieve(url, path)
        print(f"✅ Saved to {path}")

def load_model():
    global _model
    if _model is None:
        _download_if_missing(MODEL_PATH, MODEL_URL)
        _model = joblib.load(MODEL_PATH)
    return _model

def load_model_columns():
    global _model_cols
    if _model_cols is None:
        _download_if_missing(COLUMNS_PATH, COLUMNS_URL)
        with open(COLUMNS_PATH, "rb") as f:
            _model_cols = pickle.load(f)
    return _model_cols

# ---- Läs unika värden från datan ----
def load_unique_values():
    global _unique_values_cache
    if _unique_values_cache is None:
        df = load_clean_data()
        
        # Konvertera datumfält om det behövs
        if "Time" in df.columns:
            df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
            if "Month" not in df.columns:
                df["Month"] = df["Time"].dt.month
            if "Year" not in df.columns:
                df["Year"] = df["Time"].dt.year
        
        required = ["County", "Municipality", "Species"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Saknade kolumner i cleaned_data.csv: {missing}")

        counties = sorted([c for c in df["County"].dropna().unique().tolist() if str(c).strip()])
        species = sorted([s for s in df["Species"].dropna().unique().tolist() if str(s).strip()])

        county_to_munis = {}
        for c in counties:
            munis = df.loc[df["County"] == c, "Municipality"].dropna().unique().tolist()
            munis = sorted([m for m in munis if str(m).strip()])
            county_to_munis[c] = munis

        _unique_values_cache = {
            "counties": counties,
            "species": species,
            "county_to_munis": county_to_munis,
        }
    return _unique_values_cache

def get_municipalities_for_county(county: str) -> list:
    uv = load_unique_values()
    return uv["county_to_munis"].get(county, [])

# ---- Matcha modellens features ----
def _one_hot_align(frame: pd.DataFrame, model_cols: list) -> pd.DataFrame:
    X = frame.copy()
    for c in model_cols:
        if c not in X.columns:
            X[c] = 0
    return X[model_cols]

# ---- Skapa feature-rad till modellen ----
def build_feature_row(
    year: int,
    month: int,
    hour: int,
    county: str,
    species: str,
    municipality: str | None = None,
    lat_wgs84: float | None = None,
    long_wgs84: float | None = None,
    day_of_year: int | None = None,
    weekday: str | None = None,
) -> pd.DataFrame:
    import calendar

    # Sätt defaultvärden om saknas
    if municipality is None:
        municipality = "Unknown"
    if lat_wgs84 is None:
        lat_wgs84 = 60.0
    if long_wgs84 is None:
        long_wgs84 = 15.0
    if day_of_year is None:
        day_of_year = pd.Timestamp(year=year, month=month, day=1).dayofyear
    if weekday is None:
        weekday = calendar.day_name[pd.Timestamp(year=year, month=month, day=1).weekday()]

    # Skapa dataframe med originalfeatures
    df = pd.DataFrame({
        "Year": [year],
        "Month": [month],
        "Hour": [hour],
        "County": [county.strip()],
        "Municipality": [municipality.strip()],
        "Species": [species.strip()],
        "Lat_WGS84": [lat_wgs84],
        "Long_WGS84": [long_wgs84],
        "Day_of_Year": [day_of_year],
        "Weekday": [weekday],
    })

    return df

# ---- Kör prediktion ----
def predict_proba_label(X: pd.DataFrame):
    model = load_model()
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)
        if proba.shape[1] == 2:
            score = float(proba[0, 1])
            return score, None, proba
        else:
            idx = int(np.argmax(proba[0]))
            score = float(proba[0, idx])
            return score, None, proba
    else:
        y = model.predict(X)
        label = str(y[0])
        return None, label, None