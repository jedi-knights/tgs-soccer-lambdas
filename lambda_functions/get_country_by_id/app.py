"""
Lambda function to get a country by ID and call another Lambda to get organizations
"""
import json
import http.client
import logging
import boto3
from urllib.parse import urljoin, urlparse

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENDPOINT = 'https://public.totalglobalsports.com'
RESOURCE = '/api/Association/get-country-by-id/{}'

# Initialize Boto3 client for Lambda
lambda_client = boto3.client('lambda')

def handler(event, context):
    """
    This Lambda function retrieves a country by ID from the TGS API and calls another Lambda to get organizations.

    :param event: Lambda event
    :param context: Lambda context
    """
    logger.info("Lambda event: %s", json.dumps(event))
    logger.info("Lambda context: %s", context)

    country_id = event.get('country_id')
    if not country_id:
        logger.error("Country ID is required")
        raise ValueError("Country ID is required")

    resource = RESOURCE.format(country_id)
    parsed_result = urlparse(urljoin(ENDPOINT, resource))
    host = parsed_result.netloc
    resource_path = parsed_result.path

    logger.info("Host: %s", host)
    logger.info("Resource: %s", resource_path)

    try:
        connection = http.client.HTTPSConnection(host)
        connection.request('GET', resource_path)
        response = connection.getresponse()

        if response.status != 200:
            raise http.client.HTTPException(f"Failed to retrieve country: {response.status}")

        data = response.read()
        connection.close()
        json_data = json.loads(data)
        country = json_data.get('data', {})

        # Call the get_organizations Lambda function
        response = lambda_client.invoke(
            FunctionName='get_organizations',
            InvocationType='RequestResponse',
            Payload=json.dumps({})
        )

        response_payload = json.loads(response['Payload'].read())
        organizations = response_payload.get('data', [])

    except http.client.HTTPException as err:
        logger.error(err)
        raise
    except BaseException as err:
        logger.error("An unexpected error occurred: %s", err)
        raise

    return {
        'country': country,
        'organizations': organizations
    }

if __name__ == "__main__":
    test_event = {'country_id': '123'}
    result = handler(test_event, None)
    print(json.dumps(result, indent=4))