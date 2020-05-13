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
        lib.refresh_from_spotify(spotify_library)
        return redirect(url_for('.home'))
    num_tracks = len(lib.get_saved_tracks())
    num_albums = len(lib.get_saved_albums())
    num_playlists = len(lib.get_saved_playlists())
    context = {
        'form': form,
        'num_tracks': num_tracks,
        'num_albums': num_albums,
        'num_playlists': num_playlists,
        'last_import': lib.get_last_import_dt()
    }
    return render_template('home.html', context=context)


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
