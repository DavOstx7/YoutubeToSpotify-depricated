import logger from "../common/logger";
import api from "./api";
import { AuthorizationHeader } from "./models";

export class SpotifyClient {
    private accessToken: string;
    private userId: string;
    
    constructor(accessToken: string) {
        this.accessToken = accessToken;
        this.userId = undefined;
    }

    get authorizationHeader(): AuthorizationHeader {
        return {"Authorization": `Bearer ${this.accessToken}`};
    }

    public async setUserId(): Promise<SpotifyClient> {
        const response = await api.requestUserProfile(this.authorizationHeader);
        this.userId = response.id;
        return this;
    }

    public async createPlaylist(name: string, description: string, isPublic: boolean): Promise<string> {
        const _playlistType = isPublic ? "public" : "private";
        logger.info(`Creating a new ${_playlistType} Spotify playlist '${name}'`);

        const response = await api.requestToCreatePlaylist(this.userId, name, description, isPublic, this.authorizationHeader);
        return response.id;
    }

    public async addTracks(playlistId: string, trackNames: string[], position: number = 0): Promise<string | undefined> {
        const trackUris = await this.getTrackUris(trackNames);

        if(trackUris.length == 0) {
            logger.warning("Could not find a single Spotify track uri for the given track names");
            return undefined;
        }

        logger.info(`Adding ${trackUris.length} track uris to the Spotify playlist`);
        const response = await api.requestToAddTracks(playlistId, trackUris, position, this.authorizationHeader);
        return response.snapshot_id;

    }

    private async getTrackUris(trackNames: string[]): Promise<string[]> {
        logger.info(`Starting to search Spotify track uris for ${trackNames.length} track names...`);

        const trackUris: string[] = [];
        for (const trackName of trackNames) {
            const trackUri = await this.searchForTrackUri(trackName);

            if (trackUri) {
                logger.debug(`Found Spotify track uri '${trackUri}' for '${trackName}'`);
                trackUris.push(trackUri);
            } else {
                logger.warning(`Failed to find a Spotify track uri for '${trackName}'`);
            }
        }
        return trackUris;
    }

    private async searchForTrackUri(trackName: string): Promise<string | undefined> {
        const response = await api.requestToSearchForTracks(trackName, 1, this.authorizationHeader);

        if ("tracks" in response) {
            const items: any[] = response.tracks.items;
            if (items.length > 0) {
                return items[0]["uri"] ?? undefined;
            }
        }
        return undefined;
    };
}
