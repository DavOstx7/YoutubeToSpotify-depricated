from typing import List, Optional
from python.youtube import api


class PlaylistQueryParams:
    def __init__(self, api_key: str, playlist_id: str, max_results: int = 5):
        self._params = api.get_playlist_query_params(api_key, playlist_id, max_results)

    def dict(self) -> dict:
        return self._params

    @property
    def api_key(self) -> str:
        return self._params["key"]

    @property
    def part(self) -> str:
        return self._params["part"]

    @property
    def playlist_id(self) -> str:
        return self._params["playlistId"]

    @property
    def max_results(self) -> int:
        return self._params["maxResults"]

    @property
    def page_token(self) -> Optional[str]:
        return self._params.get("pageToken")

    @page_token.setter
    def page_token(self, page_token: str):
        self._params["pageToken"] = page_token

    @page_token.deleter
    def page_token(self):
        if "pageToken" in self._params:
            del self._params["pageToken"]


class _PlaylistItemSnippet:
    def __init__(self, snippet: dict):
        self._snippet = snippet

    @property
    def published_at(self) -> str:
        return self._snippet['publishedAt']

    @property
    def channel_id(self) -> str:
        return self._snippet['channelId']

    @property
    def title(self) -> str:
        return self._snippet['title']

    @property
    def description(self) -> str:
        return self._snippet['description']

    @property
    def thumbnails(self) -> dict:
        return self._snippet['thumbnails']

    @property
    def channel_title(self) -> str:
        return self._snippet['channelTitle']

    @property
    def video_owner_channel_title(self) -> str:
        return self._snippet['videoOwnerChannelTitle']

    @property
    def video_owner_channel_id(self) -> str:
        return self._snippet['videoOwnerChannelId']

    @property
    def playlist_id(self) -> str:
        return self._snippet['playlistId']

    @property
    def position(self) -> int:
        return self._snippet['position']

    @property
    def resource_id(self) -> dict:
        return self._snippet['resourceId']

    @property
    def content_details(self) -> dict:
        return self._snippet['contentDetails']

    @property
    def status(self) -> dict:
        return self._snippet['status']


class _PlaylistItem:
    def __init__(self, item: dict):
        self._item = item

    @property
    def id(self) -> str:
        return self._item['id']

    @property
    def snippet(self) -> _PlaylistItemSnippet:
        return _PlaylistItemSnippet(self._item['snippet'])


class PlaylistItemsPage:
    def __init__(self, response: dict):
        self._response = response

    @property
    def id(self) -> str:
        return self._response['id']

    @property
    def next_page_token(self) -> Optional[str]:
        return self._response.get('nextPageToken')

    @property
    def prev_page_token(self) -> Optional[str]:
        return self._response.get('prevPageToken')

    @property
    def page_info(self) -> dict:
        return self._response['pageInfo']

    @property
    def items(self) -> List[_PlaylistItem]:
        return [_PlaylistItem(item) for item in self._response['items']]
