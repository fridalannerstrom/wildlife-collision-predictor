import os
import pickle
import joblib
import numpy as np
import pandas as pd
from src.data_loader import load_clean_data  # 🟢 LAGT TILL

# ---- Sökvägar anpassade till din struktur ----
MODEL_PATH = os.path.join("model", "model.pkl")
COLUMNS_PATH = os.path.join("model", "model_columns.pkl")

_model = None
_model_cols = None
_unique_values_cache = None

def load_model():
    """Ladda din tränade modell (joblib eller pickle)."""
    global _model
    if _model is None:
        try:
            _model = joblib.load(MODEL_PATH)
        except Exception:
            with open(MODEL_PATH, "rb") as f:
                _model = pickle.load(f)
    return _model

def load_model_columns():
    """Ladda listan över EXAKTA kolumner som modellen tränades på."""
    global _model_cols
    if _model_cols is None:
        with open(COLUMNS_PATH, "rb") as f:
            _model_cols = pickle.load(f)  # t.ex. en list[str]
    return _model_cols

def load_unique_values():
    """
    Läser cleaned_data.csv en gång och bygger:
    - counties (lista)
    - species (lista)
    - weekdays (lista)
    - county_to_munis (dict: county -> sorterad lista av municipalities)
    """
    global _unique_values_cache
    if _unique_values_cache is None:
        df = load_clean_data()

        required = ["Weekday", "County", "Municipality", "Species"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Saknade kolumner i cleaned_data.csv: {missing}")

        counties = sorted([c for c in df["County"].dropna().unique().tolist() if str(c).strip()])
        species =  sorted([s for s in df["Species"].dropna().unique().tolist() if str(s).strip()])

        # county -> municipalities
        county_to_munis = {}
        for c in counties:
            munis = df.loc[df["County"] == c, "Municipality"].dropna().unique().tolist()
            munis = sorted([m for m in munis if str(m).strip()])
            county_to_munis[c] = munis

        weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"] \
                   if df["Weekday"].dtype == object \
                   else sorted(df["Weekday"].dropna().unique().tolist())

        _unique_values_cache = {
            "counties": counties,
            "species": species,
            "weekdays": weekdays,
            "county_to_munis": county_to_munis,
        }
    return _unique_values_cache


# --- ny hjälpfunktion ---
def get_municipalities_for_county(county: str) -> list:
    uv = load_unique_values()
    return uv["county_to_munis"].get(county, [])

def _one_hot_align(frame: pd.DataFrame, model_cols: list) -> pd.DataFrame:
    """
    Säkerställ att test-matrisen har EXAKT samma kolumner och ordning
    som vid träning. Saknade kolumner fylls med 0; extra droppas.
    """
    X = frame.copy()
    for c in model_cols:
        if c not in X.columns:
            X[c] = 0
    return X[model_cols]

def build_feature_row(
    year: int,
    month: int,
    hour: int,
    weekday: str,
    county: str,
    species: str,
    municipality: str | None = None,   # <--- NYTT
    lat_wgs84: float | None = None,
    long_wgs84: float | None = None,
    day_of_year: int | None = None
) -> pd.DataFrame:
    base = {
        "Year": [year],
        "Month": [month],
        "Hour": [hour],
        "Weekday": [weekday],
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

    # inkludera Municipality i dummies om den finns
    cat_cols = [c for c in ["Weekday", "County", "Municipality", "Species"] if c in df.columns]
    df_dum = pd.get_dummies(df, columns=cat_cols, drop_first=False)

    model_cols = load_model_columns()
    X = _one_hot_align(df_dum, model_cols)
    return X

def predict_proba_label(X: pd.DataFrame):
    """
    Kör modellen och mappa till enkel label om det är binärt.
    Fungerar även för multiclass (tar högsta sannolikheten).
    """
    model = load_model()

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)
        # Binärt fall → sannolikhet för klass 1
        if proba.shape[1] == 2:
            score = float(proba[0, 1])
            label = "High" if score >= 0.66 else ("Medium" if score >= 0.33 else "Low")
            return score, label, proba
        else:
            # Multiclass → välj högsta sannolikheten
            idx = int(np.argmax(proba[0]))
            score = float(proba[0, idx])
            label = str(getattr(model, "classes_", [])[idx]) if hasattr(model, "classes_") else f"class_{idx}"
            return score, label, proba
    else:
        # Ingen predict_proba → använd predict()
        y = model.predict(X)
        label = str(y[0])
        return None, label, None