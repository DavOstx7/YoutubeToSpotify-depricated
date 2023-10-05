import os.path
from python.config.base import BaseJSONConfig

SCRIPT_DIR = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(SCRIPT_DIR, "../..", "user_config.json")

UNSET_CONFIG_VALUE = "?"


class LoggingUserConfig(BaseJSONConfig):
    def __init__(self):
        super().__init__(CONFIG_FILE, "logging")

    @property
    def level(self) -> str:
        return self._config["level"]


class YouTubeUserConfig(BaseJSONConfig):
    def __init__(self):
        super().__init__(CONFIG_FILE, "youtube")

    @property
    def api_key(self) -> str:
        return self._config["api_key"]

    @property
    def playlist_id(self) -> str:
        return self._config["playlist_id"]


class SpotifyUserConfig(BaseJSONConfig):
    def __init__(self):
        super().__init__(CONFIG_FILE, "spotify")

    @property
    def access_token(self) -> str:
        return self._config["access_token"]

    @property
    def playlist_name(self) -> str:
        return self._config["playlist"]["name"]

    @property
    def playlist_description(self) -> str:
        return self._config["playlist"]["description"]

    @property
    def is_public_playlist(self) -> bool:
        return self._config["playlist"]["public"]

    @property
    def existing_playlist_id(self) -> str:
        return self._config["playlist"]["existing_id"]

    @property
    def is_existing_playlist_id_set(self) -> bool:
        return self.existing_playlist_id != UNSET_CONFIG_VALUE
