"""
Lambda function to get organizations
"""
import json
import http.client
import logging
from urllib.parse import urljoin, urlparse

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENDPOINT = 'https://public.totalglobalsports.com'
RESOURCE = '/api/Association/get-current-orgs-list'

parsed_result = urlparse(urljoin(ENDPOINT, RESOURCE))
host = parsed_result.netloc
resource = parsed_result.path

def handler(event, context):
    """
    This Lambda function retrieves a list of organizations from the TGS API.

    :param event: Lambda event
    :param context: Lambda context
    """
    logger.info("Lambda event: %s", json.dumps(event))
    logger.info("Lambda context: %s", context)
    logger.info("Host: %s", host)
    logger.info("Resource: %s", resource)

    try:
        connection = http.client.HTTPSConnection(host)
        connection.request('GET', resource)
        response = connection.getresponse()

        if response.status != 200:
            raise http.client.HTTPException(f"Failed to retrieve organizations: {response.status}")

        data = response.read()
        connection.close()
        json_data = json.loads(data)
        organizations = json_data.get('data', [])
    except http.client.HTTPException as err:
        logger.error(err)
        raise
    except BaseException as err:
        logger.error("An unexpected error occurred: %s", err)
        raise

    return organizations

if __name__ == "__main__":
    result = handler({}, None)
    print(json.dumps(result, indent=4))
