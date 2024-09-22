"""
This module contains tests for the get_countries lambda function.
"""
import pytest

from lambda_functions.get_countries.app import handler
from common.models import Country

@pytest.mark.handler
@pytest.mark.parametrize("mock_response_data, expected_countries", [
    (
        {
            'data': [
                {'countryID': 1, 'countryName': 'United States'},
                {'countryID': 2, 'countryName': 'Narnia'}
            ]
        },
        [
            {'id': 1, 'name': 'United States'},
            {'id': 2, 'name': 'Narnia'}
        ]
    ),
    # Add more test cases here
])
def test_handler(mock_requests_get,
                 lambda_event_context,
                 mock_response_data,
                 expected_countries):
    """
    Test the handler function.
    """
    # Arrange
    event, context = lambda_event_context
    mock_requests_get(mock_response_data)

    # Act
    response = handler(event, context)

    # Assert the response is a list
    assert isinstance(response, list), "Response is not a list"

    # Assert the list contains at least one element
    assert len(response) == 2, "Response does not contain 2 elements"

    # Assert all elements in the list are of type Country
    assert all(isinstance(item, Country) for item in response), "Not all items are of type Country"

    # Assert the names and IDs of the countries are correct
    for i, expected_country in enumerate(expected_countries):
        assert response[i].id == expected_country['id'], "Incorrect country ID"
        assert response[i].name == expected_country['name'], "Incorrect country name"
