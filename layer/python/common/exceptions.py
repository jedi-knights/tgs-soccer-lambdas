"""
This module contains common exceptions used in the application.
"""

class DataValidationError(Exception):
    """Exception raised for errors in the input data."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
