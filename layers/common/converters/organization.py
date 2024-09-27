"""
This module contains functions for converting data to and from Organization objects.
"""

from models import Organization
from exceptions import DataValidationError

def dict_to_organization(data: dict) -> Organization:
    """
    Convert a dictionary to an Organization object

    :param data: Dictionary
    :return: Organization
    """
    if data is None:
        raise DataValidationError("Data cannot be None")

    org_id = data.get('orgID', None)

    if org_id is None:
        raise DataValidationError("Data must contain 'orgID' key")

    org_name = data.get('orgName', None)

    if org_name is None:
        raise DataValidationError("Data must contain 'orgName' key")

    org_season_id = data.get('orgSeasonID', None)

    if org_season_id is None:
        raise DataValidationError("Data must contain 'orgSeasonID' key")

    org_season_group_id = data.get('orgSeasonGroupID', None)

    if org_season_group_id is None:
        raise DataValidationError("Data must contain 'orgSeasonGroupID' key")

    try:
        organization = Organization(
            id=org_id,
            name=org_name,
            season_id=org_season_id,
            season_group_id=org_season_group_id
        )
    except ValueError as exc:
        raise DataValidationError("Organization validation failed") from exc

    return organization
