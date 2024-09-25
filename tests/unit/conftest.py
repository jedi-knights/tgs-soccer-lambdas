"""
Pytest configuration file for unit events
"""

import pytest

@pytest.fixture
def mock_requests_get(mocker):
    """
    Mock the requests.get function

    :param mocker: Pytest mocker
    :return: Function
    :raises: None
    """
    def _mock_requests_get(mock_response_data, status_code=200):
        mock_response = mocker.Mock()
        mock_response.json.return_value = mock_response_data
        mock_response.status_code = status_code
        mocker.patch('layers.common.utils.requests.get', return_value=mock_response)

    return _mock_requests_get

@pytest.fixture
def lambda_event_context():
    """
    Create a mock Lambda event and context

    :return: Tuple containing the event and context
    :raises: None
    """
    event = {}
    context = {}
    return event, context
