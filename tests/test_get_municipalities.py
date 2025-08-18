import os
import sys
import pytest

# Add the 'app' directory to sys.path so we can import from src.*
APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app"))
if APP_PATH not in sys.path:
    sys.path.insert(0, APP_PATH)

# Import functions to test
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
