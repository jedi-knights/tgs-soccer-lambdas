"""
This module contains utility lambda_functions used by lambda lambda_functions.
"""
from urllib.parse import urljoin
from typing import Optional

import requests

from common.constants import ENDPOINT
from common.logger import configure_logger
from common.models import Country
from lambda_functions.get_countries.app import dict_to_country

logger = configure_logger(__name__)



def get_countries():
    resource = '/api/Association/get-all-countries'
    url = urljoin(ENDPOINT, resource)
    response = None

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return

    if response is None:
        logger.error("No response received")
        return

    # Check if the response status code is not 200
    if response.status_code != 200:
        logger.error(f"Unexpected status code: {response.status_code}")
        return

    # Parse the JSON response
    try:
        json_data = response.json()
    except ValueError as err:
        # The response body does not contain valid JSON.
        logger.error(f"Error parsing JSON data: {err}")
        return
    except requests.exceptions.JSONDecodeError as err:
        # JSON decoding failed.
        logger.error(f"Error decoding JSON data: {err}")
        return

    selected_countries = []
    data = json_data.get('data', None)

    if data is None:
        logger.error("No data property found in response")
        return

    for item in data:
        country = dict_to_country(item)
        selected_countries.append(country)

    return selected_countries
