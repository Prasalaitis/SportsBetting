import time
from typing import Dict
from src.api_client import BetfairAPIClient
from src.utils import log_game
from src.kafka_producer import produce_message

def monitor_live_game(client: BetfairAPIClient, market_id: str, pre_game_odds: Dict[str, float], threshold: float = 0.2) -> Dict[str, float]:
    while True:
        if client.is_game_live(market_id):
            market_odds = client.get_market_odds([market_id])
            if market_odds:
                current_total_games = market_odds[0]['runners'][0]['ex']['availableToBack'][0]['price']
                if abs(current_total_games - pre_game_odds['odds']) >= threshold:
                    log_game(market_id, pre_game_odds['odds'], current_total_games)
                    message = {
                        'marketId': market_id,
                        'current_total_games': current_total_games,
                        'pre_game_total_games': pre_game_odds['odds']
                    }
                    produce_message('betfair_topic', message)
                    return message
        time.sleep(60)  # Check every minute