import os.path
from python.config.base import BaseJSONConfig

SCRIPT_DIR = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(SCRIPT_DIR, "../..", "receive_token_config.json")


class SpotifyReceiveTokenConfig(BaseJSONConfig):
    def __init__(self):
        super().__init__(CONFIG_FILE, "spotify")

    @property
    def client_id(self) -> str:
        return self._config["client_id"]

    @property
    def client_secret(self) -> str:
        return self._config["client_secret"]

    @property
    def redirect_uri(self) -> str:
        return self._config["redirect_uri"]
