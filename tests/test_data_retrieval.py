import pytest
from src.data_retrieval import get_pre_game_odds
from unittest.mock import patch

@patch('src.data_retrieval.BetfairAPIClient.get_market_catalogue')
@patch('src.data_retrieval.BetfairAPIClient.get_market_odds')
def test_get_pre_game_odds(mock_get_market_odds, mock_get_market_catalogue):
    mock_get_market_catalogue.return_value = [{'marketId': '1.234'}]
    mock_get_market_odds.return_value = [{
        'marketId': '1.234',
        'runners': [{
            'selectionId': '5678',
            'ex': {
                'availableToBack': [{'price': 1.9}]
            }
        }]
    }]
    client = Betfair