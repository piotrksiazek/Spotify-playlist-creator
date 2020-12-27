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


@app.route('/MyPlaylists', methods=['GET', 'POST'])
def my_playlists():
    # playlists = [(playlist['name'], playlist['id']) for playlist in spotify.user_playlists(user=user)['items']]
    playlists_dict = {}
    for playlist in spotify.user_playlists(user=user)['items']:
        playlists_dict[playlist['name']] = playlist['id']
    playlists_names = [name for name, name_id in playlists_dict.items()]
    form = OriginDestination2()
    form.destination_playlist.choices = playlists_names
    form.origin_playlist.choices = playlists_names

    if form.validate_on_submit():
        create_new_playlist_from_not_mentioned_top_songs(spotify, playlists_dict[form.origin_playlist.data], playlists_dict[form.destination_playlist.data])
    return render_template('MyPlaylists.html', playlists=playlists_names, form=form)


if __name__ == '__main__':
    app.run(debug=True)
