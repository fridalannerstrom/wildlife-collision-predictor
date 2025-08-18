import os
import sys
import pandas as pd
import pytest

# Add the 'app' directory to sys.path so we can import from src.*
APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app"))
if APP_PATH not in sys.path:
    sys.path.insert(0, APP_PATH)

# Import functions to test
from src.data_loader import load_clean_data


def test_load_clean_data_returns_dataframe():
    """
    Test that load_clean_data:
    1) Returns a pandas DataFrame
    2) Is not empty
    3) Contains a 'County' column (as expected in the cleaned dataset)
    """
    # Act
    df = load_clean_data()

    # Assert
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "County" in df.columns
