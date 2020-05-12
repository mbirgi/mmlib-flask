from flask import render_template, redirect, url_for

from . import main
from .forms import RefreshSpotifyForm
from .. import spotify
from ..library import library


@main.route('/', methods=['GET', 'POST'])
def index():
    form = RefreshSpotifyForm()
    if form.validate_on_submit():
        print("Button pressed")
        spotify_library = spotify.import_spotify_library()
        print(spotify_library)
        library.refresh_from_spotify(spotify_library)
        return redirect(url_for('.index'))
    return render_template('index.html', form=form)

@main.route('/saved_tracks', methods=['GET', 'POST'])
def saved_tracks_list():
    form = RefreshSpotifyForm()
    if form.validate_on_submit():
        print("Button pressed")
        spotify_library = spotify.import_spotify_library()
        print(spotify_library)
        library.refresh_from_spotify(spotify_library)
        return redirect(url_for('.index'))
    return render_template('saved_tracks_list.html', form=form, all_tracks=library.get_all_tracks())
