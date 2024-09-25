"""
This module contains functions for converting data to and from Country objects.
"""

from pydantic import ValidationError

from layers.common.models import Country
from layers.common.exceptions import DataValidationError

def dict_to_country(data: dict) -> Country:
    """
    Converts a dictionary to a Country object.

    :param data: A dictionary containing country data.
    :return: A Country object.
    """
    if data is None:
        raise DataValidationError("Data cannot be None")

    country_id = data.get('countryID', None)

    if country_id is None:
        raise DataValidationError("Data must contain 'countryID' key")

    country_name = data.get('countryName', None)

    if country_name is None:
        raise DataValidationError("Data must contain 'countryName' key")

    country_name = str(country_name)
    country_name = country_name.strip()

    if len(country_name) == 0:
        raise DataValidationError("Data must contain a non-empty 'countryName'")

    try:
        country = Country(id=country_id, name=country_name)
    except ValidationError as exc:
        raise DataValidationError("Country validation failed") from exc

    return country
