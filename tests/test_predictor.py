import os
import sys
import pandas as pd
import pytest

# Add the 'app' directory to sys.path so we can import from src.*
APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app"))
if APP_PATH not in sys.path:
    sys.path.insert(0, APP_PATH)

# Import functions to test
from src.predictor import (
    build_feature_row,
    predict_proba_label,
    load_model_columns,
)


def test_build_feature_row_has_expected_raw_columns():
    """Ensure build_feature_row returns exactly the raw fields"""
    X = build_feature_row(
        year=2025,
        month=8,
        hour=10,
        weekday="Monday",
        county="Värmlands län",
        species="Moose",
        municipality="Sunne",
        day_of_year=223,
    )

    expected_cols = {
        "Year", "Month", "Hour", "County", "Municipality",
        "Species", "Lat_WGS84", "Long_WGS84",
        "Day_of_Year", "Weekday"
    }

    assert isinstance(X, pd.DataFrame)
    assert set(X.columns) == expected_cols, (
        f"Got columns {list(X.columns)}"
    )


def test_model_columns_look_engineered():
    """
    Ensure that model_columns include engineered features
    with numeric and categorical prefixes.
    """
    model_cols = load_model_columns()
    assert isinstance(model_cols, list)
    assert len(model_cols) > 0

    # Check that at least one numeric and one categorical feature exist
    has_num = any(c.startswith("num_") for c in model_cols)
    has_cat = any(c.startswith("cat_") for c in model_cols)
    assert has_num, (
        "Expected at least one numeric feature starting with 'num_'"
    )
    assert has_cat, (
        "Expected at least one categorical feature starting with 'cat_'"
    )


def test_predict_proba_label_output_format():
    """
    Smoke test: The model should return a valid prediction
    in the expected format.
    """
    X = build_feature_row(
        year=2025,
        month=8,
        hour=6,
        weekday="Monday",
        county="Värmlands län",
        species="Moose",
        municipality="Sunne",
        day_of_year=223,
    )

    score, label, proba = predict_proba_label(X)

    # If the model supports predict_proba, ensure it returns a float
    if score is not None:
        assert isinstance(score, float)

    # If the model uses label prediction, ensure the label is one of the expected classes
    if label is not None:
        assert isinstance(label, str)
        assert label in [
            "Very High", "High", "Moderate", "Low", "Very Low"
        ]

    # If proba is returned, make sure it's a 2D array-like structure
    if proba is not None:
        assert hasattr(proba, "__getitem__")
        assert len(proba[0]) >= 1
