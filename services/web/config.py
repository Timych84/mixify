import os


class Config:
    SECRET_KEY = os.urandom(64)
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = './.flask_session/'
    SPOTIFY_API_SCOPES = "playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-read-recently-played"
    HOST = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    PORT = int(os.environ.get("FLASK_RUN_PORT", 5000))
