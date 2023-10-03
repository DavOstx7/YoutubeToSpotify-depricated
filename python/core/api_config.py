import json
import os.path

SCRIPT_DIR = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(SCRIPT_DIR, "../..", "api_config.json")


def load_config() -> dict:
    with open(CONFIG_FILE, 'r') as config_file:
        return json.load(config_file)


class YouTubeAPIConfig:
    def __init__(self):
        self._config = load_config()["youtube"]

    @property
    def playlist_items_url(self) -> str:
        return self._config["urls"]["playlist_items"]

    @property
    def max_items_per_request(self) -> int:
        return self._config["max_items_per_request"]


class SpotifyAPIConfig:
    def __init__(self):
        self._config = load_config()["spotify"]

    @property
    def user_profile_url(self) -> str:
        return self._config["urls"]["user_profile"]

    @property
    def search_url(self) -> str:
        return self._config["urls"]["search"]

    @property
    def toke_url(self) -> str:
        return self._config["urls"]["token"]

    @property
    def authorization_url(self) -> str:
        return self._config["urls"]["authorization"]

    def playlists_url(self, user_id: str) -> str:
        return self._config["urls"]["playlists"].format(user_id=user_id)

    def tracks_url(self, playlist_id: str) -> str:
        return self._config["urls"]["tracks"].format(playlist_id=playlist_id)

    @property
    def authorization_scopes(self) -> str:
        return self._config["authorization_scopes"]

    @property
    def max_tracks_per_request(self) -> int:
        return self._config["max_tracks_per_request"]
