from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, StringField, DecimalField, IntegerField

from .. import library as lib


class RefreshSpotifyForm(FlaskForm):
    refresh = SubmitField(label='Refresh', id='refresh')


class FilterAlbumsForm(FlaskForm):
    # tags_filter = SelectMultipleField('Tags')
    artist_filter = SelectMultipleField('Artists')
    filter_artists = SubmitField("Filter Artists")
    album_filter = SelectMultipleField('Albums')
    filter_albums = SubmitField("Filter Albums")
    reset_filters = SubmitField("Reset Filters")


class LibraryForm(FlaskForm):
    tags_filter = SelectMultipleField('Tags')
    artist_filter = SelectMultipleField('Artists')
    album_filter = SelectMultipleField('Albums')
    danceability_min = DecimalField(default=0)
    danceability_max = DecimalField(default=1)
    energy_min = DecimalField(default=0)
    energy_max = DecimalField(default=1)
    speechiness_min = DecimalField(default=0)
    speechiness_max = DecimalField(default=1)
    acousticness_min = DecimalField(default=0)
    acousticness_max = DecimalField(default=1)
    instrumentalness_min = DecimalField(default=0)
    instrumentalness_max = DecimalField(default=1)
    liveness_min = DecimalField(default=0)
    liveness_max = DecimalField(default=1)
    valence_min = DecimalField(default=0)
    valence_max = DecimalField(default=1)
    tempo_min = IntegerField(default=110)
    tempo_max = IntegerField(default=120)
    apply = SubmitField("Apply Filters")
    reset = SubmitField("Reset Filters")
    edit_tags = SubmitField("Edit Tags")
    save_playlist = SubmitField("Save as Playlist")

    def __init__(self):
        super().__init__()
        self.tags_filter.choices = lib.get_all_tags()
        artist_choices = sorted([(artist.id, artist.name) for artist in lib.get_all_artists()], key=lambda t: t[1])
        self.artist_filter.choices = artist_choices
        album_choices = sorted([(album.id, album.name) for album in lib.get_all_albums()], key=lambda t: t[1])
        self.album_filter.choices = album_choices


class EditTagsForm(FlaskForm):
    existing_tags = StringField('Existing Tags')
    new_tag = StringField('New Tag')
    save = SubmitField(label='Save', id='save')
    cancel = SubmitField(label='Cancel', id='cancel')
