from src.api_client import BetfairAPIClient
from src.data_retrieval import get_pre_game_odds
from src.live_monitor import monitor_live_game
from src.kafka_consumer import consume_messages
from src.config import settings

def main() -> None:
    client = BetfairAPIClient(settings.app_key, settings.session_token)

    # Get pre-game odds for NBA total points market
    pre_game_odds = get_pre_game_odds(client, 'TOTAL_POINTS')
    print("Pre-game odds:", pre_game_odds)

    # Monitor live game for the first market found
    if pre_game_odds:
        result = monitor_live_game(client, pre_game_odds['marketId'], pre_game_odds, threshold=0.2)
        print("Live game result:", result)

    # Consume messages from Kafka
    consume_messages(settings.kafka_topic)

if __name__ == "__main__":
    main()