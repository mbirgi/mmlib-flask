from .. import db
from ..models import Track, Artist, Album, Playlist
from .. import spotify


class SQLLibrary():
    def __init__(self):
        pass

    def refresh_from_spotify(self, spotify_library):
        self._update_saved_tracks(spotify_library['saved_tracks'])
        self._update_saved_albums(spotify_library['saved_albums'])
        self._update_saved_playlists(spotify_library['playlists'])
        # self._update_audio_features()
        # self._save_last_import_dt()
        db.session.commit()

    # def _update_audio_features(self):
    #     features = spotify.get_audio_features_for_tracks([track.id for track in Track.query.all()])
    #     for item in features:
    #         track = Track.query.get(item['id'])
    #         track.danceability = item.get('danceability')
    #         track.energy = item.get('energy')
    #         track.key = item.get('key')
    #         track.loudness = item.get('loudness')
    #         track.mode = item.get('mode')
    #         track.speechiness = item.get('speechiness')
    #         track.acousticness = item.get('acousticness')
    #         track.instrumentalness = item.get('instrumentalness')
    #         track.liveness = item.get('liveness')
    #         track.valence = item.get('valence')
    #         track.tempo = item.get('tempo')
    #         track.duration_ms = item.get('duration_ms')
    #         track.time_signature = item.get('time_signature')
    #         db.session.add(track)



    def _update_saved_albums(self, saved_albums):
        for album in saved_albums:
            self._write_saved_album(album)

    def _update_saved_playlists(self, saved_playlists):
        for playlist in saved_playlists:
            self._write_saved_playlist(playlist)

    def _update_saved_tracks(self, tracks):
        for track in tracks:
            self._write_saved_track(track)

    def _write_saved_album(self, saved_album):
        album = Album.query.get(saved_album['id']) or self._make_db_album(saved_album)
        if not album.is_saved_album:
            album.is_saved_album = True
            db.session.add(album)

    def _write_saved_playlist(self, saved_playlist):
        playlist = Playlist.query.get(saved_playlist['id']) or self._make_db_playlist(saved_playlist)
        if not playlist.is_saved_playlist:
            playlist.is_saved_playlist = True
            db.session.add(playlist)

    def _write_saved_track(self, saved_track):
        track = Track.query.get(saved_track['id']) or self._make_db_track(saved_track)
        if not track.is_saved_track:
            track.is_saved_track = True
            db.session.add(track)

    def _make_db_album(self, album):
        db_album = Album(
            id=album['id'],
            name=album['name'],
            total_tracks=album['total_tracks']
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

    def _make_db_playlist(self, playlist):
        db_playlist = Playlist(
            id=playlist['id'],
            name=playlist['name'],
            description=playlist['description'],
        )
        db.session.add(db_playlist)
        self._add_item_tracks(db_playlist, playlist['tracks'])
        return db_playlist

    def _make_db_track(self, track):
        db_track = Track(
            id=track['id'],
            name=track['name'],
            duration_ms=track['duration_ms'],
            track_number=track['track_number'],
            danceability=track.get('danceability'),
            energy=track.get('energy'),
            key=track.get('key'),
            loudness=track.get('loudness'),
            mode=track.get('mode'),
            speechiness=track.get('speechiness'),
            acousticness=track.get('acousticness'),
            instrumentalness=track.get('instrumentalness'),
            liveness=track.get('liveness'),
            valence=track.get('valence'),
            tempo=track.get('tempo'),
            time_signature=track.get('time_signature'),
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
