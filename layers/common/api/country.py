"""
This module contains functions that access the TGS API to retrieve countries.
"""

from urllib.parse import urljoin
from constants import ENDPOINT
from exceptions import DataValidationError
from logger import configure_logger
from models import Country
from converters import dict_to_country
from utils import fetch_data_from_api, extract_data

logger = configure_logger(__name__)

def get_countries() -> list[Country]:
    """
    Retrieves a list of countries from the TGS API.
    """
    resource = '/api/Association/get-all-countries'
    url = urljoin(ENDPOINT, resource)

    json_data = fetch_data_from_api(url)
    data = extract_data(json_data)

    selected_countries = []
    for item in data:
        try:
            current_country = dict_to_country(item)
            selected_countries.append(current_country)
        except DataValidationError as err:
            logger.error("Error converting data to Country: %s", err)
            raise

    return selected_countries

if __name__ == "__main__":
    countries = get_countries()
    if countries is not None:
        for country in countries:
            logger.info("Country: %s", country.name)
    else:
        logger.error("Failed to retrieve countries")
