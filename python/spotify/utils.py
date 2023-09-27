import requests
import base64
import webbrowser
import urllib.parse
from typing import List
from python.core.http import http_request, StatusCodes
from python.core.api_config import SpotifyAPIConfig
from python.core.logger import logger

spotify_api = SpotifyAPIConfig()
MIN_POSITIVE_VALUE = 1


def validate_tracks_uri_size(tracks_uri: List[str]):
    tracks_uri_size = len(tracks_uri)
    if not (MIN_POSITIVE_VALUE <= tracks_uri_size <= spotify_api.max_tracks_per_request):
        valid_range = f"{MIN_POSITIVE_VALUE}-{spotify_api.max_tracks_per_request}"
        logger.error(f"The size of tracks uri ({tracks_uri_size}) is not in the valid range of {valid_range}")
        logger.critical("Exiting...")
        exit()


def get_authorization_headers(client_id: str, redirect_uri: str) -> dict:
    return {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": spotify_api.authorization_scopes
    }


def get_request_token_headers(client_id: str, client_secret: str) -> dict:
    auth = f"{client_id}:{client_secret}"
    auth_64 = base64.urlsafe_b64encode(auth.encode()).decode()
    return {
        "Authorization": f"Basic {auth_64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }


def get_request_token_data(code: str, redirect_uri: str) -> dict:
    return {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }


@http_request(expected_status_codes=[StatusCodes.OK])
def request_authorization_token(client_id: str, client_secret: str, code: str, redirect_uri: str):
    headers = get_request_token_headers(client_id, client_secret)
    data = get_request_token_data(code, redirect_uri)
    return requests.post(spotify_api.toke_url, headers=headers, data=data)


@http_request(expected_status_codes=[StatusCodes.OK])
def request_user_profile(headers: dict) -> requests.Response:
    return requests.get(spotify_api.user_profile_url, headers=headers)


@http_request(expected_status_codes=[StatusCodes.CREATED])
def request_to_create_playlist(user_id: str, name: str, description: str, is_public: bool, headers: dict):
    url = spotify_api.playlists_url(user_id)
    headers = {"Content-Type": "application/json", **headers}
    data = {"name": name, "description": description, "public": is_public}
    return requests.post(url, headers=headers, json=data)


@http_request(expected_status_codes=[StatusCodes.OK])
def request_to_search_for_track(name: str, limit: int, headers: dict):
    query_params = {"q": name, "type": "track", "limit": limit}
    return requests.get(spotify_api.search_url, params=query_params, headers=headers)


@http_request(expected_status_codes=[StatusCodes.CREATED])
def request_to_add_tracks(playlist_id: str, tracks_uri: List[str], position: int, headers: dict):
    validate_tracks_uri_size(tracks_uri)
    url = spotify_api.tracks_url(playlist_id)
    headers = {"Content-Type": "application/json", **headers}
    data = {"uris": tracks_uri, "position": position}
    return requests.post(url, headers=headers, json=data)


def authorize_via_browser(client_id: str, redirect_uri: str):
    headers = get_authorization_headers(client_id, redirect_uri)
    query_params = urllib.parse.urlencode(headers)
    webbrowser.open(f"{spotify_api.authorization_url}?{query_params}")


def print_authorization_token(client_id: str, client_secret: str, code: str, redirect_uri: str):
    response = request_authorization_token(client_id, client_secret, code, redirect_uri)
    access_token = response["access_token"]
    print(f"Access Token -> {access_token}")
