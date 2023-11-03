"""
This module defines fixtures and configuration settings for pytest testing.
The 'client' fixture is provided to simulate interactions with the Flask app during testing.
The Flask app instance is imported from the 'gistapi' module to provide a context for testing.
"""

import pytest
from gistapi.gistapi import app  # Import your Flask app


@pytest.fixture
def test_client():
    """
    The 'client' fixture is provided for interactions with the Flask app during testing
    """
    with app.test_client() as client:
        yield client
