from python.core.logger import logger
from python.youtube.playlist import YoutubePlaylist
from python.spotify.client import SpotifyClient
from python.core.user_config import YouTubeUserConfig, SpotifyUserConfig, LoggingUserConfig

logging_config = LoggingUserConfig()
youtube_config = YouTubeUserConfig()
spotify_config = SpotifyUserConfig()


def main():
    logger.setLevel(logging_config.level)

    youtube_playlist = YoutubePlaylist(youtube_config.api_key, youtube_config.playlist_id)
    spotify_client = SpotifyClient(spotify_config.access_token)

    # In order to add to an existing playlist, set the playlist id variable instead of calling 'create_playlist' method
    # playlist_id = "?"

    playlist_id = spotify_client.create_playlist(
        spotify_config.playlist_name, spotify_config.playlist_description, spotify_config.is_public_playlist
    )

    for titles_batch in youtube_playlist.titles_batch_generator(max_batch_size=50):
        snapshot_id = spotify_client.add_tracks(playlist_id, titles_batch)
        if snapshot_id:
            logger.debug(f"Spotify snapshot id of the new added tracks is {snapshot_id}")


if __name__ == "__main__":
    main()
