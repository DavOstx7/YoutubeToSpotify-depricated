import logger from "../common/logger";
import api from "./api";
import { PlaylistQueryParams, PlaylistItemsPage } from "./models";

export class YouTubePlaylist {
    private queryParams: PlaylistQueryParams;
    private currentPage: PlaylistItemsPage | undefined;

    constructor(apiKey: string, playlistId: string, maxResults: number = 5) {
        this.queryParams = api.getPlaylistQueryParams(apiKey, playlistId, maxResults);
        this.currentPage = undefined;
    }

    get isInInitialState(): boolean {
        return this.currentPage === undefined;
    }

    get isOnFirstPage(): boolean {
        if (this.isInInitialState) {
            return false;
        }
        
        return this.currentPage!.nextPageToken !== undefined && this.currentPage.prevPageToken === undefined;
    }

    get isOnMiddlePage(): boolean {
        if (this.isInInitialState) {
            return false;
        }
        return this.currentPage.nextPageToken !== undefined && this.currentPage.prevPageToken !== undefined;
    }

    get isOnLastPage(): boolean {
        if (this.isInInitialState) {
            return false;
        }
        return this.currentPage.nextPageToken === undefined && this.currentPage.prevPageToken !== undefined;
    }

    public changeData(apiKey: string, playlistId: string, maxResults: number = 5) {
        this.queryParams = api.getPlaylistQueryParams(apiKey, playlistId, maxResults);
        this.currentPage = undefined;
    }

    public refresh() {
        if (this.queryParams.pageToken !== undefined) {
            delete this.queryParams.pageToken;
        }
        this.currentPage = undefined;
    }

    public async searchForPage(): Promise<PlaylistItemsPage> {
        if (this.isInInitialState) {
            logger.debug("Searching for the initial YouTube playlist page");
        } else {
            logger.debug(`Searching for a YouTube playlist page with a token of: ${this.queryParams.pageToken}`);
        }

        this.currentPage = await api.requestPlaylistPage(this.queryParams);
        return this.currentPage;
    }

    public nextPage(): boolean {
        if (this.isOnLastPage) {
            return false;
        } 
        this.queryParams.pageToken = this.currentPage.nextPageToken;
        return true;
    }

    public prevPage(): boolean {
        if (this.isOnFirstPage) {
            return false;
        } 
        this.queryParams.pageToken = this.currentPage.prevPageToken;
        return true;
    }

    public async *titlesBatchGenerator(maxBatchSize: number = 100): AsyncIterable<string[]> {
        logger.info("Starting to search for YouTube video titles inside the playlist...");

        let titlesBatch: string[] = [];
        for await (const page of this) {
            for (const item of page.items) {
                logger.debug(`Found YouTube video title '${item.snippet.title}'`);
                titlesBatch.push(item.snippet.title);
                
                if (titlesBatch.length >= maxBatchSize){
                    yield titlesBatch;
                    titlesBatch = [];
                }
            }
        }

        if (titlesBatch.length > 0){
            yield titlesBatch;
        }
    }

    [Symbol.asyncIterator]() {
        return {
            next: async () => {
                if (this.isOnLastPage) {
                    return { done: true };
                }
                const value = await this.searchForPage();
                this.nextPage();
                return { value, done: false };
            }
        };
    }
}
