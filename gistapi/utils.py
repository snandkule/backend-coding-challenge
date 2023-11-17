"""
The utility class provides common methods to perform operations like
search for regular expression in gist files, gist description and file contents
"""

import re
import requests

from gistapi.exception_handlers.file_content_fetch_exception import (
    FileContentFetchException,
)


def fetch_and_search(raw_url: str, pattern: str, file_name: str, gist_id):
    """Provides whether pattern is present in file content or not.

    Pulls down a file content for a given raw file url and then searches
    for a given regular expression in file content.

    Returns:
        the boolean result which provides whether pattern is present in file content or not
    """
    if re.search(pattern, file_name):
        return True
    try:
        response = requests.get(raw_url, stream=True, timeout=10)
        response.raise_for_status()
        gist_prev_chunk = ""
        for chunk in response.iter_content(chunk_size=max(len(pattern), 1024)):
            if chunk:
                # Convert the binary chunk to a string (assuming UTF-8 encoding)
                gist_content_chunk = chunk.decode("utf-8")
                if re.search(pattern, gist_prev_chunk + gist_content_chunk):
                    return True
                gist_prev_chunk = gist_content_chunk

    except requests.exceptions.RequestException as e:
        raise FileContentFetchException(
            f"Failed to fetch content for file '{file_name}' "
            f"in Gist '{gist_id}':{str(e)}"
        )
    return False


def search_in_description(description, pattern):
    """Search for a pattern in the description of a gist.

    Args:
        description (str): The description of gist.
        pattern (str): The regular expression pattern to search for.

    Returns:
        bool: True if the pattern is found in the description, False otherwise.
    """
    if re.search(pattern, description):
        return True
    return False


def search_in_gist_files(gist, pattern):
    """
    Search for a pattern in the files of a Gist and return success response if found.

    This function iterates through the files of a Gist, checks if the pattern exists in the
    file content or file name. If the pattern is found, returns the
    success response

    Parameters:
        gist (dict): The Gist to search within.
        pattern (str): The regular expression pattern to search for.

    Returns:
        the boolean result which provides whether pattern is present in files or not
    """

    files = gist.get("files", {})

    for file_name, file_info in files.items():
        file_content = file_info.get("content", "")
        search_response = None

        # If file content is not present in file info, fetch it using the raw URL
        if "content" not in file_info:
            search_response = fetch_and_search(
                file_info.get("raw_url", None), pattern, file_name, gist["id"]
            )

        # Check if the pattern exists in the file content or file name
        if (
            re.search(pattern, file_content)
            or search_response
            or re.search(pattern, file_name)
        ):
            return True
    return False
