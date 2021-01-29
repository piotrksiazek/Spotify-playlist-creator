from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class OriginDestination(FlaskForm):
    origin_playlist = StringField('Origin', validators=[DataRequired()])
    destination_playlist = PasswordField('Destination', validators=[DataRequired()])
    submit = SubmitField('MAKE PLAYLIST BROOO')


class OriginDestination2(FlaskForm):
    origin_playlist = SelectField('Origin', choices=[], validators=[DataRequired()])
    destination_playlist = SelectField('Destination', choices=['abc', 'scd'], validators=[DataRequired()])
    submit = SubmitField('Go')


class CreateNewPlaylist(FlaskForm):
    playlist_name = StringField('Playlist name', validators=[DataRequired()])
    submit = SubmitField('Create playlist')

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