import userConfig from '../user_config.json';
import logger, {loggingLevel} from './common/logger';
import { YouTubePlaylist } from './youtube/playlist';
import { SpotifyClient } from './spotify/client';

const UNSET_CONFIG_VALUE = "?"
const loggingConfig = userConfig.logging;
const youtubeConfig = userConfig.youtube;
const spotifyConfig = userConfig.spotify;

function isConfigValueSet(value: string): boolean {
    return value !== UNSET_CONFIG_VALUE;
}

async function getSpotifyPlaylistId(spotifyClient: SpotifyClient): Promise<string> {
    let playlistId: string = undefined;

    if (isConfigValueSet(spotifyConfig.playlist.existing_id)) {
        playlistId = spotifyConfig.playlist.existing_id;
        logger.info(`Using the pre-existing Spotify playlist id ${playlistId}`);
    } else {
        playlistId = await spotifyClient.createPlaylist(
            spotifyConfig.playlist.name, spotifyConfig.playlist.description, spotifyConfig.playlist.public
        );
        logger.info(`Using the newly-created Spotify playlist id ${playlistId}`)
    }

    return playlistId;
}

async function main() {
    logger.setLevel(loggingLevel[loggingConfig.level]);
    
    const youtubePlaylist = new YouTubePlaylist(youtubeConfig.api_key, youtubeConfig.playlist_id);
    const spotifyClient = await new SpotifyClient(spotifyConfig.access_token).setUserId();

    const playlistId = await getSpotifyPlaylistId(spotifyClient);

    for await (const titlesBatch of youtubePlaylist.titlesBatchGenerator(50)) {
        const snapshotId = await spotifyClient.addTracks(playlistId, titlesBatch);
        if (snapshotId) {
            logger.debug(`Spotify snapshot id of the new added tracks is ${snapshotId}`);
        }
    }
}

main();
