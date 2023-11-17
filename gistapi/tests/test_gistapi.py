"""
This module contains testcases for various scenarios to test search gist API"""

import json


def test_search_gists_found(test_client):
    """
    The testcases tests success scenario with valid input
    """
    data = {"username": "justdionysus", "pattern": "import requests"}
    response = test_client.post("/api/v1/search?page=1&page_size=10", json=data)
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert data["pattern"] == "import requests"
    assert data["status"] == "success"
    assert data["username"] == "justdionysus"
    expected_fields = [
        {
            "description": "",
            "html_url": "https://gist.github.com/justdionysus/65e6162d99c2e2ea8049b0584dd00912",
            "owner": {
                "id": 2153161,
                "login": "justdionysus",
            },
        }
    ]
    for i, expected_match in enumerate(expected_fields):
        assert data["matches"][i]["description"] == expected_match["description"]
        assert data["matches"][i]["html_url"] == expected_match["html_url"]
        assert data["matches"][i]["owner"]["id"] == expected_match["owner"]["id"]
        assert data["matches"][i]["owner"]["login"] == expected_match["owner"]["login"]


def test_search_gists_found_with_different_content(test_client):
    """
    The testcases tests success scenario with valid input and different type of gist content
    """
    data = {"username": "snandkule", "pattern": "Shailesh"}
    response = test_client.post("/api/v1/search?page=1&page_size=10", json=data)
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert data["pattern"] == "Shailesh"
    assert data["status"] == "success"
    assert data["username"] == "snandkule"
    expected_fields = [
        {
            "description": "",
            "html_url": "https://gist.github.com/snandkule/ef66fd03cf85beb8e5f84545544d8a0b",
            "owner": {
                "login": "snandkule",
            },
        }
    ]
    for i, expected_match in enumerate(expected_fields):
        assert data["matches"][i]["description"] == expected_match["description"]
        assert data["matches"][i]["html_url"] == expected_match["html_url"]
        assert data["matches"][i]["owner"]["login"] == expected_match["owner"]["login"]


def test_search_gists_with_empty_username(test_client):
    """
    The testcases tests error scenario with empty username
    """
    data = {"username": "", "pattern": "import requests"}
    response = test_client.post("/api/v1/search", json=data)
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 400
    assert data == {"error": "Both 'username' and 'pattern' parameters are required."}


def test_search_gists_with_empty_pattern(test_client):
    """
    The testcases tests error scenario with empty pattern
    """
    data = {"username": "xyz", "pattern": ""}
    response = test_client.post("/api/v1/search", json=data)
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 400
    assert data == {"error": "Both 'username' and 'pattern' parameters are required."}


def test_search_gists_not_found(test_client):
    """
    The testcases tests error scenario with non-existing username
    """
    data = {"username": "nonexistentuser", "pattern": "import requests"}
    response = test_client.post("/api/v1/search", json=data)
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 404
    assert data == {"error": "User not found, Kindly provide correct username"}


def test_search_gists_invalid_page_number(test_client):
    """
    The testcases tests error scenario with invalid page number
    """
    data = {"username": "justdionysus", "pattern": "import requests"}
    response = test_client.post("/api/v1/search?page=0&page_size=10", json=data)
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 400
    assert data == {"error": "'page' should be more than 0"}


def test_search_gists_invalid_page_size(test_client):
    """
    The testcases tests error scenario with invalid page number
    """
    data = {"username": "justdionysus", "pattern": "import requests"}
    response = test_client.post("/api/v1/search?page=1&page_size=0", json=data)
    data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 400
    assert data == {"error": "'page_size' should be greater than 0 and less than 101"}
