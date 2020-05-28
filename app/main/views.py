import itertools

from flask import current_app as app
from flask import render_template, redirect, url_for, flash, session

from . import main
from .forms import RefreshSpotifyForm, library_form_builder, FilterAlbumsForm
from .. import core
from .. import library as lib


@main.route('/', methods=['GET', 'POST'])
def home():
    form = RefreshSpotifyForm()
    if form.validate_on_submit():
        print("refreshing spotify library")
        core.refresh_library()
        return redirect(url_for('.home'))
    num_tracks = lib.get_saved_tracks_count()
    num_albums = lib.get_saved_albums_count()
    num_playlists = lib.get_saved_playlists_count()
    num_lib_tracks = lib.get_total_tracks_count()
    context = {
        'form': form,
        'num_tracks': num_tracks,
        'num_albums': num_albums,
        'num_playlists': num_playlists,
        'num_lib_tracks': num_lib_tracks,
        'last_import': lib.get_last_import_dt()
    }
    return render_template('home.html', context=context)


@main.route('/library', methods=['GET', 'POST'])
def library():
    library_form = library_form_builder([])

    if library_form.validate_on_submit():
        if library_form.apply.data:
            app.logger.debug("button: apply filters")
            app.logger.debug(f"tags_filter_data: {library_form.tags_filter.data}")
            app.logger.debug(f"artist_filter_data: {library_form.artist_filter.data}")
            app.logger.debug(f"album_filter_data: {library_form.album_filter.data}")
            session['tags_filter_data'] = library_form.tags_filter.data
            session['artist_filter_data'] = library_form.artist_filter.data
            session['album_filter_data'] = library_form.album_filter.data
            filtered_track_ids = lib.get_filtered_track_ids(
                tags_filter=session.get('tags_filter_data') if session.get('tags_filter_data') else [],
                artist_filter=session.get('artist_filter_data') if session.get('artist_filter_data') else [],
                album_filter=session.get('album_filter_data') if session.get('album_filter_data') else []
            )
            app.logger.debug(f'filtered_track_ids: {filtered_track_ids}')
            session['filtered_track_ids'] = filtered_track_ids
            session['selected_track_ids'] = []
            return redirect(url_for('.library'))
        if library_form.reset.data:
            app.logger.debug("button: reset filters")
            del session['filtered_track_ids']
            del session['selected_track_ids']
            del session['tags_filter_data']
            del session['artist_filter_data']
            del session['album_filter_data']
            return redirect(url_for('.library'))
        if library_form.edit_tags.data:
            app.logger.debug(f"button: edit tags")
        if library_form.save_playlist.data:
            app.logger.debug(f"button: save playlist")
        if library_form.select_all.data:
            app.logger.debug(f"button: select all tracks")
            session['selected_track_ids'] = session.get('filtered_track_ids')
        if library_form.unselect_all.data:
            app.logger.debug(f"button: unselect all tracks")
            session['selected_track_ids'] = []

    elif library_form.errors:
        flash(library_form.errors)

    filtered_track_ids = session.get('filtered_track_ids')
    selected_track_ids = session.get('selected_track_ids')
    app.logger.debug(f"session['filtered_track_ids']: {filtered_track_ids}")
    app.logger.debug(f"session['selected_track_ids']: {selected_track_ids}")
    if filtered_track_ids:
        filtered_tracks = lib.get_tracks(track_ids=filtered_track_ids)
    else:
        filtered_tracks = []
    app.logger.debug(f"filtered_tracks: {filtered_tracks}")
    library_form = library_form_builder(filtered_tracks)
    library_form.tags_filter.data = session.get('tags_filter_data')
    library_form.artist_filter.data = session.get('artist_filter_data')
    library_form.album_filter.data = session.get('album_filter_data')
    if selected_track_ids:
        for track_id in selected_track_ids:
            try:
                attr = getattr(library_form, track_id)
                attr.data = True
                app.logger.debug(f"attr: {attr}")
            except:
                pass
    return render_template('library.html', library_form=library_form,
                           filtered_tracks=filtered_tracks)


@main.route('/saved_tracks', methods=['GET', 'POST'])
def saved_tracks():
    return render_template('saved_tracks.html', saved_tracks=lib.get_saved_tracks())


@main.route('/saved_albums', methods=['GET', 'POST'])
def saved_albums():
    form = FilterAlbumsForm()
    selected_albums = lib.get_saved_albums()
    # album_artists = list(itertools.chain.from_iterable([album.artists for album in lib.get_all_albums()]))
    # form.artist_filter.choices = set(
    #     sorted([(artist['id'], artist['name']) for artist in album_artists], key=lambda t: t[1]))
    # session['show_albums_filter'] = bool(session.get('sel_artist_ids'))
    # # print("sel_artist_ids:", session.get('sel_artist_ids'))
    # albums = lib.get_saved_albums_for_artists(artists=session.get('sel_artist_ids'))
    # # print("albums:", albums)
    # form.album_filter.choices = sorted([(album['id'], album['name']) for album in albums], key=lambda t: t[1])
    #
    # if form.validate_on_submit():
    #     if form.filter_artists.data:
    #         session['sel_artist_ids'] = form.artist_filter.data
    #     elif form.filter_albums.data:
    #         session['sel_album_ids'] = form.album_filter.data
    #     elif form.reset_filters.data:
    #         session['sel_artist_ids'] = []
    #         session['sel_album_ids'] = []
    #     return redirect(url_for('.saved_albums'))
    #
    # selected_albums = [album for album in albums if album['id'] in session.get('sel_album_ids', [])]
    return render_template('saved_albums.html', form=form,
                           # debug_selected_artists=session.get('sel_artist_ids'),
                           # debug_selected_albums=session.get('sel_album_ids'),
                           selected_albums=selected_albums,
                           show_albums_filter=session.get('show_albums_filter'))


@main.route('/saved_playlists', methods=['GET', 'POST'])
def saved_playlists():
    return render_template('saved_playlists.html', playlists=lib.get_saved_playlists())

# def _init_library_filters():
#     library_filters = FilterLibraryForm(
#         danceability_min=0.0, danceability_max=1,
#         energy_min=0, energy_max=1,
#         speechiness_min=0, speechiness_max=1,
#         acousticness_min=0, acousticness_max=1,
#         instrumentalness_min=0, instrumentalness_max=1,
#         liveness_min=0, liveness_max=1,
#         valence_min=0, valence_max=1,
#         tempo_min=110, tempo_max=120,
#     )
#     library_filters.tags_filter.choices = lib.get_all_tags()
#     artist_choices = sorted([(artist.id, artist.name) for artist in lib.get_all_artists()], key=lambda t: t[1])
#     library_filters.artist_filter.choices = artist_choices
#     album_choices = sorted([(album.id, album.name) for album in lib.get_all_albums()], key=lambda t: t[1])
#     library_filters.album_filter.choices = album_choices
#     return library_filters
