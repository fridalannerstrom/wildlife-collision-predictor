import sys
import os
import pytest

# Add the "app" directory to the Python path so imports work when running pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

# Import the functions to test
from src.predictor import get_municipalities_for_county, load_unique_values


def test_get_municipalities_for_known_county():
    """
    Test that get_municipalities_for_county:
    1) Returns a list of municipalities for a valid county
    2) The list is not empty
    """
    # Arrange: Load unique values (counties, species, mapping)
    uv = load_unique_values()

    # Pick the first county from the list of available counties
    county = uv["counties"][0]

    # Act: Get municipalities for this county
    municipalities = get_municipalities_for_county(county)

    # Assert: The result should be a list
    assert isinstance(municipalities, list)

    # Assert: The list should contain at least one municipality
    assert len(municipalities) > 0
