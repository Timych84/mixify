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
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return render_template('signin.html', auth_url=auth_url)
    authenticated = 'token_info' in session
    return render_template('index.html', authenticated=authenticated)


@app.route('/sign_out')
def sign_out():
    session.pop("token_info", None)
    return redirect('/')


@app.route('/recommendations')
def recommendations():
    return redirect('/')


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
        overwrite = request.form.get('overwrite')
        if playlist_name:
            try:
                total_mix_playlist_id = "therwillbeid"
                create_success = True
                # raise ValueError("Simulated error during playlist creation")
                return render_template('create_playlist.html', playlist_name=playlist_name, authenticated=authenticated, create_success=create_success, overwrite=overwrite)
            except Exception as e:
                create_success = False
                return render_template('create_playlist.html', playlist_name=playlist_name, authenticated=authenticated, create_success=create_success, overwrite=overwrite)
        else:
            return "Please provide a valid playlist name."
    return render_template('create_playlist.html', authenticated=authenticated)


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
