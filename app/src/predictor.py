"""
predictor.py

Handles loading of the trained ML model and performing predictions
based on input features. Also includes helper functions to load unique values
from the cleaned dataset for use in dropdowns.
"""

import os
import joblib
import lzma
import numpy as np
import pandas as pd
import streamlit as st
from urllib.request import urlretrieve
from src.data_loader import load_clean_data

# ------------------------------------------------------
# Paths to model files (local and GitHub fallback)
# ------------------------------------------------------

MODEL_PATH = os.path.join("model", "model.pkl.xz")
COLUMNS_PATH = os.path.join("model", "model_columns.pkl")  # optional

MODEL_URL = (
    "https://github.com/fridalannerstrom/wildlife-collision-predictor/"
    "releases/download/model/model.pkl.xz"
)

# ------------------------------------------------------
# Helper: Download model file from GitHub if missing
# ------------------------------------------------------

def _download_if_missing(path: str, url: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        print(f"⬇️ Downloading {url} ...")
        urlretrieve(url, path)
        print(f"✅ Saved to {path}")

# ------------------------------------------------------
# Load model and columns with Streamlit caching
# ------------------------------------------------------

@st.cache_resource
def load_model():
    _download_if_missing(MODEL_PATH, MODEL_URL)
    try:
        with lzma.open(MODEL_PATH, "rb") as f:
            model = joblib.load(f)
        return model
    except Exception as e:
        import traceback
        st.error(f"❌ Failed to load model: {type(e).__name__}: {e}")
        st.text("🧵 Full traceback:")
        st.text(traceback.format_exc())
        raise e

@st.cache_resource
def load_model_columns():
    with open(COLUMNS_PATH, "rb") as f:
        return joblib.load(f)

# ------------------------------------------------------
# Load unique values for dropdowns (cached)
# ------------------------------------------------------

@st.cache_resource
def load_unique_values():
    df = load_clean_data()

    if "Time" in df.columns:
        df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
        if "Month" not in df.columns:
            df["Month"] = df["Time"].dt.month
        if "Year" not in df.columns:
            df["Year"] = df["Time"].dt.year

    required = ["County", "Municipality", "Species"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in cleaned_data.csv: {missing}")

    counties = sorted(df["County"].dropna().unique())
    species = sorted(df["Species"].dropna().unique())

    county_to_munis = {}
    for c in counties:
        munis = df.loc[df["County"] == c, "Municipality"].dropna().unique()
        county_to_munis[c] = sorted([m for m in munis if str(m).strip()])

    return {
        "counties": [c for c in counties if str(c).strip()],
        "species": [s for s in species if str(s).strip()],
        "county_to_munis": county_to_munis,
    }

def get_municipalities_for_county(county: str) -> list:
    uv = load_unique_values()
    return uv["county_to_munis"].get(county, [])

# ------------------------------------------------------
# Build input row from user selections
# ------------------------------------------------------

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

    municipality = municipality or "Unknown"
    lat_wgs84 = lat_wgs84 or 60.0
    long_wgs84 = long_wgs84 or 15.0
    if day_of_year is None:
        day_of_year = pd.Timestamp(year=year, month=month, day=1).dayofyear
    if weekday is None:
        weekday = calendar.day_name[
            pd.Timestamp(year=year, month=month, day=1).weekday()
        ]

    return pd.DataFrame({
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

# ------------------------------------------------------
# Make prediction and return probability and label
# ------------------------------------------------------

def predict_proba_label(X_raw: pd.DataFrame, model):
    """
    Takes raw input, encodes with dummy vars, aligns to model columns, and predicts.
    """
    # One-hot encode input
    X_encoded = pd.get_dummies(X_raw)

    # Load expected column names
    model_columns = load_model_columns()

    # Align columns
    for col in model_columns:
        if col not in X_encoded.columns:
            X_encoded[col] = 0
    X_encoded = X_encoded[model_columns]

    # Predict
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X_encoded)

        if proba.shape[1] == 2:
            score = float(proba[0, 1])
            return score, None, dict(enumerate(proba[0]))
        else:
            idx = int(np.argmax(proba[0]))
            score = float(proba[0, idx])
            return score, None, dict(enumerate(proba[0]))
    else:
        y = model.predict(X_encoded)
        label = str(y[0])
        return None, label, None
