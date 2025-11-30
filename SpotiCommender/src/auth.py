# autoryzacja w Spotify

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Ustaw swoje dane z dashboardu Spotify:
CLIENT_ID = "8e05b82a2284442491633fa07881cf98"
CLIENT_SECRET = "2ef037270856414f87093e23caf0578b"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "playlist-modify-public user-top-read"

def get_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))
    return sp
