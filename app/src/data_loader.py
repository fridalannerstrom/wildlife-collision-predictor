"""
data_loader.py

Loads the cleaned wildlife collision dataset from either a remote GitHub URL
or a local CSV file. Handles basic cleaning of column names, data types,
and extracts temporal features from timestamps.

Used throughout the app to provide consistent access to data.
"""

import os
import pandas as pd
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env (if any)
load_dotenv()

DEFAULT_LOCAL_PATH = "data/cleaned_data.csv"


@st.cache_data
def load_clean_data(encoding="utf-8"):
    """
    Loads the cleaned collision dataset.

    - Tries to load from CLEAN_DATA_URL (if set), otherwise from local file.
    - Strips column names and string columns: County, Municipality, Species
    - Parses 'Time' column into derived features:
      Year, Month, Hour, Day_of_Year, etc.

    Returns:
        pd.DataFrame: Cleaned dataset ready for analysis or prediction.
    """
    clean_data_url = os.getenv("CLEAN_DATA_URL")

    try:
        if clean_data_url:
            df = pd.read_csv(clean_data_url, encoding=encoding)
        else:
            df = pd.read_csv(DEFAULT_LOCAL_PATH, encoding=encoding)

        # Basic cleanup
        df.columns = df.columns.str.strip()
        for col in ["County", "Municipality", "Species"]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()

        if "Time" in df.columns:
            df["Time"] = pd.to_datetime(df["Time"], errors="coerce")

            # Only create new columns if they don’t exist
            df["Year"] = df.get("Year", df["Time"].dt.year)
            df["Month"] = df.get("Month", df["Time"].dt.month)
            df["Hour"] = df.get("Hour", df["Time"].dt.hour)
            df["Day_of_Year"] = df.get("Day_of_Year", df["Time"].dt.dayofyear)
            df["Date"] = df.get("Date", df["Time"].dt.date)

    except pd.errors.ParserError as e:
        raise RuntimeError("❌ Failed to parse CSV. Check format.") from e
    except Exception as e:
        where = "CLEAN_DATA_URL" if clean_data_url else DEFAULT_LOCAL_PATH
        raise RuntimeError(f"❌ Failed to load data from {where}: {e}") from e

    if df.empty:
        raise RuntimeError("❌ CSV file loaded but is empty.")

    return df
