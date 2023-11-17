"""
Module provides method to register all possible exceptions
"""

from flask import jsonify

from gistapi.exception_handlers.custom_exception import CustomException
from gistapi.exception_handlers.file_content_fetch_exception import (
    FileContentFetchException,
)
from gistapi.exception_handlers.invalid_input_exception import InvalidInputException
from gistapi.exception_handlers.user_not_found_exception import UserNotFoundException


def register_exception_handlers(app):
    """
    Register exception handlers for all the possible exceptions
    """

    @app.errorhandler(InvalidInputException)
    def invalid_input_error_handler(error):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(UserNotFoundException)
    def user_not_found_error_handler(error):
        return jsonify({"error": str(error)}), 404

    @app.errorhandler(FileContentFetchException)
    def file_content_fetch_error_handler(error):
        response = jsonify({"error": error.message})
        response.status_code = error.status_code
        return response

    @app.errorhandler(CustomException)
    def handle_custom_exception(error):
        response = jsonify({"error": error.message})
        response.status_code = error.status_code
        return response

    @app.errorhandler(Exception)
    def generic_exception_handler(error):
        # Log the error or take appropriate action
        return jsonify({"error": "An error occurred: " + str(error)}), 500
