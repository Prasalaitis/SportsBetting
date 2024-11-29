import pytest
from src.utils import log_game
import logging

def test_log_game(caplog):
    with caplog.at_level(logging.INFO):
        log_game('1.234', 1.9, 1.8)
    assert "Market ID: 1.234, Pre-game Total Games: 1.9, Current Total Games: 1.8" in caplog.text