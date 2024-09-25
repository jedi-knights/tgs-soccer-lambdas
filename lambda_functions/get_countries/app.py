"""
Lambda function to get countries
"""

from layers.common.logger import configure_logger
from layers.common.api import get_countries

logger = configure_logger(__name__)

def handler(event, context):
    """
    Lambda handler function

    :param event: Lambda event
    :param context: Lambda context
    """
    logger.info("Lambda event: %s", event)
    logger.info("Lambda context: %s", context)
    countries = get_countries()

    return countries
