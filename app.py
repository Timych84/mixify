import os
from flask import Flask, session, request, render_template, redirect
from flask_session import Session
from spotipy_helper import create_spotify_auth_manager, get_spotify_client, get_currentuser_playlists, create_new_playlist
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
Session(app)

@app.route('/')
def index():
    auth_manager = create_spotify_auth_manager(session)
    if request.args.get("code"):
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')
    if not auth_manager.validate_token(auth_manager.cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return render_template('signin.html', auth_url=auth_url)
    return render_template('index.html')

@app.route('/sign_out')
def sign_out():
    session.pop("token_info", None)
    return redirect('/')

@app.route('/recommendations')
def recommendations():
    return redirect('/')

@app.route('/myplaylists')
def myplaylists():
    auth_manager = create_spotify_auth_manager(session)
    if not auth_manager.validate_token(auth_manager.cache_handler.get_cached_token()):
        return redirect('/')
    spotify = get_spotify_client(auth_manager)
    user_playlists = get_currentuser_playlists(spotify, sort_by='name', ascending=True)
    return render_template('my_playlists.html', user_playlists=user_playlists)

@app.route('/daily_mix_generator')
def daily_mix_generator():
    auth_manager = create_spotify_auth_manager(session)
    if not auth_manager.validate_token(auth_manager.cache_handler.get_cached_token()):
        return redirect('/')
    spotify = get_spotify_client(auth_manager)
    playlists = spotify.search(q="Daily Mix", type="playlist", limit=50)
    filtered_playlists = [playlist for playlist in playlists['playlists']['items'] if playlist['owner']['id'] == 'spotify']
    sorted_playlists = sorted(filtered_playlists, key=lambda x: x['name'].lower())
    return render_template('daily_mix_generator.html', playlists=sorted_playlists)

@app.route('/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    auth_manager = create_spotify_auth_manager(session)
    if not auth_manager.validate_token(auth_manager.cache_handler.get_cached_token()):
        return redirect('/')
    if request.method == 'POST':
        playlist_name = request.form.get('playlist_name')
        overwrite = request.form.get('overwrite')
        if playlist_name:
            try:
                total_mix_playlist_id = "therewillbeid"  # Replace with appropriate logic
                spotify = get_spotify_client(auth_manager)
                create_success = create_new_playlist(spotify, playlist_name, overwrite)
                return render_template('create_playlist.html', playlist_name=playlist_name, create_success=create_success, overwrite=overwrite)
            except Exception as e:
                create_success = False
                return render_template('create_playlist.html', playlist_name=playlist_name, create_success=create_success, overwrite=overwrite)
        else:
            return "Please provide a valid playlist name."
    return render_template('create_playlist.html')

@app.route('/current_user')
def current_user():
    auth_manager = create_spotify_auth_manager(session)
    if not auth_manager.validate_token(auth_manager.cache_handler.get_cached_token()):
        return redirect('/')
    spotify = get_spotify_client(auth_manager)
    return spotify.current_user()

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=int(os.environ.get("PORT", 8080)))
