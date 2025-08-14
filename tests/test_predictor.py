import sys
import os
import pandas as pd

from app.src.predictor import (
    build_feature_row,
    predict_proba_label,
    load_model_columns,
)

app_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "app")
)
sys.path.insert(0, app_path)


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
    Ensure model_columns represent engineered features with numeric
    and categorical prefixes.
    """
    model_cols = load_model_columns()
    assert isinstance(model_cols, list)
    assert len(model_cols) > 0

    # At least one numeric and one categorical feature should exist
    has_num = any(c.startswith("num_") for c in model_cols)
    has_cat = any(c.startswith("cat_") for c in model_cols)
    assert has_num, (
        "Expected at least one engineered numeric feature starting with 'num_'"
    )
    assert has_cat, (
        "Expected at least one categorical feature starting with 'cat_'"
    )


def test_predict_proba_label_output_format():
    """
    Smoke test: model should be able to make a prediction and
    return the expected format.
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

    # Predictor can return score (float) + proba or label (str)
    # if model lacks predict_proba
    if score is not None:
        assert isinstance(score, float)

    if label is not None:
        assert isinstance(label, str)
        assert label in [
            "Very High", "High", "Moderate", "Low", "Very Low"
        ]

    # proba can be None or a 2D array-like structure
    if proba is not None:
        assert hasattr(proba, "__getitem__")
        assert len(proba[0]) >= 1
