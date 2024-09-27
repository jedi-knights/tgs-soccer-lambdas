"""
This module contains the Organization model.
"""

from pydantic import BaseModel

class Organization(BaseModel):
    """
    Represents an organization.
    """
    id: int
    name: str
    season_id: int
    season_group_id: int
