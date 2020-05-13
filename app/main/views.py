from datetime import datetime

from flask import render_template, redirect, url_for

from . import main
from .forms import RefreshSpotifyForm
from .. import spotify
from ..library import library as lib


@main.route('/', methods=['GET', 'POST'])
def home():
    form = RefreshSpotifyForm()
    if form.validate_on_submit():
        print("Button pressed")
        spotify_library = spotify.import_spotify_library()
        print(spotify_library)
        library.refresh_from_spotify(spotify_library)
        return redirect(url_for('.home'))
    return render_template('home.html', form=form, current_time=datetime.utcnow())


@main.route('/library', methods=['GET', 'POST'])
def library():
    return render_template('library.html', library=lib.get_all())


@main.route('/saved_tracks', methods=['GET', 'POST'])
def saved_tracks():
    return render_template('saved_tracks.html', saved_tracks=lib.get_saved_tracks())


@main.route('/saved_albums', methods=['GET', 'POST'])
def saved_albums():
    return render_template('saved_albums.html', saved_albums=lib.get_saved_albums())


@main.route('/saved_playlists', methods=['GET', 'POST'])
def saved_playlists():
    return render_template('saved_playlists.html', saved_playlists=lib.get_saved_playlists())
