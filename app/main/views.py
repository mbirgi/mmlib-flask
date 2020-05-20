import time

from flask import render_template, redirect, url_for, flash, session
import itertools

from . import main
from .forms import RefreshSpotifyForm, FilterLibraryForm, FilterAlbumsForm
from ..core import refresh_library


@main.route('/', methods=['GET', 'POST'])
def home():
    form = RefreshSpotifyForm()
    if form.validate_on_submit():
        print("refreshing spotify library")
        start = time.time()
        refresh_library()
        end = time.time()
        print("refresh duration (sec):", end - start)
        return redirect(url_for('.home'))
    # num_tracks = len(lib.get_saved_tracks())
    # num_albums = len(lib.get_saved_albums())
    # num_playlists = len(lib.get_saved_playlists())
    # num_lib_tracks = lib.get_total_tracks()
    context = {
        'form': form,
        # 'num_tracks': num_tracks,
        # 'num_albums': num_albums,
        # 'num_playlists': num_playlists,
        # 'num_lib_tracks': num_lib_tracks,
        # 'last_import': lib.get_last_import_dt()
    }
    return render_template('home.html', context=context)


@main.route('/library', methods=['GET', 'POST'])
def library():
    filter_library_form = FilterLibraryForm(
        danceability_min=0.0, danceability_max=1,
        energy_min=0, energy_max=1,
        speechiness_min=0, speechiness_max=1,
        acousticness_min=0, acousticness_max=1,
        instrumentalness_min=0, instrumentalness_max=1,
        liveness_min=0, liveness_max=1,
        valence_min=0, valence_max=1,
        tempo_min=110, tempo_max=120,
        # mode="Any"
    )
    filter_library_form.tags_filter.choices = lib.get_all_tags()
    artist_choices = sorted([(artist['id'], artist['name']) for artist in lib.get_all_artists()], key=lambda t: t[1])
    filter_library_form.artist_filter.choices = artist_choices
    album_choices = sorted([(album['id'], album['name']) for album in lib.get_all_albums()], key=lambda t: t[1])
    filter_library_form.album_filter.choices = album_choices
    print(f"ok? {filter_library_form.validate_on_submit()}")
    if filter_library_form.validate_on_submit():
        print("filtering library")
        print(f"tags: {filter_library_form.tags_filter.data}")
        print(f"artists: {filter_library_form.artist_filter.data}")
        print(f"albums: {filter_library_form.album_filter.data}")
        return redirect(url_for('.library'))
    elif filter_library_form.errors:
        flash(filter_library_form.errors)
    return render_template('library.html', filter_library_form=filter_library_form, selected_tracks=[])


@main.route('/saved_tracks', methods=['GET', 'POST'])
def saved_tracks():
    return render_template('saved_tracks.html', saved_tracks=lib.get_saved_tracks())


@main.route('/saved_albums', methods=['GET', 'POST'])
def saved_albums():
    form = FilterAlbumsForm()
    album_artists = list(itertools.chain.from_iterable([album['artists'] for album in lib.get_all_albums()]))
    form.artist_filter.choices = set(sorted([(artist['id'], artist['name']) for artist in album_artists], key=lambda t: t[1]))
    session['show_albums_filter'] = bool(session.get('sel_artist_ids'))
    # print("sel_artist_ids:", session.get('sel_artist_ids'))
    albums = lib.get_saved_albums_for_artists(artists=session.get('sel_artist_ids'))
    # print("albums:", albums)
    form.album_filter.choices = sorted([(album['id'], album['name']) for album in albums], key=lambda t: t[1])

    if form.validate_on_submit():
        if form.filter_artists.data:
            session['sel_artist_ids'] = form.artist_filter.data
        elif form.filter_albums.data:
            session['sel_album_ids'] = form.album_filter.data
        elif form.reset_filters.data:
            session['sel_artist_ids'] = []
            session['sel_album_ids'] = []
        return redirect(url_for('.saved_albums'))

    selected_albums = [album for album in albums if album['id'] in session.get('sel_album_ids', [])]
    return render_template('saved_albums.html', form=form,
                           debug_selected_artists=session.get('sel_artist_ids'),
                           debug_selected_albums=session.get('sel_album_ids'),
                           selected_albums=selected_albums,
                           show_albums_filter=session.get('show_albums_filter'))


@main.route('/saved_playlists', methods=['GET', 'POST'])
def saved_playlists():
    return render_template('saved_playlists.html', playlists=lib.get_saved_playlists())
