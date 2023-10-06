from typing import Optional
from python.spotify import api


class AccessToken:
    def __init__(self, access_token: str):
        self._access_token = access_token

    @property
    def header(self) -> dict:
        return {
            "Authorization": f"Bearer {self._access_token}"
        }


class Track:
    def __init__(self, name: str):
        self.name = name

    async def search_for_uri(self, headers: dict) -> Optional[str]:
        response = await api.request_to_search_for_track(self.name, limit=1, headers=headers)

        if "tracks" in response:
            items: list = response["tracks"]["items"]
            if items:
                return items[0].get("uri")


class UserProfile:
    def __init__(self, _response: dict):
        self._response = _response

    @property
    def id(self) -> str:
        return self._response["id"]

    @property
    def uri(self) -> str:
        return self._response["uri"]
