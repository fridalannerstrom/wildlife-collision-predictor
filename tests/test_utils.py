import sys
import os
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from src.utils import read_csv_latin1


def test_read_csv_latin1_reads_file():
    sample_path = os.path.join("data", "cleaned_data.csv")
    df = read_csv_latin1(sample_path)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "Species" in df.columns