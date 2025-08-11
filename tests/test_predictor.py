import sys
import pandas as pd
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

import pytest
from src.predictor import build_feature_row, predict_proba_label, load_model_columns

def test_build_feature_row_has_all_model_columns():
    # Arrange
    X = build_feature_row(
        year=2025,
        month=8,
        hour=10,
        weekday="Monday",
        county="Värmlands län",
        species="Moose",
        municipality="Sunne",
        day_of_year=223
    )

    model_cols = load_model_columns()

    # Assert
    assert isinstance(X, pd.DataFrame)
    assert list(X.columns) == model_cols
    assert X.shape[1] == len(model_cols)

def test_predict_proba_label_output_format():
    # Arrange
    X = build_feature_row(
        year=2025,
        month=8,
        hour=6,
        weekday="Monday",
        county="Värmlands län",
        species="Moose",
        municipality="Sunne",
        day_of_year=223
    )

    # Act
    score, label, proba = predict_proba_label(X)

    # Assert
    assert isinstance(score, float)
    assert label in ["High", "Medium", "Low"]
    assert proba is not None
    assert len(proba[0]) >= 2  # för binär/multiklassmodell