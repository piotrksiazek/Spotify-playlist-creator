from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class Origin_Destination(FlaskForm):
    origin_playlist = StringField('Origin', validators=[DataRequired()])
    destination_playlist = PasswordField('Destination', validators=[DataRequired()])