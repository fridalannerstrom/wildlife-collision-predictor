import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from src.predictor import get_municipalities_for_county, load_unique_values


def test_get_municipalities_for_known_county():
    uv = load_unique_values()
    county = uv["counties"][0]

    municipalities = get_municipalities_for_county(county)

    assert isinstance(municipalities, list)
    assert len(municipalities) > 0