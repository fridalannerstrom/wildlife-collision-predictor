# src/baseline_loader.py
import os
import pandas as pd
import requests
from io import BytesIO
import gzip

BASELINE_URL = "https://github.com/fridalannerstrom/wildlife-collision-predictor/releases/download/processed_data/baseline_risk.csv"
LOCAL_PATH = "data/processed/baseline_risk.csv"

def load_baseline_risk():
    if not os.path.exists(LOCAL_PATH):
        print("⬇️ Downloading baseline_risk.csv.gz from GitHub...")
        os.makedirs(os.path.dirname(LOCAL_PATH), exist_ok=True)
        r = requests.get(BASELINE_URL)
        r.raise_for_status()
        with open(LOCAL_PATH, "wb") as f:
            f.write(r.content)
        print("✅ Download complete.")

    # Load from compressed CSV
    return pd.read_csv(LOCAL_PATH)