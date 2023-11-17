"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

import requests
from flask import Flask, jsonify, request

from gistapi.exception_handlers.custom_exception import CustomException
from gistapi.exception_handlers.exception_handlers import register_exception_handlers
from gistapi.exception_handlers.invalid_input_exception import InvalidInputException
from gistapi.exception_handlers.user_not_found_exception import UserNotFoundException
from gistapi.utils import search_in_description, search_in_gist_files

app = Flask(__name__)

register_exception_handlers(app)


@app.route("/ping")
def ping():
    """Provide a static response to a simple GET request."""
    return "This is static response"


def gists_for_user(username: str):
    """Provides the list of gist metadata for a given user.

    This abstracts the /users/:username/gist endpoint from the GitHub API.
    See https://developer.github.com/v3/gists/#list-a-users-gists for
    more information.

    Args:
        username (string): the user to query gists for

    Returns:
        The dict parsed from the json response from the GitHub API.  See
        the above URL for details of the expected structure.
    """
    if not username:
        raise InvalidInputException("Username is required")

    gists_url = f"https://api.github.com/users/{username}/gists"

    try:
        response = requests.get(gists_url, timeout=10)
        if response.status_code == 200:
            # Successful response
            return response.json()
        if response.status_code == 404:
            raise UserNotFoundException(
                "User not found, Kindly provide correct username"
            )
        raise CustomException(
            f"Failed to fetch gist for {username}", response.status_code
        )
    except UserNotFoundException as e:
        raise e
    except requests.exceptions.RequestException as e:
        raise CustomException(
            f"Failed to fetch gist for {username}. " f"Got exception {str(e)}"
        )
    except CustomException as e:
        raise e


@app.route("/api/v1/search", methods=["POST"])
def search():
    """Provides matches for a single pattern across a single users gists.

    Pulls down a list of all gists for a given user and then searches
    each gist for a given regular expression.

    Returns:
        A Flask Response object of type application/json.  The result
        object contains the list of matches along with a 'status' key
        indicating any failure conditions.
    """
    post_data = request.get_json()
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 5))
    username = post_data["username"]
    pattern = post_data["pattern"]

    if not username or not pattern:
        raise InvalidInputException(
            "Both 'username' and 'pattern' parameters are required."
        )

    if page < 1:
        raise InvalidInputException("'page' should be more than 0")

    if page_size < 1 or page_size > 100:
        raise InvalidInputException(
            "'page_size' should be greater than 0 and less than 101"
        )

    result = {}
    gists = gists_for_user(username)

    matching_gists = []

    for gist in gists:
        # For each gist, checking for the pattern in description, file content and file name
        if search_in_description(gist.get("description", ""), pattern):
            matching_gists.append(gist)
            continue

        found_in_files = search_in_gist_files(gist, pattern)

        if found_in_files:
            matching_gists.append(gist)

    start_id = (page - 1) * page_size
    end_id = min(start_id + page_size, len(matching_gists))
    result["status"] = "success"
    result["username"] = username
    result["pattern"] = pattern
    result["matches"] = matching_gists[start_id:end_id]
    result["page"] = page
    result["count"] = len(result["matches"])
    result["page_size"] = page_size
    result["total_count"] = len(matching_gists)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9876)
