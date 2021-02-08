import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


scope = "playlist-modify-public"
my_uri = 'spotify:playlist:1qBB4GjHyKZYnQclPJfNe0'
user='rbegouu2bjgv6t268sa2dc9hj'
