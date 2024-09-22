"""
Lambda function to get organizations
"""

from layer.python.common.logger import configure_logger

logger = configure_logger(__name__)


def handler(event, context):
    """
    Lambda handler function

    :param event: Lambda event
    :param context: Lambda context
    """
    logger.info("Lambda event: %s", event)
    logger.info("Lambda context: %s", context)
    return "Hello World!"
