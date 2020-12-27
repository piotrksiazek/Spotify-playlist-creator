from flask import Flask, render_template, redirect
import config
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from config import Config
from forms import OriginDestination, OriginDestination2

from Playlist import Playlist
from Track import Track

app = Flask(__name__)
app.config.from_object(Config)


scope = config.scope
# my_uri = config.my_uri
user = config.user
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
from main import create_new_playlist_from_not_mentioned_top_songs


@app.route('/', methods=['GET', 'POST'])
def home():
    form = OriginDestination()
    if form.validate_on_submit():
        original_playlist = form.origin_playlist.data
        destination_playlist = form.destination_playlist.data
        create_new_playlist_from_not_mentioned_top_songs(spotify, original_playlist, destination_playlist)
    return render_template('index.html', form=form)


@app.route('/MyPlaylists')
def my_playlists():
    # playlists = [(playlist['name'], playlist['id']) for playlist in spotify.user_playlists(user=user)['items']]
    playlists = [playlist['name'] for playlist in spotify.user_playlists(user=user)['items']]
    form = OriginDestination2()
    form.destination_playlist.choices = playlists
    form.origin_playlist.choices = playlists
    # form.category.choices = playlists
    return render_template('MyPlaylists.html', playlists=playlists, form=form)
if __name__ == '__main__':
    app.run(debug=True)
