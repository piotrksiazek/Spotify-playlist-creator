from flask import render_template, redirect, url_for, flash
import config
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from app.forms import OriginDestination, OriginDestination2, LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app import app
from app import models
from app import db
from app import scheduler
from main import create_new_playlist_from_not_mentioned_top_songs

# app = Flask(__name__, template_folder='templates')
# app.config.from_object(Config)
# bootstrap = Bootstrap(app)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# login = LoginManager(app)
# login.login_view = 'login'
# scheduler = APScheduler()

scope = config.scope
my_uri = config.my_uri
user = config.user
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


@app.before_first_request
def start_scheduler():
    scheduler.start()


@app.login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_object = models.User.query.filter_by(username=form.username.data).first()
        if user_object is None or not user_object.check_password(form.password.data):
            print('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user_object, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_object = models.User(username=form.username.data, email=form.email.data)
        user_object.set_password(form.password.data)
        db.session.add(user_object)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    form = OriginDestination()
    if form.validate_on_submit():
        original_playlist = form.origin_playlist.data
        destination_playlist = form.destination_playlist.data
        create_new_playlist_from_not_mentioned_top_songs(spotify, original_playlist, destination_playlist)
    return render_template('index.html', form=form)


@app.route('/MyPlaylists', methods=['GET', 'POST'])
@login_required
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
