import os
from spotipy import cache_handler, oauth2

def create_spotify_auth_manager(session):
    return oauth2.SpotifyOAuth(
        scope=os.environ.get("SPOTIFY_API_SCOPES"),
        cache_handler=cache_handler.FlaskSessionCacheHandler(session),
        show_dialog=True
    )

def get_spotify_client(auth_manager):
    return Spotify(auth_manager=auth_manager)
