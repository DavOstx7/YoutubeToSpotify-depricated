from python.core.logger import logger
from python.youtube.playlist import YoutubePlaylist
from python.spotify.client import SpotifyClient
from python.core.user_config import YouTubeUserConfig, SpotifyUserConfig, LoggingUserConfig

logging_user = LoggingUserConfig()
youtube_user = YouTubeUserConfig()
spotify_user = SpotifyUserConfig()


def main():
    logger.setLevel(logging_user.level)

    youtube_playlist = YoutubePlaylist(youtube_user.api_key, youtube_user.playlist_id)
    spotify_client = SpotifyClient(spotify_user.access_token)

    # In order to add to an existing playlist, set the playlist id variable instead of calling 'create_playlist' method
    # playlist_id = "?"

    playlist_id = spotify_client.create_playlist(
        spotify_user.playlist_name, spotify_user.playlist_description, spotify_user.is_public_playlist
    )

    for titles_batch in youtube_playlist.titles_batch_iterator(size=100):
        snapshot_id = spotify_client.add_tracks(playlist_id, names=titles_batch)


if __name__ == "__main__":
    main()
