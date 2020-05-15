from datetime import datetime

from flask import render_template, redirect, url_for

from . import main
from .forms import RefreshSpotifyForm, EditTagsForm, FilterLibraryForm
from .. import spotify
from ..library import library as lib


@main.route('/', methods=['GET', 'POST'])
def home():
    form = RefreshSpotifyForm()
    if form.validate_on_submit():
        print("Button pressed")
        spotify_library = spotify.import_spotify_library()
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
    filter_library_form = FilterLibraryForm()
    if filter_library_form.validate_on_submit():
        print("filtering library")
        print(f"tags: {filter_library_form.tags_filter.data}")
        print(f"artists: {filter_library_form.tags_filter.data}")
        print(f"albums: {filter_library_form.tags_filter.data}")
        return redirect(url_for('.library'))
    return render_template('library.html', library=lib.get_all()[:10], filter_library_form=filter_library_form)


@main.route('/saved_tracks', methods=['GET', 'POST'])
def saved_tracks():
    return render_template('saved_tracks.html', saved_tracks=lib.get_saved_tracks())


@main.route('/saved_albums', methods=['GET', 'POST'])
def saved_albums():
    return render_template('saved_albums.html', albums=lib.get_saved_albums())


@main.route('/saved_playlists', methods=['GET', 'POST'])
def saved_playlists():
    return render_template('saved_playlists.html', playlists=lib.get_saved_playlists())
