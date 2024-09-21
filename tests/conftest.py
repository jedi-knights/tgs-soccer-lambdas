"""
This file contains fixtures and hooks that are used by pytest to setup the test environment.
"""

# tests/conftest.py
import logging
import pytest

@pytest.fixture
def test_logger():
    """
    Create a logger for testing
    """
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
