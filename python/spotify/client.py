from typing import List, Optional
from python.spotify import api
from python.spotify.models import AccessToken, Track, UserProfile
from python.core.logger import logger


class SpotifyClient:
    def __init__(self, access_token: str):
        self._token = AccessToken(access_token)
        self._user: Optional[UserProfile] = None

    async def set_user_profile(self) -> 'SpotifyClient':
        response = await api.request_user_profile(self._token.header)
        self._user = UserProfile(response)
        return self

    async def create_playlist(self, name: str, description: str, is_public: bool) -> str:
        _playlist_type = "public" if is_public else "private"
        logger.info(f"Creating a new {_playlist_type} Spotify playlist '{name}'")

        response = await api.request_to_create_playlist(self._user.id, name, description, is_public, self._token.header)
        return response["id"]

    async def add_tracks(self, playlist_id: str, track_names: List[str], position: int = 0) -> Optional[str]:
        track_uris = await self._get_track_uris(track_names)

        if track_uris:
            logger.info(f"Adding {len(track_uris)} track uris to the Spotify playlist")
            response = await api.request_to_add_tracks(playlist_id, track_uris, position, self._token.header)
            return response["snapshot_id"]

        logger.warning("Could not find a single Spotify track uri for the given track names")

    async def _get_track_uris(self, track_names: List[str]) -> List[str]:
        logger.info(f"Starting to search Spotify track uris for {len(track_names)} track names...")

        track_uris = []
        for track_name in track_names:
            track_uri = await Track(track_name).search_for_uri(self._token.header)

            if track_uri:
                logger.debug(f"Found Spotify track uri '{track_uri}' for '{track_name}'")
                track_uris.append(track_uri)
            else:
                logger.warning(f"Failed to find a Spotify track uri for '{track_name}'")
        return track_uris
