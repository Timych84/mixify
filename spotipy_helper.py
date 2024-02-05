import os
from spotipy import cache_handler, oauth2, Spotify
from config import Config
from datetime import datetime

def create_spotify_auth_manager(session):
    return oauth2.SpotifyOAuth(
        scope=Config.SPOTIFY_API_SCOPES,
        cache_handler=cache_handler.FlaskSessionCacheHandler(session),
        show_dialog=True
    )


def get_spotify_client(auth_manager):
    return Spotify(auth_manager=auth_manager)


def validate_spotify_token(auth_manager):
    token_info = auth_manager.cache_handler.get_cached_token()
    if not auth_manager.validate_token(token_info):
        return redirect('/')
    return True


def get_currentuser_playlists(spotify, sort_by='name', ascending=True):
    playlists = []
    offset = 0
    limit = 50  # Maximum number of playlists to retrieve per request

    while True:
        response = spotify.current_user_playlists(limit=limit, offset=offset)

        if not response['items']:
            break  # No more playlists

        playlists.extend(response['items'])
        offset += limit
    playlists = sorted(playlists, key=lambda x: x[sort_by], reverse=not ascending)
    return playlists


def create_new_playlist(spotify, playlist_name, overwrite):
    user_playlists = get_currentuser_playlists(spotify, sort_by='name', ascending=True)
    existing_playlist = None
    for p in user_playlists:
        if p['name'] == playlist_name:
            existing_playlist = p
            break
    if existing_playlist:
        if overwrite == "on":
            spotify.current_user_unfollow_playlist(existing_playlist['id'])
        else:
            return False
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d.%m.%Y %H:%M:%S")
    spotify.user_playlist_create(spotify.current_user()['id'], playlist_name, False, False, f"Generated Total Daily Mix {formatted_datetime}")
    return True
