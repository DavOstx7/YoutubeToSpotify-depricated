from typing import List
from python.spotify import api
from python.spotify.models import Token, Track, UserProfile
from python.core.logger import logger


class SpotifyClient:
    def __init__(self, access_token: str):
        self._token = Token(access_token)
        self._user = UserProfile(api.request_user_profile(self._token.header))

    def create_playlist(self, name: str, description: str, is_public: bool) -> str:
        _playlist_type = "public" if is_public else "private"
        logger.info(f"Creating a new {_playlist_type} Spotify playlist with the name of '{name}'")

        response = api.request_to_create_playlist(self._user.id, name, description, is_public, self._token.header)
        return response["id"]

    def add_tracks(self, playlist_id: str, track_names: List[str], position: int = 0) -> str:
        track_uris = self._get_track_uris(track_names)
        logger.info(f"Found {len(track_uris)} track uris to add to the Spotify playlist...")

        response = api.request_to_add_tracks(playlist_id, track_uris, position, self._token.header)
        return response["snapshot_id"]

    def _get_track_uris(self, track_names: List[str]):
        logger.info(f"Searching track uris for {len(track_names)} track names")

        track_uris = []
        for track_name in track_names:
            track_uri = Track(track_name).search_for_uri(self._token.header)
            if track_uri:
                logger.debug(f"Found a Spotify track uri of {track_uri} for '{track_name}'")
                track_uris.append(track_uri)
            else:
                logger.warning(f"Failed to find a Spotify track uri for '{track_name}'")
        return track_uris
