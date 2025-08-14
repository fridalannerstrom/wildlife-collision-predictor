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

# Load environment variables from .env (if any)
load_dotenv()

DEFAULT_LOCAL_PATH = "data/cleaned_data.csv"

def load_clean_data(encoding="utf-8"):
    """
    Loads the cleaned collision dataset.
    
    - Tries to load from CLEAN_DATA_URL (if set), otherwise from local file.
    - Strips column names and certain string columns (County, Municipality, Species)
    - Parses 'Time' column into derived features: Year, Month, Hour, Day_of_Year, etc.
    
    Returns:
        pd.DataFrame: Cleaned dataset ready for analysis or prediction.
    """
    clean_data_url = os.getenv("CLEAN_DATA_URL")

    try:
        # Load data
        if clean_data_url:
            df = pd.read_csv(clean_data_url, encoding=encoding)
        else:
            df = pd.read_csv(DEFAULT_LOCAL_PATH, encoding=encoding)

        # Clean column names and string values
        df.columns = df.columns.str.strip()
        for col in ["County", "Municipality", "Species"]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()

    except pd.errors.ParserError as e:
        raise RuntimeError(
            "Could not parse CSV file. Make sure the URL is a raw CSV and the encoding/delimiter is correct."
        ) from e
    except Exception as e:
        where = "CLEAN_DATA_URL" if clean_data_url else DEFAULT_LOCAL_PATH
        raise RuntimeError(f"Failed to load data from: {where}") from e

    if df.empty:
        raise RuntimeError("CSV file loaded but is empty. Check the data source.")

    # Parse and extract time features
    if "Time" in df.columns:
        df["Time"] = pd.to_datetime(df["Time"], errors="coerce")

        if "Year" not in df.columns:
            df["Year"] = df["Time"].dt.year
        if "Month" not in df.columns:
            df["Month"] = df["Time"].dt.month
        if "Hour" not in df.columns:
            df["Hour"] = df["Time"].dt.hour
        if "Date" not in df.columns:
            df["Date"] = df["Time"].dt.date
        if "Day_of_Year" not in df.columns:
            df["Day_of_Year"] = df["Time"].dt.dayofyear

    return df