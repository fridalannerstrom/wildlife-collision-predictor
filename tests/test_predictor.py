# tests/test_predictor.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from src.predictor import build_feature_row, load_model_columns

def test_build_feature_row_shape():
    # Build input row for a known case
    X = build_feature_row(
        year=2025,
        month=8,
        hour=14,
        weekday="Monday",
        county="Värmlands län",
        species="Moose",
        municipality="Sunne",
        day_of_year=223
    )

    model_cols = load_model_columns()
    
    # Assert that output matches the model's expected input shape
    assert X.shape[1] == len(model_cols)
    assert list(X.columns) == model_cols