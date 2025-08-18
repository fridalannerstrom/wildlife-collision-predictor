"""
Train and export the ML model pipeline to predict wildlife collision risk.
"""

import pandas as pd
import numpy as np
import os
import lzma
import cloudpickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# ------------------------------
# Constants
# ------------------------------

DATA_PATH = "data/cleaned_data.csv"
MODEL_PATH = "model/model.pkl.xz"
COLUMNS_PATH = "model/model_columns.pkl"
TARGET = "Collision_Risk"

# ------------------------------
# Load and prepare data
# ------------------------------

df = pd.read_csv(DATA_PATH, encoding="utf-8")

# Parse time columns
df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
if "Hour" not in df.columns:
    df["Hour"] = df["Time"].dt.hour

# Drop rows with missing values
df.dropna(subset=["Species", "County", "Municipality", "Hour"], inplace=True)

# Create target if missing
if TARGET not in df.columns:
    df[TARGET] = df["Collision_ID"].notna().astype(int)

# ------------------------------
# Select features
# ------------------------------

FEATURES = [
    "Species", "County", "Municipality", "Hour",
    "Month", "Year", "Day_of_Year", "Weekday",
    "Lat_WGS84", "Long_WGS84"
]
X = df[FEATURES]
y = df[TARGET]

# ------------------------------
# Preprocessing pipeline
# ------------------------------

categorical = ["Species", "County", "Municipality", "Weekday"]
numeric = ["Hour", "Month", "Year", "Day_of_Year", "Lat_WGS84", "Long_WGS84"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", "passthrough", numeric)
    ]
)

# Combine preprocessor + model
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight="balanced"
    ))
])

# ------------------------------
# Train pipeline
# ------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

pipeline.fit(X_train, y_train)
accuracy = pipeline.score(X_test, y_test)
print(f"✅ Model trained, accuracy: {accuracy:.2%}")

# ------------------------------
# Save pipeline
# ------------------------------

os.makedirs("model", exist_ok=True)

with lzma.open(MODEL_PATH, "wb") as f:
    cloudpickle.dump(pipeline, f)
print(f"💾 Model saved to {MODEL_PATH}")

with open(COLUMNS_PATH, "wb") as f:
    cloudpickle.dump(X.columns.tolist(), f)
print(f"📄 Model columns saved to {COLUMNS_PATH}")