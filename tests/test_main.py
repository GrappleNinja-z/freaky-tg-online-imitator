import os
import pytest
from src.config import Config

def test_config_validation():
    os.environ['API_KEY'] = 'test_key'
    os.environ['DATABASE_URL'] = 'test_db'
    os.environ['SECRET_TOKEN'] = 'test_token'

    config = Config.load()
    config.validate()

    assert config.api_key == 'test_key'
