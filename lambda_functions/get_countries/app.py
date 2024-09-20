from common import utils
from common.models import Country

def dict_to_country(data: dict) -> Country:
    """
    Converts a dictionary to a Country object.

    :param data: A dictionary containing country data.
    :return: A Country object.
    """
    return Country(**data)


def handler(event, context):
    return "Hello World!"
