"""
This module contains functions to interact with the TGS API to retrieve organizations.
"""

from urllib.parse import urljoin
from common.constants import ENDPOINT
from common.logger import configure_logger
from common.models import Organization
from common.converters import dict_to_organization
from common.utils import fetch_data_from_api, extract_data

logger = configure_logger(__name__)

def get_organizations() -> list[Organization]:
    """
    Retrieves a list of organizations from the TGS API.
    """
    resource = '/api/Association/get-current-orgs-list'
    url = urljoin(ENDPOINT, resource)

    json_data = fetch_data_from_api(url)
    data = extract_data(json_data)

    selected_organizations = []
    for item in data:
        current_organization = dict_to_organization(item)
        selected_organizations.append(current_organization)

    return selected_organizations

if __name__ == '__main__':
    organizations = get_organizations()
    if organizations:
        for organization in organizations:
            print(organization)
    else:
        print("No organizations found")
