import os
import json
import sys
import time
from flask import Flask, session, request, redirect, render_template, url_for, flash
from flask_session import Session
import spotipy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)


@app.route('/')
def index():

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope="playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-read-recently-played",
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return render_template('signin.html', auth_url=auth_url)
        # return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    # Step 3. Signed in, display data
    # spotify = spotipy.Spotify(auth_manager=auth_manager)
    authenticated = 'token_info' in session
    return render_template('index.html', authenticated=authenticated)
    # return f'<h2>Hi {spotify.me()["display_name"]}, ' \
    #        f'<small><a href="/sign_out">[sign out]<a/></small></h2>' \
    #        f'<a href="/playlists">my playlists</a> | ' \
    #        f'<a href="/currently_playing">currently playing</a> | ' \
    #        f'<a href="/test">test</a> | ' \
    #        f'<a href="/dmixes">dmixes</a> | ' \
    #     f'<a href="/current_user">me</a>' \



@app.route('/sign_out')
def sign_out():
    session.pop("token_info", None)
    return redirect('/')


@app.route('/recommendations')
def recommendations():
    return "recommendations"

# @app.route('/test')
# def test():
#     cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
#     auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
#     if not auth_manager.validate_token(cache_handler.get_cached_token()):
#         return redirect('/')
#     spotify = spotipy.Spotify(auth_manager=auth_manager)
#     playlists = spotify.search(q="Daily Mix", type="playlist")
#     # playlists = spotify.current_user_playlists()
#     for playlist in playlists['playlists']['items']:
#         if playlist['owner']['id'] == 'spotify':
#             print("Playlist Name:", playlist['name'], file=sys.stdout)
#             offset = 0
#             while True:
#                 response = spotify.playlist_items(playlist['id'], offset=offset, fields='items.track.id,total', additional_types=['track'])
#                 if len(response['items']) == 0:
#                     break
#                 print(response['items'], file=sys.stdout)
#                 offset = offset + len(response['items'])
#                 print(offset, "/", response['total'], file=sys.stdout)


#     playlist_names = [playlist['name'] for playlist in playlists['playlists']['items'] if playlist['owner']['id'] == 'spotify']
#     return render_template('playlists.html', playlist_names=playlist_names)

@app.route('/playlists')
def playlists():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    # current_user = spotify.current_user()
    # return spotify.current_user_playlists()
    return spotify.user_playlists(spotify.current_user()['id'])

@app.route('/daily_mix_generator')
def daily_mix_generator():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    # return spotify.current_user_playlists()
    # playlists = spotify.current_user_playlists()
    playlists = spotify.search(q="Daily Mix", type="playlist", limit=50)
    filtered_playlists = [playlist for playlist in playlists['playlists']['items'] if playlist['owner']['id'] == 'spotify']
    sorted_playlists = sorted(filtered_playlists, key=lambda x: x['name'].lower())
    return render_template('daily_mix_generator.html', playlists=sorted_playlists)


@app.route('/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    authenticated = 'token_info' in session
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    if request.method == 'POST':
        playlist_name = request.form.get('playlist_name')
        if playlist_name:
            try:
                total_mix_playlist_id = "therwillbeid"
                # raise ValueError("Simulated error during playlist creation")
                flash(f"Playlist '{playlist_name}' created successfully! Playlist ID: {total_mix_playlist_id}")
                return render_template('create_playlist.html', playlist_name=playlist_name, authenticated=authenticated)
                # return render_template('create_playlist_success.html', playlist_name=playlist_name)
            except Exception as e:
                # Flash an error message if an exception occurs (used for demonstration)
                flash(f"An error occurred: {str(e)}")
        else:
            return "Please provide a valid playlist name."
    return render_template('create_playlist.html', authenticated=authenticated)
# @app.route('/currently_playing')
# def currently_playing():
#     cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
#     auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
#     if not auth_manager.validate_token(cache_handler.get_cached_token()):
#         return redirect('/')
#     spotify = spotipy.Spotify(auth_manager=auth_manager)
#     track = spotify.current_user_playing_track()
#     if not track is None:
#         return track
#     return "No track currently playing."


@app.route('/current_user')
def current_user():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()


'''
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
'''
if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=int(os.environ.get("PORT", os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))
