from .. import db
from ..models import Track, Artist, Album, Playlist


class SQLLibrary():
    def __init__(self):
        pass

    def save_tracks(self, sp_tracks):
        for sp_track in sp_tracks:
            lib_track = Track.query.get(sp_track['id'])
            if lib_track is None:
                lib_track = self._make_db_track(sp_track)
            else:
                self._update_lib_track(lib_track, sp_track)
            db.session.add(lib_track)
        db.session.commit()

    def update_saved_tracks(self, sp_tracks):
        for sp_track in sp_tracks:
            lib_track = Track.query.get(sp_track['id']) or self._make_db_track(sp_track)
            lib_track.is_saved_track = True
            db.session.add(lib_track)
        db.session.commit()

    def update_saved_albums(self, sp_albums):
        for sp_album in sp_albums:
            lib_album = Album.query.get(sp_album['id']) or self._make_db_album(sp_album)
            lib_album.is_saved_album = True
            db.session.add(lib_album)
        db.session.commit()

    def _update_lib_track(self, lib_track, sp_track):
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

    def _make_db_track(self, sp_track):
        lib_track = Track()
        self._update_lib_track(lib_track, sp_track)
        db.session.add(lib_track)
        self._add_item_artists(lib_track, sp_track['artists'])
        return lib_track

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

    def _make_db_playlist(self, playlist):
        db_playlist = Playlist(
            id=playlist['id'],
            name=playlist['name'],
            description=playlist['description'],
        )
        db.session.add(db_playlist)
        self._add_item_tracks(db_playlist, playlist['tracks'])
        return db_playlist


    # def _update_saved_playlists(self, saved_playlists):
    #     for playlist in saved_playlists:
    #         self._write_saved_playlist(playlist)
    #
    # def _write_saved_playlist(self, saved_playlist):
    #     playlist = Playlist.query.get(saved_playlist['id']) or self._make_db_playlist(saved_playlist)
    #     if not playlist.is_saved_playlist:
    #         playlist.is_saved_playlist = True
    #         db.session.add(playlist)
    #
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
