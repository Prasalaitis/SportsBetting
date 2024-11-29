import logging
from src.api_client import BetfairAPIClient
from src.data_retrieval import get_pre_game_odds
from src.config import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def main() -> None:
    client = BetfairAPIClient(settings.app_key, settings.session_token)

    # Get pre-game odds for NBA total points market
    pre_game_odds = get_pre_game_odds(client, 'TOTAL_POINTS')
    logging.info("Pre-game odds:")
    if pre_game_odds:
        logging.info(f"Market ID: {pre_game_odds['marketId']}, Odds: {pre_game_odds['odds']}")

if __name__ == "__main__":
    main()