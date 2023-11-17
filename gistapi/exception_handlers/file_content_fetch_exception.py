"""
Module provides all the possible exceptions to raise while file operations
"""


class FileContentFetchException(Exception):
    """
    File containing exception to raise while facing any issue during file content fetch operation
    """

    def __init__(self, message, status_code=500):
        """
        Initialises FileContentFetchException object
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
