"""
This module contains a custom logger configuration that logs to CloudWatch and standard output.
"""

import json
import logging
import watchtower

from common.constants import LOG_GROUP_NAME

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

def configure_logger(name):
    """
    Configure a logger with a CloudWatch handler and a StreamHandler.

    :param name: The name of the logger.
    :return: The configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create a JSON log formatter
    formatter = JsonFormatter()

    # Create a StreamHandler for standard output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Try to create a CloudWatch handler
    try:
        cloudwatch_handler = watchtower.CloudWatchLogHandler(log_group=LOG_GROUP_NAME)
        cloudwatch_handler.setFormatter(formatter)
        logger.addHandler(cloudwatch_handler)
    except Exception as err:
        logger.error(f"Failed to connect to CloudWatch: {err}")

    return logger
