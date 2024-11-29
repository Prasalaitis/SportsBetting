import requests
import json
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from typing import Any, Dict, List, Optional

class BetfairAPIClient:
    def __init__(self, app_key: str, session_token: str):
        self.app_key = app_key
        self.session_token = session_token
        self.base_url = "https://api.betfair.com/exchange/betting/rest/v1.0/"
        self.logger = logging.getLogger(__name__)
        self.session = self._init_session()

    def _init_session(self) -> requests.Session:
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        return session

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        headers = {
            'X-Application': self.app_key,
            'X-Authentication': self.session_token,
            'Content-Type': 'application/json'
        }
        try:
            response = self.session.post(self.base_url + endpoint, headers=headers, data=json.dumps(params))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error occurred: {e}")
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Connection error occurred: {e}")
        except requests.exceptions.Timeout as e:
            self.logger.error(f"Timeout error occurred: {e}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
        return None

    def get_market_catalogue(self, market_filter: Dict[str, Any], market_projection: List[str], max_results: int) -> Optional[Dict[str, Any]]:
        endpoint = "listMarketCatalogue/"
        params = {
            'filter': market_filter,
            'marketProjection': market_projection,
            'maxResults': max_results
        }
        return self._make_request(endpoint, params)

    def get_market_odds(self, market_ids: List[str]) -> Optional[Dict[str, Any]]:
        endpoint = "listMarketBook/"
        params = {
            'marketIds': market_ids,
            'priceProjection': {
                'priceData': ['EX_BEST_OFFERS']
            }
        }
        return self._make_request(endpoint, params)

    def is_game_live(self, market_id: str) -> bool:
        market_book = self.get_market_odds([market_id])
        if market_book:
            return market_book[0].get('inplay', False)
        return False