import userConfig from '../user_config.json';
import logger, {loggingLevel} from './common/logger';
import { YouTubePlaylist } from './youtube/playlist';
import { SpotifyClient } from './spotify/client';


const loggingConfig = userConfig.logging;
const youtubeConfig = userConfig.youtube;
const spotifyConfig = userConfig.spotify;

async function main() {
    logger.setLevel(loggingLevel[loggingConfig.level]);
    
    const youtubePlaylist = new YouTubePlaylist(youtubeConfig.api_key, youtubeConfig.playlist_id);
    const spotifyClient = await new SpotifyClient(spotifyConfig.access_token).setUserId();

    // In order to add to an existing playlist, set the playlist id variable instead of calling 'createPlaylist' method
    // const playlistId = "?";

    const playlistId = await spotifyClient.createPlaylist(
        spotifyConfig.playlist.name, spotifyConfig.playlist.description, spotifyConfig.playlist.public
    );

    for await (let titlesBatch of youtubePlaylist.titlesBatchGenerator(50)) {
        const snapshotId = await spotifyClient.addTracks(playlistId, titlesBatch);
        if (snapshotId) {
            logger.debug(`Spotify snapshot id of the new added tracks is ${snapshotId}`);
        }
    }
}

main();
