import sys
import os
import pytest
import pandas as pd

# Add the "app" directory to the Python path so imports work when running pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

# Import the function we want to test
from src.data_loader import load_clean_data


def test_load_clean_data_returns_dataframe():
    """
    Test that load_clean_data:
    1) Returns a pandas DataFrame
    2) Is not empty
    3) Contains a 'County' column (as expected in the cleaned dataset)
    """
    # Act: Load the cleaned data
    df = load_clean_data()

    # Assert: The output should be a DataFrame
    assert isinstance(df, pd.DataFrame)

    # Assert: The DataFrame should not be empty
    assert not df.empty

    # Assert: It should contain the 'County' column
    assert "County" in df.columns
