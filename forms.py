from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class OriginDestination(FlaskForm):
    origin_playlist = StringField('Origin', validators=[DataRequired()])
    destination_playlist = PasswordField('Destination', validators=[DataRequired()])
    submit = SubmitField('MAKE PLAYLIST BROOO')

class OriginDestination2(FlaskForm):
    origin_playlist = SelectField('Origin', choices=[])
    destination_playlist = SelectField('Destination', choices=['abc', 'scd'])
    submit = SubmitField('MAKE PLAYLIST BROOO')