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
    def new_playlist_name(self) -> str:
        return self._config["new_playlist"]["name"]

    @property
    def new_playlist_description(self) -> str:
        return self._config["new_playlist"]["description"]

    @property
    def is_new_playlist_public(self) -> bool:
        return self._config["new_playlist"]["public"]

    @property
    def existing_playlist_id(self) -> str:
        return self._config["existing_playlist"]["id"]

    def is_existing_playlist_id_set(self) -> bool:
        return self.existing_playlist_id != UNSET_CONFIG_VALUE
