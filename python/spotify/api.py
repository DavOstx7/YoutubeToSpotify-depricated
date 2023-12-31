import httpx
import base64
import webbrowser
import urllib.parse
from typing import List
from python.core.http import http_request, StatusCodes
from python.config.api import SpotifyAPIConfig
from python.core.exceptions import ValidationError

MIN_POSITIVE_VALUE = 1
client = httpx.AsyncClient()
config = SpotifyAPIConfig()


def validate_track_uris_size(track_uris: List[str]):
    track_uris_size = len(track_uris)
    if not (MIN_POSITIVE_VALUE <= track_uris_size <= config.max_tracks_per_request):
        valid_range = f"{MIN_POSITIVE_VALUE}-{config.max_tracks_per_request}"
        raise ValidationError(f"The size of track uris ({track_uris_size}) is not in the valid range of {valid_range}")


def get_authorization_query_params(client_id: str, redirect_uri: str) -> dict:
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": config.authorization_scopes
    }
    return urllib.parse.urlencode(params)


def get_request_access_token_headers(client_id: str, client_secret: str) -> dict:
    auth = f"{client_id}:{client_secret}"
    auth_64 = base64.urlsafe_b64encode(auth.encode()).decode()
    return {
        "Authorization": f"Basic {auth_64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }


def get_request_access_token_form_body(code: str, redirect_uri: str) -> dict:
    return {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }


@http_request(expected_status_codes=[StatusCodes.OK])
async def request_access_token(client_id: str, client_secret: str, code: str, redirect_uri: str):
    headers = get_request_access_token_headers(client_id, client_secret)
    form_body = get_request_access_token_form_body(code, redirect_uri)
    return await client.post(config.token_url, headers=headers, data=form_body)


@http_request(expected_status_codes=[StatusCodes.OK])
async def request_user_profile(headers: dict):
    return await client.get(config.user_profile_url, headers=headers)


@http_request(expected_status_codes=[StatusCodes.CREATED])
async def request_to_create_playlist(user_id: str, name: str, description: str, is_public: bool, headers: dict):
    url = config.playlists_url(user_id)
    headers = {"Content-Type": "application/json", **headers}
    json_body = {"name": name, "description": description, "public": is_public}
    return await client.post(url, headers=headers, json=json_body)


@http_request(expected_status_codes=[StatusCodes.OK])
async def request_to_search_for_track(name: str, limit: int, headers: dict):
    query_params = {"q": name, "type": "track", "limit": limit}
    return await client.get(config.search_url, params=query_params, headers=headers)


@http_request(expected_status_codes=[StatusCodes.CREATED])
async def request_to_add_tracks(playlist_id: str, track_uris: List[str], position: int, headers: dict):
    validate_track_uris_size(track_uris)
    url = config.tracks_url(playlist_id)
    headers = {"Content-Type": "application/json", **headers}
    json_body = {"uris": track_uris, "position": position}
    return await client.post(url, headers=headers, json=json_body)


def authorize_via_browser(client_id: str, redirect_uri: str):
    query_params = get_authorization_query_params(client_id, redirect_uri)
    webbrowser.open(f"{config.authorization_url}?{query_params}")
