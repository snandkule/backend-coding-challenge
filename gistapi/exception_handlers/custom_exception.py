"""
Module provides a custom exception to raise with requirement specific error message and status code
"""


class CustomException(Exception):
    """
    Custom exception to raise with requirement specific error message and status code
    """

    def __init__(self, message, status_code=500):
        """
        Initialises CustomException object
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
