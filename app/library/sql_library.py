from .. import db
from ..models import Track, Artist


class SQLLibrary():
    def __init__(self):
        pass

    def refresh_from_spotify(self, spotify_library):
        for track in spotify_library['saved_tracks']:
            self._write_saved_track(track)
        # self._update_saved_albums(spotify_library['saved_albums'])
        # self._update_saved_playlists(spotify_library['playlists'])
        # self._update_audio_features()
        # self._save_last_import_dt()
        db.session.commit()

    def _write_saved_track(self, saved_track):
        for artist in saved_track['artists']:
            if not Artist.query.get(artist['id']):
                new_artist = Artist(**artist)
                db.session.add(new_artist)
        track = Track.query.get(saved_track['id']) or self._make_db_track(saved_track)
        track.is_saved_track = True
        db.session.add(track)

    def _make_db_track(self, track):
        return Track(
            id=track['id'],
            name=track['name'],
            duration_ms=track['duration_ms']
        )
