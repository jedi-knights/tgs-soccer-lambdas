"""
This module contains utility functions common to multiple lambdas.
"""

import requests

from layers.common.logger import configure_logger

def fetch_data_from_api(url: str) -> dict:
    """
    Fetches data from the given API URL and return the JSON response.

    :param url: The URL of the API endpoint.
    :return: The JSON response.
    :raises: ValueError if the response is invalid or cannot be parsed
    """
    logger = configure_logger(__name__)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error occurred: %s", http_err)
        raise
    except requests.exceptions.RequestException as req_err:
        logger.error("An error occurred: %s", req_err)
        raise

    if response is None:
        logger.error("No response received")
        raise ValueError("No response received from the API")

    # Check if the response status code is not 200
    if response.status_code != 200:
        logger.error("Unexpected status code: %s", response.status_code)
        raise ValueError(f"Unexpected status code: {response.status_code}")

    # Parse the JSON response
    try:
        json_data = response.json()
    except requests.exceptions.JSONDecodeError as err:
        # JSON decoding failed.
        logger.error("Error decoding JSON data: %s", err)
        raise
    except ValueError as err:
        # The response body does not contain valid JSON.
        logger.error("Error parsing JSON data: %s", err)
        raise

    return json_data


def extract_data(json_data: dict) -> dict:
    """
    Extracts the 'data' property from the given JSON data.

    :param json_data: The JSON data.
    :return: The 'data' property.
    :raises: ValueError if the 'data' property is not found
    """
    if json_data is None:
        raise ValueError("JSON data cannot be None")

    data = json_data.get('data')

    if data is None:
        raise ValueError("No 'data' property found in JSON data")

    return data
