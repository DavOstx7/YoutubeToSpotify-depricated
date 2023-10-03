import json
import os.path

SCRIPT_DIR = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(SCRIPT_DIR, "../..", "user_config.json")


def load_user_config() -> dict:
    with open(CONFIG_FILE, 'r') as config_file:
        return json.load(config_file)


class LoggingUserConfig:
    def __init__(self):
        self._config = load_user_config()["logging"]

    @property
    def level(self) -> str:
        return self._config["level"]


class YouTubeUserConfig:
    def __init__(self):
        self._config = load_user_config()["youtube"]

    @property
    def api_key(self) -> str:
        return self._config["api_key"]

    @property
    def playlist_id(self) -> str:
        return self._config["playlist_id"]


class SpotifyUserConfig:
    def __init__(self):
        self._config = load_user_config()["spotify"]

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
