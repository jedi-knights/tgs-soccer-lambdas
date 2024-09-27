"""
Lambda function to get countries
"""
import json
import http.client
import logging
import boto3
from botocore.exceptions import ClientError
from urllib.parse import urljoin, urlparse

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENDPOINT = 'https://public.totalglobalsports.com'
RESOURCE = '/api/Association/get-all-countries'

parsed_result = urlparse(urljoin(ENDPOINT, RESOURCE))
host = parsed_result.netloc
resource = parsed_result.path

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'countries'
table = dynamodb.Table(TABLE_NAME)

def create_dynamodb_table():
    """
    Create the DynamoDB table if it doesn't exist.
    """
    try:
        new_table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'country_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'country_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        new_table.wait_until_exists()
        logger.info("DynamoDB table created successfully")
    except ClientError as e:
        logger.error("Failed to create DynamoDB table: %s", e)
        raise

def handler(event, context):
    """
    This Lambda function retrieves a list of countries from the TGS API.

    :param event: Lambda event
    :param context: Lambda context
    """
    logger.info("Lambda event: %s", json.dumps(event))
    logger.info("Lambda context: %s", context)
    logger.info("Host: %s", host)
    logger.info("Resource: %s", resource)

    try:
        # Check if the DynamoDB table exists
        try:
            table.load()
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.info("DynamoDB table does not exist, creating table")
                create_dynamodb_table()
            else:
                raise

        # Check if there are any entries in the DynamoDB table
        response = table.scan(limit=1)
        if response['Count'] > 0:
            logger.info("Countries found in DynamoDB")
            return response['Items']

        logger.info("Countries not found in DynamoDB")
        logger.info("Retrieving countries from the TGS API")
        connection = http.client.HTTPSConnection(host)
        connection.request('GET', resource)
        response = connection.getresponse()

        if response.status != 200:
            raise http.client.HTTPException(f"Failed to retrieve countries: {response.status}")

        data = response.read()
        connection.close()
        json_data = json.loads(data)
        countries = json_data.get('data', [])

        # Save the countries to DynamoDB
        logger.info("Saving countries to DynamoDB")
        with table.batch_writer() as batch:
            for country in countries:
                batch.put_item(Item=country)
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
