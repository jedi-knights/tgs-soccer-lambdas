"""
Test the common.converters.organization module.
"""
import pytest

from layer.python.common.converters import dict_to_organization
from layer.python.common.models import Organization
from layer.python.common.exceptions import DataValidationError

@pytest.mark.parametrize("data, expected", [
    (
            {},
            pytest.raises(DataValidationError, match="Data must contain 'orgID' key")
    ),
    (
            {'orgID': 1},
            pytest.raises(DataValidationError, match="Data must contain 'orgName' key")
    ),
    (
            {'orgID': 1, 'orgName': 'Test Organization'},
            pytest.raises(DataValidationError, match="Data must contain 'orgSeasonID' key")
    ),
    (
            {'orgID': 1, 'orgName': 'Test Organization', 'orgSeasonID': 1},
            pytest.raises(DataValidationError, match="Data must contain 'orgSeasonGroupID' key")
    ),
    (
            {'orgID': 1, 'orgName': 'Test Organization', 'orgSeasonID': 2, 'orgSeasonGroupID': 3},
            Organization(id=1, name='Test Organization', season_id=2, season_group_id=3)
    ),
    (
            {
                'orgID': '1',
                'orgName': 'Test Organization',
                'orgSeasonID': '2',
                'orgSeasonGroupID': '3'
            },
            Organization(id=1, name='Test Organization', season_id=2, season_group_id=3)
    ),
    (
            None,
            pytest.raises(DataValidationError, match="Data cannot be None")
    )
])
def test_dict_to_organization(data, expected):
    """
    Test the dict_to_organization function.

    :param data: The data to convert.
    :param expected: The expected result.
    :return: None
    """
    if isinstance(expected, Organization):
        organization = dict_to_organization(data)
        assert isinstance(organization, Organization)
    else:
        with expected:
            dict_to_organization(data)
