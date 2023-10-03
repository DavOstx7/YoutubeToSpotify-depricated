import apiConfig from '../../api_config.json';
import { URLSearchParams } from 'url';
import { HttpRequest, StatusCodes } from '../common/http';
import { RequestAccessTokenHeaders } from './models';
import { ValidationError } from '../common/errors';

const MIN_POSITIVE_VALUE = 1;
export const config = apiConfig.spotify;

export class SpotifyAPIRequests {
    public getAuthorizationQueryParams(clientId: string, redirectUri: string): URLSearchParams {
        return new URLSearchParams({
            client_id: clientId,
            response_type: "code",
            redirect_uri: redirectUri,
            scope: apiConfig.spotify.authorization_scopes
        });
    }

    private getRequestAccessTokenHeaders(clientId: string, clientSecret: string): RequestAccessTokenHeaders {
        const auth = `${clientId}:${clientSecret}`;
        const auth64 = Buffer.from(auth).toString("base64");

        return {
            "Authorization": `Basic ${auth64}`,
            "Content-Type": "application/x-www-form-urlencoded"
        };
    }

    private getRequestAccessTokenFormBody(code: string, redirectUri: string): URLSearchParams {
        return new URLSearchParams({
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirectUri
        });
    }
    
    @HttpRequest([StatusCodes.OK])
    public async requestAccessToken(clientId: string, clientSecret: string, code: string, redirectUri: string): Promise<any> {
        const headers = this.getRequestAccessTokenHeaders(clientId, clientSecret);
        const formBody = this.getRequestAccessTokenFormBody(code, redirectUri);

        return await fetch(config.urls.token, {
            method: "POST",
            headers: headers,
            body: formBody.toString()
        });

    }

    @HttpRequest([StatusCodes.OK])
    public async requestUserProfile(headers: {}): Promise<any> {
        return await fetch(config.urls.user_profile, {
            method: "GET",
            headers: headers
        });
    }

    @HttpRequest([StatusCodes.CREATED])
    public async requestToCreatePlaylist(userId: string, name: string, description: string, isPublic: boolean, headers: {}): Promise<any> {
        const url = config.urls.playlists.replace("{user_id}", userId);
        const jsonBody = {"name": name, "description": description, "public": isPublic};

        return await fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json", ...headers},
            body: JSON.stringify(jsonBody)
        });
    }

    @HttpRequest([StatusCodes.OK])
    public async requestToSearchForTracks(name: string, limit: number, headers: {}): Promise<any> {
        const queryParams = new URLSearchParams({"q": name, "type": "track", "limit": limit} as {});
        const url = `${config.urls.search}?${queryParams}`;

        return await fetch(url, {
            method: "GET",
            headers: headers
        });
    }

    @HttpRequest([StatusCodes.CREATED])
    public async requestToAddTracks(playlistId: string, trackUris: string[], position: number, headers: {}): Promise<any> {
        this.validateTrackUrisSize(trackUris);
        const url = config.urls.tracks.replace("{playlist_id}", playlistId);
        const jsonBody = {"uris": trackUris, "position": position};

        return await fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json", ...headers},
            body: JSON.stringify(jsonBody)
        });
    }

    private validateTrackUrisSize(trackUris: string[]) {
        if (! this.isValidTrackUrisSize(trackUris)) {
            const validRange = `${MIN_POSITIVE_VALUE}-${config.max_tracks_per_request}`;
            throw new ValidationError(`The size of track uris is not in the valid range of ${validRange}`)
        }
    }

    private isValidTrackUrisSize(trackUris: string[]) {
        return trackUris.length >=MIN_POSITIVE_VALUE && trackUris.length <= config.max_tracks_per_request;
    }
}

const api = new SpotifyAPIRequests();
export default api;
