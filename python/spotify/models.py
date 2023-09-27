from typing import Optional, List
from python.spotify import utils


class Token:
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

    def search_for_uri(self, headers: dict) -> Optional[str]:
        response = utils.request_to_search_for_track(self.name, limit=1, headers=headers)

        if "tracks" in response:
            items: list = response["tracks"]["items"]
            if items:
                return items[0].get("uri")


class UserProfile:
    def __init__(self, _response: dict):
        self._response = _response

    @property
    def country(self) -> str:
        return self._response["country"]

    @property
    def display_name(self) -> str:
        return self._response["display_name"]

    @property
    def email(self) -> str:
        return self._response["email"]

    @property
    def explicit_content(self) -> dict:
        return self._response["explicit_content"]

    @property
    def external_urls(self) -> dict:
        return self._response["external_urls"]

    @property
    def followers(self) -> dict:
        return self._response["followers"]

    @property
    def href(self) -> str:
        return self._response["href"]

    @property
    def id(self) -> str:
        return self._response["id"]

    @property
    def images(self) -> List[dict]:
        return self._response["images"]

    @property
    def product(self) -> str:
        return self._response["product"]

    @property
    def type(self) -> str:
        return self._response["type"]

    @property
    def uri(self) -> str:
        return self._response["uri"]
