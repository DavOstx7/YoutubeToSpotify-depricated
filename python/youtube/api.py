import httpx
from python.core.http import http_request, StatusCodes
from python.config.api import YouTubeAPIConfig
from python.core.exception import ValidationError

MIN_POSITIVE_VALUE = 1
client = httpx.AsyncClient()
config = YouTubeAPIConfig()


def validate_max_results_value(max_results: int):
    if not (MIN_POSITIVE_VALUE <= max_results <= config.max_items_per_request):
        valid_range = f"{MIN_POSITIVE_VALUE}-{config.max_items_per_request}"
        raise ValidationError(f"The value of max results ({max_results}) is not in the valid range of {valid_range}")


def get_playlist_query_params(api_key: str, playlist_id: str, max_results: int = 5) -> dict:
    validate_max_results_value(max_results)
    return {"key": api_key, "part": "snippet", "playlistId": playlist_id, "maxResults": max_results}


@http_request(expected_status_codes=[StatusCodes.OK])
async def request_playlist_page(query_params: dict):
    return await client.get(config.playlist_items_url, params=query_params)
