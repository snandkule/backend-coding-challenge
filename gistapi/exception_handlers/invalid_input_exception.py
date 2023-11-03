"""
The Module contains all the possible classes to represent any invalid api input exceptions
"""


class InvalidInputException(Exception):
    """
    The exception class to represent any invalid api input exception
    """

    def __init__(self, message="Invalid input data"):
        """
        Initialises InvalidInputException object
        """
        self.message = message
        super().__init__(self.message)
