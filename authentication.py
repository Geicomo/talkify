import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = '141ac1cdc293449f93c854636e1619e1'
SPOTIPY_CLIENT_SECRET = 'dccd1190076045918165792c6f82efef'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-modify-playback-state user-read-playback-state',
                                               cache_path='token_cache'))

# This will prompt for authentication and save the token in 'token_cache'
