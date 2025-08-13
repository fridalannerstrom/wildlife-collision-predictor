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

# ---- Automatiska nedladdningar ----
def _download_if_missing(path: str, url: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        print(f"⬇️ Downloading {url} ...")
        urlretrieve(url, path)
        print(f"✅ Saved to {path}")

# ---- Ladda modell & kolumner ----
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

# ---- Läs unika värden från cleaned_data.csv ----
def load_unique_values():
    global _unique_values_cache
    if _unique_values_cache is None:
        df = load_clean_data()
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

# ---- Hjälpfunktion: hämta kommuner per län ----
def get_municipalities_for_county(county: str) -> list:
    uv = load_unique_values()
    return uv["county_to_munis"].get(county, [])

# ---- Matcha modellens exakta kolumner ----
def _one_hot_align(frame: pd.DataFrame, model_cols: list) -> pd.DataFrame:
    X = frame.copy()
    for c in model_cols:
        if c not in X.columns:
            X[c] = 0
    return X[model_cols]

# ---- Bygg feature-rad från användarinmatning ----
def build_feature_row(
    year: int,
    month: int,
    hour: int,
    county: str,
    species: str,
    municipality: str | None = None,
    lat_wgs84: float | None = None,
    long_wgs84: float | None = None,
    day_of_year: int | None = None
) -> pd.DataFrame:
    base = {
        "Year": [year],
        "Month": [month],
        "Hour": [hour],
        "County": [county],
        "Species": [species],
    }
    if municipality is not None:
        base["Municipality"] = [municipality]
    if day_of_year is not None:
        base["Day_of_Year"] = [day_of_year]
    if lat_wgs84 is not None:
        base["Lat_WGS84"] = [lat_wgs84]
    if long_wgs84 is not None:
        base["Long_WGS84"] = [long_wgs84]

    df = pd.DataFrame(base)
    cat_cols = [c for c in ["County", "Municipality", "Species"] if c in df.columns]
    df_dum = pd.get_dummies(df, columns=cat_cols, drop_first=False)
    model_cols = load_model_columns()
    X = _one_hot_align(df_dum, model_cols)
    return X

# ---- Kör modell och returnera sannolikhet + label ----
def predict_proba_label(X: pd.DataFrame):
    model = load_model()
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)
        if proba.shape[1] == 2:
            score = float(proba[0, 1])
            label = "High" if score >= 0.66 else ("Medium" if score >= 0.33 else "Low")
            return score, label, proba
        else:
            idx = int(np.argmax(proba[0]))
            score = float(proba[0, idx])
            label = str(getattr(model, "classes_", [])[idx]) if hasattr(model, "classes_") else f"class_{idx}"
            return score, label, proba
    else:
        y = model.predict(X)
        label = str(y[0])
        return None, label, None