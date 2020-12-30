from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class OriginDestination(FlaskForm):
    origin_playlist = StringField('Origin', validators=[DataRequired()])
    destination_playlist = PasswordField('Destination', validators=[DataRequired()])
    submit = SubmitField('MAKE PLAYLIST BROOO')


class OriginDestination2(FlaskForm):
    origin_playlist = SelectField('Origin', choices=[], validators=[DataRequired()])
    destination_playlist = SelectField('Destination', choices=['abc', 'scd'], validators=[DataRequired()])
    submit = SubmitField('MAKE PLAYLIST BROOO')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    spotify_id = StringField('Spotify Id', validators=[DataRequired()])
    submit = SubmitField('Sign In')