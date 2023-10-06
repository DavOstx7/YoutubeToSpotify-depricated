from typing import List, Optional, AsyncGenerator
from python.youtube import api
from python.youtube.models import PlaylistQueryParams, PlaylistItemsPage
from python.core.logger import logger


class YoutubePlaylist:
    def __init__(self, api_key: str, playlist_id: str, max_results: int = 5):
        self._query_params = PlaylistQueryParams(api_key, playlist_id, max_results)
        self._current_page: Optional[PlaylistItemsPage] = None

    @property
    def is_in_initial_state(self) -> bool:
        return self._current_page is None

    @property
    def is_on_first_page(self) -> bool:
        if self.is_in_initial_state:
            return False
        return self._current_page.next_page_token and not self._current_page.prev_page_token

    @property
    def is_on_middle_page(self) -> bool:
        if self.is_in_initial_state:
            return False
        return self._current_page.next_page_token and self._current_page.prev_page_token

    @property
    def is_on_last_page(self) -> bool:
        if self.is_in_initial_state:
            return False
        return not self._current_page.next_page_token and self._current_page.prev_page_token

    def change_data(self, api_key: str, playlist_id: str, max_results: int = 5):
        self._query_params = PlaylistQueryParams(api_key, playlist_id, max_results)
        self._current_page = None

    def refresh(self):
        del self._query_params.page_token
        self._current_page = None

    async def search_for_page(self) -> PlaylistItemsPage:
        if self.is_in_initial_state:
            logger.debug("Searching for initial YouTube playlist page")
        else:
            logger.debug(f"Searching for YouTube playlist page with token '{self._query_params.page_token}'")

        response = await api.request_playlist_page(self._query_params.dict())
        self._current_page = PlaylistItemsPage(response)
        return self._current_page

    def next_page(self) -> bool:
        if self.is_on_last_page:
            return False
        self._query_params.page_token = self._current_page.next_page_token
        return True

    def prev_page(self) -> bool:
        if self.is_on_first_page:
            return False
        self._query_params.page_token = self._current_page.prev_page_token
        return True

    async def titles_batch_generator(self, max_batch_size: int = 100) -> AsyncGenerator[List[str], None]:
        logger.info("Starting to search for YouTube video titles inside the playlist...")

        titles_batch = []
        async for page in self.page_generator():
            for item in page.items:
                logger.debug(f"Found YouTube video title '{item.snippet.title}'")
                titles_batch.append(item.snippet.title)

                if len(titles_batch) >= max_batch_size:
                    yield titles_batch
                    titles_batch = []

        if titles_batch:
            yield titles_batch

    async def page_generator(self) -> AsyncGenerator[PlaylistItemsPage, None]:
        while not self.is_on_last_page:
            yield await self.search_for_page()
            self.next_page()
