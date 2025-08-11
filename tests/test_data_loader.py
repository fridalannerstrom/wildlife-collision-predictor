import sys
import os
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from src.data_loader import load_clean_data


def test_load_clean_data_returns_dataframe():
    df = load_clean_data()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "County" in df.columns