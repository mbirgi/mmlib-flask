from app import db
from app.models import Track, Artist, Album, Playlist


def _add_item_artists(item, artists):
    for artist in artists:
        item_artist = Artist.query.get(artist['id']) or _make_db_artist(artist)
        item.artists.append(item_artist)


def _add_item_tracks(item, tracks):
    for track in tracks:
        item_track = Track.query.get(track['id']) or _make_db_track(track)
        item.tracks.append(item_track)


def _make_db_album(sp_album):
    db_album = Album(
        id=sp_album['id'],
        name=sp_album['name'],
        total_tracks=sp_album['total_tracks']
    )
    db.session.add(db_album)
    _add_item_artists(db_album, sp_album['artists'])
    _add_item_tracks(db_album, sp_album['tracks'])
    return db_album


def _make_db_artist(artist):
    db_artist = Artist(
        id=artist['id'],
        name=artist['name'],
    )
    db.session.add(db_artist)
    return db_artist


def _make_db_playlist(sp_playlist):
    db_playlist = Playlist(
        id=sp_playlist['id'],
        name=sp_playlist['name'],
        description=sp_playlist['description'],
    )
    db.session.add(db_playlist)
    _add_item_tracks(db_playlist, sp_playlist['tracks'])
    return db_playlist


def _make_db_track(sp_track):
    lib_track = Track()
    _update_lib_track(lib_track, sp_track)
    db.session.add(lib_track)
    _add_item_artists(lib_track, sp_track['artists'])
    return lib_track


def _update_lib_playlist(lib_playlist, sp_playlist):
    lib_playlist.id = sp_playlist['id']
    lib_playlist.name = sp_playlist['name']
    lib_playlist.description = sp_playlist['description']
    db.session.add(lib_playlist)
    lib_playlist.tracks = []
    _add_item_tracks(lib_playlist, sp_playlist['tracks'])
    return lib_playlist


def _update_lib_track(lib_track, sp_track):
    lib_track.id = sp_track['id']
    lib_track.name = sp_track['name']
    lib_track.duration_ms = sp_track['duration_ms']
    lib_track.track_number = sp_track['track_number']
    lib_track.danceability = sp_track.get('danceability')
    lib_track.energy = sp_track.get('energy')
    lib_track.key = sp_track.get('key')
    lib_track.loudness = sp_track.get('loudness')
    lib_track.mode = sp_track.get('mode')
    lib_track.speechiness = sp_track.get('speechiness')
    lib_track.acousticness = sp_track.get('acousticness')
    lib_track.instrumentalness = sp_track.get('instrumentalness')
    lib_track.liveness = sp_track.get('liveness')
    lib_track.valence = sp_track.get('valence')
    lib_track.tempo = sp_track.get('tempo')
    lib_track.time_signature = sp_track.get('time_signature')
    return lib_track


def save_tracks(sp_tracks):
    for sp_track in sp_tracks:
        lib_track = Track.query.get(sp_track['id'])
        if lib_track is None:
            lib_track = _make_db_track(sp_track)
        else:
            _update_lib_track(lib_track, sp_track)
        db.session.add(lib_track)
    db.session.commit()


def update_saved_albums(sp_albums):
    for sp_album in sp_albums:
        lib_album = Album.query.get(sp_album['id']) or _make_db_album(sp_album)
        lib_album.is_saved_album = True
        db.session.add(lib_album)
    db.session.commit()


def update_saved_playlists(sp_playlists):
    for sp_playlist in sp_playlists:
        lib_playlist = Playlist.query.get(sp_playlist['id'])
        if lib_playlist is None:
            lib_playlist = _make_db_playlist(sp_playlist)
        else:
            _update_lib_playlist(lib_playlist, sp_playlist)
        lib_playlist.is_saved_playlist = True
        db.session.add(lib_playlist)
    db.session.commit()


def update_saved_tracks(sp_tracks):
    for sp_track in sp_tracks:
        lib_track = Track.query.get(sp_track['id']) or _make_db_track(sp_track)
        lib_track.is_saved_track = True
        db.session.add(lib_track)
    db.session.commit()
