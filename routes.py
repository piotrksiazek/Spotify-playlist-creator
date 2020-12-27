from flask import Flask, render_template, redirect
import config
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from config import Config
from forms import OriginDestination, OriginDestination2
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
scheduler = APScheduler()

scope = config.scope
my_uri = config.my_uri
user = config.user
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
from main import create_new_playlist_from_not_mentioned_top_songs

@app.before_first_request
def start_scheduler():
    scheduler.start()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))


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
        scheduler.add_job(id='scheduled_task',
                          func=lambda : create_new_playlist_from_not_mentioned_top_songs(spotify, playlists_dict[form.origin_playlist.data],
                                                                                         playlists_dict[form.destination_playlist.data]), trigger='interval', seconds=8)
        # create_new_playlist_from_not_mentioned_top_songs(spotify, playlists_dict[form.origin_playlist.data], playlists_dict[form.destination_playlist.data])
    return render_template('MyPlaylists.html', playlists=playlists_names, form=form)


if __name__ == '__main__':
    app.run(debug=True)
