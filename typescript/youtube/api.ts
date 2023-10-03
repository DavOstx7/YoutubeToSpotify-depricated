import apiConfig from '../../api_config.json';
import { URLSearchParams } from 'url';
import { HttpRequest, StatusCodes } from '../common/http';
import { PlaylistQueryParams } from './models';
import { ValidationError } from '../common/errors';

const MIN_POSITIVE_VALUE = 1;
export const config = apiConfig.youtube;


export class YouTubeAPIRequests {
    public getPlaylistQueryParams(apiKey: string, playlistId: string, maxResults: number = 5): PlaylistQueryParams {
        this.validateMaxResultsValue(maxResults);
        return { "key": apiKey, "part": "snippet", "playlistId": playlistId, "maxResults": maxResults };
    }

    @HttpRequest([StatusCodes.OK])
    public async requestPlaylistPage(queryParams: PlaylistQueryParams): Promise<any> {
        const url = `${config.urls.playlist_items}?${new URLSearchParams(queryParams as {})}`;
        return await fetch(url);
    }

    private isValidMaxResultsValue(maxResults: number): boolean {
        return maxResults >= MIN_POSITIVE_VALUE && maxResults <= config.max_items_per_request;
    }
    
    private validateMaxResultsValue(maxResults: number) {
        if (! this.isValidMaxResultsValue(maxResults)) {
            const validRange = `${MIN_POSITIVE_VALUE}-${config.max_items_per_request}`;
            throw new ValidationError(`The value of max results is not in the valid range of ${validRange}`);
        }
    }
}

const api = new YouTubeAPIRequests();
export default api;
