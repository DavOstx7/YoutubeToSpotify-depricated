from typing import List
from python.spotify import utils
from python.spotify.models import Token, Track, UserProfile
from python.core.logger import logger


class SpotifyClient:
    def __init__(self, access_token: str):
        self._token = Token(access_token)
        self._user = UserProfile(utils.request_user_profile(self._token.header))

    def create_playlist(self, name: str, description: str, is_public: bool) -> str:
        _playlist_type = "public" if is_public else "private"
        logger.info(f"Creating a new {_playlist_type} Spotify playlist with the name of '{name}'")

        response = utils.request_to_create_playlist(self._user.id, name, description, is_public, self._token.header)
        return response["id"]

    def add_tracks(self, playlist_id: str, names: List[str], position: int = 0) -> str:
        tracks_uri = self._get_tracks_uri(names)
        logger.info(f"Adding {len(tracks_uri)} tracks to the Spotify playlist...")

        response = utils.request_to_add_tracks(playlist_id, tracks_uri, position, self._token.header)
        return response["snapshot_id"]

    def _get_tracks_uri(self, names: List[str]):
        tracks_uri = []
        for name in names:
            track_uri = Track(name).search_for_uri(self._token.header)
            if track_uri:
                logger.debug(f"Found a Spotify track uri of {track_uri} for '{name}'")
                tracks_uri.append(track_uri)
            else:
                logger.warning(f"Failed to find a Spotify track uri found for '{name}'")
        return tracks_uri
