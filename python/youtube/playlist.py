from typing import Optional, Iterator, List
from python.youtube import utils
from python.youtube.models import PlaylistItemsPage
from python.core.logger import logger


class YoutubePlaylist:
    def __init__(self, api_key: str, playlist_id: str, max_results: int = 5):
        self._query_params: dict = utils.get_playlist_query_params(api_key, playlist_id, max_results)
        self._last_page: PlaylistItemsPage = None

    @property
    def is_in_initial_state(self) -> bool:
        return self._last_page is None

    @property
    def is_on_first_page(self) -> bool:
        if self.is_in_initial_state:
            return False
        return self._last_page.next_page_token and not self._last_page.prev_page_token

    @property
    def is_on_middle_page(self) -> bool:
        if self.is_in_initial_state:
            return False
        return self._last_page.next_page_token and self._last_page.prev_page_token

    @property
    def is_on_last_page(self) -> bool:
        if self.is_in_initial_state:
            return False
        return not self._last_page.next_page_token and self._last_page.prev_page_token

    def change_data(self, api_key: str, playlist_id: str, max_results: int = 5):
        self._query_params = utils.get_playlist_query_params(api_key, playlist_id, max_results)
        self._last_page = None

    def refresh(self):
        if "pageToken" in self._query_params:
            del self._query_params["pageToken"]
        self._last_page = None

    def search_for_page(self) -> Optional[PlaylistItemsPage]:
        if self.is_in_initial_state:
            logger.debug(f"Searching for the initial YouTube playlist page")
        else:
            logger.debug("Searching for a YouTube playlist page with a token of: ", self._query_params["pageToken"])

        response = utils.request_playlist_page(self._query_params)
        self._last_page = PlaylistItemsPage(response)
        return self._last_page

    def next_page(self) -> bool:
        if self.is_on_last_page:
            return False
        self._query_params["pageToken"] = self._last_page.next_page_token
        return True

    def prev_page(self) -> bool:
        if self.is_on_first_page:
            return False
        self._query_params["pageToken"] = self._last_page.prev_page_token
        return True

    def titles_batch_iterator(self, size: int = 100) -> Iterator[List[str]]:
        logger.info("Starting to search for YouTube videos title inside the playlist...")
        titles_batch = []
        for page in self:
            for item in page.items:
                logger.debug(f"Found YouTube video title '{item.snippet.title}'")
                titles_batch.append(item.snippet.title)

                if len(titles_batch) >= size:
                    yield titles_batch
                    titles_batch = []

        if titles_batch:
            yield titles_batch

    def __iter__(self) -> 'YoutubePlaylist':
        return self

    def __next__(self) -> PlaylistItemsPage:
        if self.is_on_last_page:
            raise StopIteration
        page = self.search_for_page()
        self.next_page()
        return page
