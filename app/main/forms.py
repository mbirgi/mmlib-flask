from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, validators


class RefreshSpotifyForm(FlaskForm):
    refresh = SubmitField(label='Refresh', id='refresh')


class EditTagsForm(FlaskForm):
    existing_tags = StringField('Existing Tags')
    new_tag = StringField('New Tag')
    save = SubmitField(label='Save', id='save')
    cancel = SubmitField(label='Cancel', id='cancel')
