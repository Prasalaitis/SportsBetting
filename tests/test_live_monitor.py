import pytest
from src.live_monitor import monitor_live_game
from unittest.mock import patch

@patch('src.live_monitor.BetfairAPIClient.get_market_odds')
@patch('src.live_monitor.BetfairAPIClient.is_game_live')
def test_monitor_live_game_edge_cases(mock_is_game_live, mock_get_market_odds):
    # Simulate different scenarios
    mock_is_game_live.side_effect = [True, False, True]
    mock_get_market_odds.side_effect = [
        [{'marketId': '1.234', 'runners': [{'ex': {'availableToBack': [{'price': 1.8}]}}]}],
        [],
        [{'marketId': '1.234', 'runners': [{'ex': {'availableToBack': [{'price': 1.5}]}}]}]
    ]
    client = BetfairAPIClient(app_key="test_app_key", session_token="test_session_token")
    pre_game_odds = {'marketId': '1.234', 'selectionId': 1, 'odds': 1.9, 'type': 'back'}
    result = monitor_live_game(client, '1.234', pre_game_odds, threshold=0.2)
    assert result == {
        'marketId': '1.234',
        'current_total_games': 1.5,
        'pre_game_total_games': 1.9
    }