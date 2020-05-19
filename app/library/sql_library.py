from .. import db
from ..models import Track, Artist, Album


class SQLLibrary():
    def __init__(self):
        pass

    def refresh_from_spotify(self, spotify_library):
        self._update_saved_tracks(spotify_library['saved_tracks'])
        # self._update_saved_albums(spotify_library['saved_albums'])
        # self._update_saved_playlists(spotify_library['playlists'])
        # self._update_audio_features()
        # self._save_last_import_dt()
        db.session.commit()

    def _update_saved_albums(self, saved_albums):
        for album in saved_albums:
            self._write_saved_album(album)

    def _update_saved_tracks(self, tracks):
        for track in tracks:
            self._write_saved_track(track)

    def _write_saved_album(self, saved_album):
        if not Album.query.get(saved_album['id']):
            album = self._make_db_album(saved_album)
            db.session.add(album)

    def _write_saved_track(self, saved_track):
        track = Track.query.get(saved_track['id']) or self._make_db_track(saved_track)
        print(track)
        if not track.is_saved_track:
            track.is_saved_track = True
            db.session.add(track)

    def _make_db_album(self, album):
        db_album = Album(
            id=album['id'],
            name=album['name'],
            total_tracks=album['total_tracks'],
        )
        db.session.add(db_album)
        self._add_item_artists(db_album, album['artists'])
        self._add_item_tracks(db_album, album['tracks'])
        return db_album

    def _make_db_artist(self, artist):
        db_artist = Artist(
            id=artist['id'],
            name=artist['name'],
        )
        db.session.add(db_artist)
        return db_artist

    def _make_db_track(self, track):
        db_track = Track(
            id=track['id'],
            name=track['name'],
            duration_ms=track['duration_ms'],
            track_number=track['track_number']
        )
        db.session.add(db_track)
        self._add_item_artists(db_track, track['artists'])
        return db_track

    def _add_item_artists(self, item, artists):
        for artist in artists:
            item_artist = Artist.query.get(artist['id']) or self._make_db_artist(artist)
            item.artists.append(item_artist)

    def _add_item_tracks(self, item, tracks):
        for track in tracks:
            item_track = Track.query.get(track['id']) or self._make_db_track(track)
            item.tracks.append(item_track)

    # def _add_artists(self, artists):
    #     for artist in artists:
    #         if not Artist.query.get(artist['id']):
    #             new_artist = Artist(**artist)
    #             db.session.add(new_artist)

    # def _add_tracks(self, tracks):
    #     for track in tracks:
    #         if not Track.query.get(track['id']):
    #             new_track = self._make_db_track(track)
    #             db.session.add(new_track)
