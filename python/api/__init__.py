"""
This module is used to implement the request processing for the TGS API.
"""

from .country import get_countries
from .organization import get_organizations

__all__ = ['get_countries', 'get_organizations']
