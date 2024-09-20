"""
Test the common.converters.country module.
"""
import pytest

from common.converters import dict_to_country
from common.models import Country

@pytest.mark.parametrize("data, expected", [
    ({'countryID': 1, 'countryName': 'Test Country'}, Country(id=1, name='Test Country')),
    ({'countryName': 'Test Country'}, pytest.raises(ValueError, match="Data must contain 'countryID' and 'countryName' keys")),
    ({'countryID': 1}, pytest.raises(ValueError, match="Data must contain 'countryID' and 'countryName' keys")),
    (None, pytest.raises(ValueError, match="Data cannot be None"))
])
def test_dict_to_country(data, expected):
    """
    Test the dict_to_country function.

    :param data: The data to convert.
    :param expected: The expected result.
    :return: None
    """
    if isinstance(expected, Country):
        country = dict_to_country(data)
        assert isinstance(country, Country)
        assert country.id == expected.id
        assert country.name == expected.name
    else:
        with expected:
            dict_to_country(data)
