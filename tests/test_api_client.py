import pytest
from src.api_client import BetfairAPIClient
from unittest.mock import patch
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

@pytest.fixture
def client() -> BetfairAPIClient:
    return BetfairAPIClient(app_key="test_app_key", session_token="test_session_token")

@patch('src.api_client.requests.Session.post')
def test_make_request_success(mock_post, client: BetfairAPIClient):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"result": "success"}
    response = client.make_request("test_endpoint", {"param": "value"})
    assert response == {"result": "success"}

@patch('src.api_client.requests.Session.post')
def test_make_request_http_error(mock_post, client: BetfairAPIClient):
    mock_post.side_effect = HTTPError("HTTP error")
    response = client.make_request("test_endpoint", {"param": "value"})
    assert response is None

@patch('src.api_client.requests.Session.post')
def test_make_request_connection_error(mock_post, client: BetfairAPIClient):
    mock_post.side_effect = ConnectionError("Connection error")
    response = client.make_request("test_endpoint", {"param": "value"})
    assert response is None

@patch('src.api_client.requests.Session.post')
def test_make_request_timeout(mock_post, client: BetfairAPIClient):
    mock_post.side_effect = Timeout("Timeout error")
    response = client.make_request("test_endpoint", {"param": "value"})
    assert response is None

@patch('src.api_client.requests.Session.post')
def test_make_request_request_exception(mock_post, client: BetfairAPIClient):
    mock_post.side_effect = RequestException("Request exception")
    response = client.make_request("test_endpoint", {"param": "value"})
    assert response is None

@patch('src.api_client.requests.Session.post')
def test_get_market_catalogue(mock_post, client: BetfairAPIClient):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"result": "success"}
    response = client.get_market_catalogue({"filter": "test"}, ["MARKET_START_TIME"], 10)
    assert response == {"result": "success"}

@patch('src.api_client.requests.Session.post')
def test_get_market_odds(mock_post, client: BetfairAPIClient):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"result": "success"}
    response = client.get_market_odds(["1.234"])
    assert response == {"result": "success"}

@patch('src.api_client.requests.Session.post')
def test_is_game_live(mock_post, client: BetfairAPIClient):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = [{"inplay": True}]
    assert client.is_game_live("1.234") == True
    mock_post.return_value.json.return_value = [{"inplay": False}]
    assert client.is_game_live("1.234") == False