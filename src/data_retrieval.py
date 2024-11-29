from datetime import datetime, timedelta
from src.api_client import BetfairAPIClient

def get_pre_game_odds(client, market_type_code, odds_threshold=1.9):
    now = datetime.utcnow()
    tomorrow = now + timedelta(days=1)
    market_filter = {
        'eventTypeIds': ['7522'],  # Event type ID for basketball (NBA)
        'marketTypeCodes': [market_type_code],
        'marketStartTime': {
            'from': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'to': tomorrow.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    }
    market_catalogue = client.get_market_catalogue(market_filter, ['MARKET_START_TIME'], 100)
    market_ids = [market['marketId'] for market in market_catalogue]
    market_odds = client.get_market_odds(market_ids)

    filtered_odds = []
    for market in market_odds:
        for runner in market['runners']:
            best_back_price = runner['ex']['availableToBack'][0]['price'] if runner['ex']['availableToBack'] else None
            if best_back_price and abs(best_back_price - odds_threshold) < 0.1:
                filtered_odds.append({
                    'marketId': market['marketId'],
                    'selectionId': runner['selectionId'],
                    'odds': best_back_price,
                    'type': 'back'
                })
    return filtered_odds