from python.core.logger import logger
from python.youtube.playlist import YoutubePlaylist
from python.spotify.client import SpotifyClient
from python.config.user import YouTubeUserConfig, SpotifyUserConfig, LoggingUserConfig

logging_config = LoggingUserConfig()
youtube_config = YouTubeUserConfig()
spotify_config = SpotifyUserConfig()


def get_spotify_playlist_id(spotify_client: SpotifyClient) -> str:
    if spotify_config.is_existing_playlist_id_set:
        playlist_id = spotify_config.existing_playlist_id
        logger.info(f"Using the pre-existing Spotify playlist id of {playlist_id}")
    else:
        playlist_id = spotify_client.create_playlist(
            spotify_config.playlist_name, spotify_config.playlist_description, spotify_config.is_public_playlist
        )
        logger.info(f"Using the newly-created Spotify playlist id {playlist_id}")
    return playlist_id


def main():
    logger.setLevel(logging_config.level)

    youtube_playlist = YoutubePlaylist(youtube_config.api_key, youtube_config.playlist_id)
    spotify_client = SpotifyClient(spotify_config.access_token)

    playlist_id = get_spotify_playlist_id(spotify_client)

    for titles_batch in youtube_playlist.titles_batch_generator(max_batch_size=50):
        snapshot_id = spotify_client.add_tracks(playlist_id, titles_batch)
        if snapshot_id:
            logger.debug(f"Spotify snapshot id of the new added tracks is {snapshot_id}")


if __name__ == "__main__":
    main()
