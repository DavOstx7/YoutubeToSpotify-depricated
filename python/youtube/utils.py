import requests
from python.core.http import http_request, StatusCodes
from python.core.api_config import YouTubeAPIConfig
from python.core.logger import logger

youtube_api = YouTubeAPIConfig()
MIN_POSITIVE_VALUE = 1


def validate_max_results_value(max_results: int):
    if not (MIN_POSITIVE_VALUE <= max_results <= youtube_api.max_items_per_request):
        valid_range = f"{MIN_POSITIVE_VALUE}-{youtube_api.max_items_per_request}"
        logger.error(f"The value of max results ({max_results}) is not in the valid range of {valid_range}")
        logger.critical("Exiting...")
        exit()


def get_playlist_query_params(api_key: str, playlist_id: str, max_results: int = 5) -> dict:
    validate_max_results_value(max_results)
    return {"key": api_key, "part": "snippet", "playlistId": playlist_id, "maxResults": max_results}


@http_request(expected_status_codes=[StatusCodes.OK])
def request_playlist_page(query_params: dict):
    return requests.get(youtube_api.playlist_items_url, params=query_params)
