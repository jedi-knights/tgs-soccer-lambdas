"""
Pytest configuration file for unit tests
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
        mocker.patch('common.utils.requests.get', return_value=mock_response)

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

@pytest.fixture
def _mock_configure_logger(mocker, test_logger):
    """
    Mock the configure_logger function

    :param mocker: Pytest mocker
    :param test_logger: Logger
    :return: Pytest mocker
    :raises: None
    """
    return mocker.patch('common.api.country.configure_logger', return_value=test_logger)
