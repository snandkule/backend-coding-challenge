"""
The Module contains all the possible classes to represent user data related exceptions
"""


class UserNotFoundException(Exception):
    """
    The exception class represents user not found exception
    """

    def __init__(self, message="User not found"):
        """
        initialises UserNotFoundException object
        """
        self.message = message
        super().__init__(self.message)
