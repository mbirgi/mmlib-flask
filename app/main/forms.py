from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SpotifyForm(FlaskForm):
    # name = StringField('What is your name?', validators=[DataRequired()])
    refresh_from_spotify = SubmitField('Refresh Spotify Library')
