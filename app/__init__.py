from flask import Flask
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import config
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_apscheduler import APScheduler

app = Flask(__name__) #, template_folder='templates'
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
scheduler = APScheduler()
login_manager = LoginManager(app)
login_manager.login_view = 'login'

scope = config.scope
my_uri = config.my_uri
user = config.user
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

from app import routes, models