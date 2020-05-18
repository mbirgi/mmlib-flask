from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, StringField, DecimalField, IntegerField


class RefreshSpotifyForm(FlaskForm):
    refresh = SubmitField(label='Refresh', id='refresh')

class FilterAlbumsForm(FlaskForm):
    # tags_filter = SelectMultipleField('Tags')
    artist_filter = SelectMultipleField('Artists')
    filter_artists = SubmitField("Filter Artists")
    album_filter = SelectMultipleField('Albums')
    filter_albums = SubmitField("Filter Albums")
    reset_filters = SubmitField("Reset Filters")

class FilterLibraryForm(FlaskForm):
    tags_filter = SelectMultipleField('Tags', validate_choice=False)
    artist_filter = SelectMultipleField('Artists', validate_choice=False)
    album_filter = SelectMultipleField('Albums', validate_choice=False)
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
    # key = IntegerField("Key")
    # mode = SelectField(choices=['Any', 'Major', 'Minor'], validate_choice=False)
    # time_signature = IntegerField("Time Signature")

class EditTagsForm(FlaskForm):
    existing_tags = StringField('Existing Tags')
    new_tag = StringField('New Tag')
    save = SubmitField(label='Save', id='save')
    cancel = SubmitField(label='Cancel', id='cancel')
