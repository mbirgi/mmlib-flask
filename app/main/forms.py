from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, StringField, validators


class RefreshSpotifyForm(FlaskForm):
    refresh = SubmitField(label='Refresh', id='refresh')

class FilterLibraryForm(FlaskForm):
    tags_filter = SelectMultipleField('Tags', choices=[('foo', 'Foo'), ('bar', 'Bar')])
    artist_filter = SelectMultipleField('Artists', choices=[('foo', 'Foo'), ('bar', 'Bar')])
    album_filter = SelectMultipleField('Artists', choices=[('foo', 'Foo'), ('bar', 'Bar')])

class EditTagsForm(FlaskForm):
    existing_tags = StringField('Existing Tags')
    new_tag = StringField('New Tag')
    save = SubmitField(label='Save', id='save')
    cancel = SubmitField(label='Cancel', id='cancel')
