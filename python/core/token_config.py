import json
import os.path

SCRIPT_DIR = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(SCRIPT_DIR, "../..", "spotify_token_config.json")


def load_spotify_token_config() -> dict:
    with open(CONFIG_FILE, 'r') as config_file:
        return json.load(config_file)


class SpotifyTokenConfig:
    def __init__(self):
        self._config = load_spotify_token_config()

    @property
    def client_id(self) -> str:
        return self._config["client_id"]

    @property
    def client_secret(self) -> str:
        return self._config["client_secret"]

    @property
    def redirect_uri(self) -> str:
        return self._config["redirect_uri"]