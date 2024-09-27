"""
Lambda function to get countries
"""
import json
import http.client
import logging
from urllib.parse import urljoin, urlparse

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class CountryRetrievalError(Exception):
    """Exception raised when failing to retrieve countries from the API."""
    def __init__(self, status_code, message="Failed to retrieve countries"):
        self.status_code = status_code
        self.message = f"{message}: {status_code}"
        super().__init__(self.message)

def handler(event, context):
    """
    Lambda handler function

    :param event: Lambda event
    :param context: Lambda context
    """
    logger.info("Lambda event: %s", json.dumps(event))
    logger.info("Lambda context: %s", context)

    endpoint = 'https://public.totalglobalsports.com'
    resource = '/api/Association/get-all-countries'
    url = urlparse(urljoin(endpoint, resource))

    try:
        connection = http.client.HTTPSConnection(url.netloc)
        connection.request('GET', url.path)
        response = connection.getresponse()

        if response.status != 200:
            raise CountryRetrievalError(response.status)

        data = response.read()
        connection.close()
        json_data = json.loads(data)
    except CountryRetrievalError as err:
        logger.error("Failed to retrieve countries: %s", err)
        raise
    except BaseException as err:
        logger.error("An unexpected error occurred: %s", err)
        raise

    return json_data


if __name__ == "__main__":
    handler({}, None)
