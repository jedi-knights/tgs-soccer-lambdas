import pytest

@pytest.fixture
def mock_requests_get(mocker):
    def _mock_requests_get(mock_response_data, status_code=200):
        mock_response = mocker.Mock()
        mock_response.json.return_value = mock_response_data
        mock_response.status_code = status_code
        mocker.patch('common.utils.requests.get', return_value=mock_response)
    return _mock_requests_get

@pytest.fixture
def lambda_event_context():
    event = {}
    context = {}
    return event, context

@pytest.fixture
def mock_configure_logger(mocker, test_logger):
    return mocker.patch('common.api.country.configure_logger', return_value=test_logger)
