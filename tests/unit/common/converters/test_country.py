"""
Test the common.converters.country module.
"""
import pytest

from common.converters import dict_to_country
from common.exceptions import DataValidationError
from common.models import Country

@pytest.mark.parametrize("data, expected", [
    (
            None,
            pytest.raises(DataValidationError, match="Data cannot be None")
    ),
    (
            {},
            pytest.raises(DataValidationError, match="Data must contain 'countryID' key")
    ),
    (
            {'countryID': 1},
            pytest.raises(DataValidationError, match="Data must contain 'countryName' key")
    ),
    (
            {'countryID': 1, 'countryName': 'Test Country'},
            Country(id=1, name='Test Country')
    ),
    (
            {'countryID': '1', 'countryName': 'Test Country'},
            Country(id=1, name='Test Country')
    ),
    (
            {'countryID': 2, 'countryName': '    Test Country'},
            Country(id=2, name='Test Country')
    ),
    (
            {'countryID': ' 7 ', 'countryName': 'Test Country    '},
            Country(id=7, name='Test Country')
    ),
    (
            {'countryID': 13, 'countryName': '  Test Country   '},
            Country(id=13, name='Test Country')
    ),
    (
            {'countryID': 'bad', 'countryName': 'Test Country'},
            pytest.raises(DataValidationError, match="Country validation failed")
    ),
    (
            {'countryID': '1', 'countryName': ''},
            pytest.raises(DataValidationError, match="Data must contain a non-empty 'countryName'")
    ),
    (
            {'countryID': '1', 'countryName': '      '},
            pytest.raises(DataValidationError, match="Data must contain a non-empty 'countryName'")
    ),
    (
            {'countryName': 'Test Country'},
            pytest.raises(DataValidationError, match="Data must contain 'countryID' key")
    )
])
def test_dict_to_country(data, expected, _mock_configure_logger):
    """
    Test the dict_to_country function.

    :param data: The data to convert.
    :param expected: The expected result.
    :param _mock_configure_logger: Mocked configure_logger function
    """
    if isinstance(expected, Country):
        country = dict_to_country(data)
        assert isinstance(country, Country)
        assert country.id == expected.id
        assert country.name == expected.name
    else:
        with expected:
            dict_to_country(data)
