"""
This module contains the Country model.
"""

from pydantic import BaseModel

class Country(BaseModel):
    """
    Represents a country.
    """
    id: int
    name: str
