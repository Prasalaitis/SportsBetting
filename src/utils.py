import logging

logging.basicConfig(filename='game_log.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def log_game(market_id: str, pre_game_total_games: float, current_total_games: float) -> None:
    logging.info(f"Market ID: {market_id}, Pre-game Total Games: {pre_game_total_games}, Current Total Games: {current_total_games}")