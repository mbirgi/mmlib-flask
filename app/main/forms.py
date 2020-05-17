from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, SubmitField, StringField, DecimalField, IntegerField


class RefreshSpotifyForm(FlaskForm):
    refresh = SubmitField(label='Refresh', id='refresh')

class FilterLibraryForm(FlaskForm):
    tags_filter = SelectMultipleField('Tags')
    artist_filter = SelectMultipleField('Artists')
    album_filter = SelectMultipleField('Albums')
    danceability_min = DecimalField()
    danceability_max = DecimalField()
    energy_min = DecimalField()
    energy_max = DecimalField()
    speechiness_min = DecimalField()
    speechiness_max = DecimalField()
    acousticness_min = DecimalField()
    acousticness_max = DecimalField()
    instrumentalness_min = DecimalField()
    instrumentalness_max = DecimalField()
    liveness_min = DecimalField()
    liveness_max = DecimalField()
    valence_min = DecimalField()
    valence_max = DecimalField()
    tempo_min = IntegerField()
    tempo_max = IntegerField()
    key = IntegerField("Key")
    mode = SelectField(choices=['Any', 'Major', 'Minor'])
    time_signature = IntegerField("Time Signature")

class EditTagsForm(FlaskForm):
    existing_tags = StringField('Existing Tags')
    new_tag = StringField('New Tag')
    save = SubmitField(label='Save', id='save')
    cancel = SubmitField(label='Cancel', id='cancel')
