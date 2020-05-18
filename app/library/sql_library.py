from ..models import Track
from .. import db

class SQLLibrary():
    def __init__(self):
        pass

    def refresh_from_spotify(self, spotify_library):
        self._write_saved_tracks(spotify_library['saved_tracks'])
        # self._update_saved_albums(spotify_library['saved_albums'])
        # self._update_saved_playlists(spotify_library['playlists'])
        # self._update_audio_features()
        # self._save_last_import_dt()

    def _write_saved_tracks(self, tracks):
        all_tracks = Track.query.all()
        new_tracks = []
        # for track in tracks:

