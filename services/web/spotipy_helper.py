import sys
import re
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
    limit = 50

    while True:
        response = spotify.current_user_playlists(limit=limit, offset=offset)

        if not response['items']:
            break

        playlists.extend(response['items'])
        offset += limit
    playlists = sorted(playlists, key=lambda x: x[sort_by], reverse=not ascending)
    return playlists


def get_daily_playlists(spotify):
    playlists = []
    offset = 0
    limit = 50
    total = None
    while True:
        response = spotify.search(q="Daily Mix", type="playlist", limit=limit, offset=offset)
        if total is None:
            total = response['playlists']['total']
        if not response['playlists']['items']:
            break
        items = response['playlists']['items']
        valid_items = [item for item in items if item is not None]
        if not valid_items:
            break
        playlists.extend(valid_items)
        offset += limit
        if offset >= total:
            break
    # for playlist in playlists:
    #     print(f"Playlist Name: {playlist['name']}, Owner: {playlist['owner']['display_name']}, Ownerid: {playlist['owner']['id']}", file=sys.stdout)

    pattern = re.compile(r'^Daily Mix [1-9]$')
    filtered_playlists = [playlist for playlist in playlists if playlist['owner']['id'] == 'spotify' and pattern.match(playlist['name'])]
    sorted_playlists = sorted(filtered_playlists, key=lambda x: x['name'].lower())

    return sorted_playlists

def create_new_playlist(spotify, playlist_name, overwrite):
    user_playlists = get_currentuser_playlists(spotify, sort_by='name', ascending=True)
    existing_playlist = None
    for p in user_playlists:
        if p['name'] == playlist_name:
            existing_playlist = p
            break
    if existing_playlist:
        # if overwrite == "on":
        if overwrite:
            spotify.current_user_unfollow_playlist(existing_playlist['id'])
        else:
            return False, None
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d.%m.%Y %H:%M:%S")
    created_playlist = spotify.user_playlist_create(spotify.current_user()['id'], playlist_name, False, False, f"Generated Total Daily Mix {formatted_datetime}")
    created_playlist_id = created_playlist['id']
    return True, created_playlist_id


def create_daily_mix_playlist(spotify, playlist_name, playlists_ids, overwrite):
    create_success, total_mix_playlist_id = create_new_playlist(spotify, playlist_name, overwrite)
    # total_mix_playlist_id = total_mix_playlist['id']
    if create_success:
        alltracks = []
        for playlist_id in playlists_ids:
            print("Playlist Name:", playlist_id, file=sys.stdout)
            offset = 0
            while True:
                response = spotify.playlist_items(playlist_id, offset=offset, fields='items.track.id,items.track.uri,total', additional_types=['track'])
                if len(response['items']) == 0:
                    break
                alltracks.extend(response['items'])
                songs_to_add = []
                for item in response['items']:
                    songs_to_add.append(item['track']['uri'])
                spotify.user_playlist_add_tracks(spotify.current_user()['id'], total_mix_playlist_id, songs_to_add)

                # for item in response['items']:
                #     print(f"track id: {item['track']['id']}")
                offset = offset + len(response['items'])
                print(offset, "/", response['total'], file=sys.stdout)
        return True
    else:
        return False
