from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class TrackId(FlaskForm):
    track_id = StringField('Track ID', validators=[DataRequired()])
    submit = SubmitField('Get info')

class ArtistId(FlaskForm):
    artist_id = StringField('Artist ID', validators=[DataRequired()])
    submit = SubmitField('Get info')

class OriginDestination(FlaskForm):
    artist = StringField('Artist', validators=[DataRequired()])
    destination_playlist = SelectField('Playlist name', choices=[], validators=[DataRequired()])
    submit = SubmitField('Create')


class OriginDestination2(FlaskForm):
    origin_playlist = SelectField('Origin', choices=[])
    destination_playlist = SelectField('Destination', choices=['abc', 'scd'])
    submit = SubmitField('Go')


class CreateNewPlaylist(FlaskForm):
    playlist_name = StringField('Playlist name', validators=[DataRequired()])
    submit = SubmitField('Create')

class DeleteUserPlaylist(FlaskForm):
    user_playlist = SelectField('Playlist name', choices=[], validators=[DataRequired()])
    submit = SubmitField('Clear')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    spotify_id = StringField('Spotify Id', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')