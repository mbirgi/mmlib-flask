from flask_wtf import FlaskForm
from wtforms import Label, SubmitField
from wtforms.validators import DataRequired


class RefreshSpotifyForm(FlaskForm):
    # label = Label(field_id='refresh', text='hello')
    refresh = SubmitField(label='Refresh', id='refresh')
