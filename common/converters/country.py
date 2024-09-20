from common.models import Country

def dict_to_country(data: dict) -> Country:
    """
    Converts a dictionary to a Country object.

    :param data: A dictionary containing country data.
    :return: A Country object.
    """
    if data is None:
        raise ValueError("Data cannot be None")

    country_id = data.get('countryID', None)
    country_name = data.get('countryName', None)

    if country_id is None or country_name is None:
        raise ValueError("Data must contain 'countryID' and 'countryName' keys")

    country = Country(id=country_id, name=country_name)

    return country