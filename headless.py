import spotipy
import sys
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

spotify_scope = "user-read-currently-playing"
# spotify_user = #open a file and get my spotify username

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=spotify_scope, redirect_uri="http://127.0.0.1:5000", cache_path=".spotifcache"))

# current_track = spotify.current_user_playing_track() #This causes the code to hang
# spotify_user = spotify.current_user()
# print(f"track: {current_track['item']['id']}", file=sys.stdout)
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")
total_mix_playlist_name = "Total Daily Mix"
total_mix_playlist_id = None
my_playlists = spotify.current_user_playlists()
for my_playlist in my_playlists['items']:
    if my_playlist['name'] == total_mix_playlist_name:
        spotify.current_user_unfollow_playlist(my_playlist['id'])
        # total_mix_playlist_id = my_playlist['id']
if not total_mix_playlist_id:
    total_mix_playlist = spotify.user_playlist_create(spotify.current_user()['id'], total_mix_playlist_name, False, False, "Generated Total Daily Mix")
    total_mix_playlist_id = total_mix_playlist['id']

playlists = spotify.search(q="Daily Mix", type="playlist", limit=50)
alltracks = []
for playlist in playlists['playlists']['items']:
    if playlist['owner']['id'] == 'spotify':
        print("Playlist Name:", playlist['name'], file=sys.stdout)
        offset = 0
        while True:
            response = spotify.playlist_items(playlist['id'], offset=offset, fields='items.track.id,items.track.uri,total', additional_types=['track'])
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

# songs_to_add = []
# for item in alltracks:
#     songs_to_add.append(item['track']['uri'])





# for i, item in enumerate(alltracks):
#     print("%d %s" % (i, item['track']['uri']))


# my_playlists = spotify.current_user_playlists()
# for my_playlist in enumerate(my_playlists['items']):
#     print("Playlist Name:", my_playlist[1]['name'], file=sys.stdout)
#     offset = 0
#     while True:
#         response = spotify.playlist_items(my_playlist[1]['id'], offset=offset, fields='items.track.id,total', additional_types=['track'])
#         if len(response['items']) == 0:
#             break
#         for item in response['items']:
#             print(f"track id: {item['track']['id']}")
#         offset = offset + len(response['items'])
#         print(offset, " of ", response['total'], file=sys.stdout)



playlist_names = [playlist['name'] for playlist in playlists['playlists']['items'] if playlist['owner']['id'] == 'spotify']
