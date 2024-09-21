"""
This module contains a custom logger configuration that logs to CloudWatch and standard output.
"""

import json
import logging
import os

import watchtower

import boto3

from botocore.exceptions import ClientError
from botocore.exceptions import EndpointConnectionError
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import PartialCredentialsError
from botocore.exceptions import BotoCoreError

from common.constants import LOG_GROUP_NAME, DEFAULT_REGION


class JsonFormatter(logging.Formatter):
    """
    Custom log formatter that outputs log records as JSON.
    """
    def format(self, record):
        """
        Format a log record as JSON.

        :param record: The log record to format.
        :return: A JSON-formatted string.
        """
        log_record = {
            'timestamp': self.formatTime(record, self.datefmt),
            'name': record.name,
            'level': record.levelname,
            'message': record.getMessage(),
        }

        return json.dumps(log_record)

def create_log_group_if_not_exists(log_group_name: str,
                                   region_name: str = 'us-east-1',
                                   aws_access_key_id=None,
                                   aws_secret_access_key=None):
    """
    Create a CloudWatch log group if it does not already exist.

    :param log_group_name: The name of the log group to create.
    :param region_name: The AWS region in which to create the log group.
    :param aws_access_key_id: The AWS access key ID.
    :param aws_secret_access_key: The AWS secret access key.
    """
    client = boto3.client(
        'logs',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    try:
        # Check if the log group already exists
        response = client.describe_log_groups(logGroupNamePrefix=log_group_name)
        log_groups = response.get('logGroups', [])
        if any(log_group['logGroupName'] == log_group_name for log_group in log_groups):
            return

        # Create the log group if it does not exist
        client.create_log_group(logGroupName=log_group_name)
    except ClientError as e:
        print(f"Failed to create log group '{log_group_name}': {e}")

def configure_logger(name, region_name=None, aws_access_key_id=None, aws_secret_access_key=None):
    """
    Configure a logger with a CloudWatch handler and a StreamHandler.

    :param name: The name of the logger.
    :return: The configured logger.
    """

    if region_name is None:
        region_name = DEFAULT_REGION

    if aws_access_key_id is None:
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')

    if aws_secret_access_key is None:
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create a JSON log formatter
    formatter = JsonFormatter()

    # Create a StreamHandler for standard output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Ensure the log group exists
    create_log_group_if_not_exists(LOG_GROUP_NAME,
                                   region_name,
                                   aws_access_key_id,
                                   aws_secret_access_key)

    # Try to create a CloudWatch handler
    try:
        client = boto3.client(
            'logs',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        cloudwatch_handler = watchtower.CloudWatchLogHandler(
            log_group=LOG_GROUP_NAME,
            boto3_client=client
        )
        cloudwatch_handler.setFormatter(formatter)
        logger.addHandler(cloudwatch_handler)
    except ClientError as err:
        logger.error("Failed to connect to CloudWatch: %s", err)
    except EndpointConnectionError as err:
        logger.error("Failed to connect to CloudWatch: %s", err)
    except NoCredentialsError as err:
        logger.error("No AWS credentials found: %s", err)
    except PartialCredentialsError as err:
        logger.error("Partial AWS credentials found: %s", err)
    except BotoCoreError as err:
        logger.error("BotoCore error occurred: %s", err)

    return logger
