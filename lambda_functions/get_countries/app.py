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

ENDPOINT = 'https://public.totalglobalsports.com'
RESOURCE = '/api/Association/get-all-countries'

parsed_result = urlparse(urljoin(ENDPOINT, RESOURCE))
host = parsed_result.netloc
url = parsed_result.path

def handler(event, context):
    """
    This Lambda function retrieves a list of countries from the TGS API.

    :param event: Lambda event
    :param context: Lambda context
    """
    logger.info("Lambda event: %s", json.dumps(event))
    logger.info("Lambda context: %s", context)
    logger.info("Host: %s", host)
    logger.info("URL: %s", url)

    try:
        connection = http.client.HTTPSConnection(host)
        connection.request('GET', url)
        response = connection.getresponse()

        if response.status != 200:
            raise http.client.HTTPException(f"Failed to retrieve countries: {response.status}")

        data = response.read()
        connection.close()
        json_data = json.loads(data)
        countries = json_data.get('data', [])
    except http.client.HTTPException as err:
        logger.error(err)
        raise
    except BaseException as err:
        logger.error("An unexpected error occurred: %s", err)
        raise

    return countries


if __name__ == "__main__":
    result = handler({}, None)
    print(json.dumps(result, indent=4))
