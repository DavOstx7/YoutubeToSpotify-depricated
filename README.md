# YoutubeToSpotify

Convert your favorite YouTube playlist to a Spotify playlist!

## Prerequisites

* <span style="color:#b2071d">YouTube API Key</span> - Follow the steps in the
  documentation [YouTube API][YouTubeAPILink]

---

* <span style="color:#b2071d">YouTube Playlist ID</span> - Go to your YouTube playlist, and the ID will appear in the
  url (.../playlist?list=`ID`)

---

* <span style="color:#1db954">Spotify Client ID & Secret</span> - Follow the steps in the
  documentation [Spotify API][SpotifyAPILink]

---

* <span style="color:#1db954">Spotify Access Token</span> (**Lasts 1 Hour**) - Choose either of two methods below
    1. Follow the steps in the documentation [Spotify Access Token][SpotifyTokenLink]
    2. Follow the steps in one of the scripts to receive the token
        1. [python/spotify/receive_token.py](python/spotify/receive_token.py)
        2. [typescript/spotify/receiveToken.ts](typescript/spotify/receiveToken.ts)

---

* <span style="color:#1db954">Spotify Playlist ID</span> (**Optional**) - Go to your Spotify playlist, and the ID will
  appear in the url (.../playlist/`ID`)

## Running Some Code

1. Fill in the values inside the [user_config.json](./user_config.json) file
2. Run the code in your preferred programming language
    1. **Python 3^6** - [main.py](python/main.py)
    2. **TypeScript** - [main.ts](typescript/main.ts)

[YouTubeAPILink]:https://developers.google.com/youtube/v3/getting-started

[SpotifyAPILink]:https://developer.spotify.com/documentation/web-api/concepts/apps

[SpotifyPytTokenLink]:https://developer.spotify.com/documentation/web-api/concepts/access-token 