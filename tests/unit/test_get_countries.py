"""
This module contains tests for the get_countries lambda function.
"""

from lambda_functions.get_countries.app import handler

def test_handler():
    """
    Test the handler function.
    """
    # Mock event and context
    event = {}
    context = {}

    # Call the handler function
    response = handler(event, context)

    # Assert he expected output
    assert response == "Hello World!", "Unexpected output"
