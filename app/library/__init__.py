# import os
from .. import db
from ..models import Track, Artist, Album, Playlist

from .json_library import JSONLibrary
from .sql_library import SQLLibrary

# _dev = os.getenv('MMLIB_DEV_MODE')

lib = SQLLibrary()


class Library():
    def save_tracks(self, tracks):
        pass

    def update_saved_tracks(self, sp_tracks):
        for sp_track in sp_tracks:
            lib_track = Track.query.get(sp_track['id']) or self._make_db_track(sp_track)
            lib_track.is_saved_track = True
            db.session.add(lib_track)
        db.session.commit()

    def update_saved_albums(self, sp_albums):
        for sp_album in sp_albums:
            lib_album = Track.query.get(sp_album['id']) or self._make_db_album(sp_album)
            lib_album.is_saved_album = True
            db.session.add(lib_album)
        db.session.commit()

    def _make_db_track(self, sp_track):
        db_track = Track(
            id=sp_track['id'],
            name=sp_track['name'],
            duration_ms=sp_track['duration_ms'],
            track_number=sp_track['track_number'],
            danceability=sp_track.get('danceability'),
            energy=sp_track.get('energy'),
            key=sp_track.get('key'),
            loudness=sp_track.get('loudness'),
            mode=sp_track.get('mode'),
            speechiness=sp_track.get('speechiness'),
            acousticness=sp_track.get('acousticness'),
            instrumentalness=sp_track.get('instrumentalness'),
            liveness=sp_track.get('liveness'),
            valence=sp_track.get('valence'),
            tempo=sp_track.get('tempo'),
            time_signature=sp_track.get('time_signature'),
        )
        db.session.add(db_track)
        self._add_item_artists(db_track, sp_track['artists'])
        return db_track

    def _add_item_artists(self, item, artists):
        for artist in artists:
            item_artist = Artist.query.get(artist['id']) or self._make_db_artist(artist)
            item.artists.append(item_artist)

    def _add_item_tracks(self, item, tracks):
        for track in tracks:
            item_track = Track.query.get(track['id']) or self._make_db_track(track)
            item.tracks.append(item_track)

    def _make_db_artist(self, artist):
        db_artist = Artist(
            id=artist['id'],
            name=artist['name'],
        )
        db.session.add(db_artist)
        return db_artist

    def _make_db_album(self, sp_album):
        db_album = Album(
            id=sp_album['id'],
            name=sp_album['name'],
            total_tracks=sp_album['total_tracks']
        )
        db.session.add(db_album)
        self._add_item_artists(db_album, sp_album['artists'])
        self._add_item_tracks(db_album, sp_album['tracks'])
        return db_album
