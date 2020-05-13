import json
import os
from datetime import datetime


class JSONLibrary():
    _data_folder = 'data'
    _db_files = {
        'saved_tracks': 'spotify_saved_tracks.json',
        'saved_albums': 'spotify_saved_albums.json',
        'saved_playlists': 'spotify_saved_playlists.json',
        'library': 'library.json',
        'admin': 'admin.json',
    }

    def __init__(self):
        self._init_files()
        self._library = self._load_items(self._db_files['library'])
        self._saved_tracks = self._load_items(self._db_files['saved_tracks'])
        self._saved_albums = self._load_items(self._db_files['saved_albums'])
        self._saved_playlists = self._load_items(self._db_files['saved_playlists'])
        self._admin = self._load_items(self._db_files['admin'])

    def get_last_import_dt(self):
        return datetime.fromisoformat(self._admin.get('last_import_dt', None))

    def _save_last_import_dt(self):
        self._admin['last_import_dt'] = datetime.utcnow().isoformat()
        self._save_items(self._admin, self._db_files['admin'])

    def get_all(self):
        return self._library

    def get_saved_tracks(self):
        return self._saved_tracks

    def get_saved_albums(self):
        return self._saved_albums

    def get_saved_playlists(self):
        return self._saved_playlists

    def _init_files(self):
        if not os.path.exists(self._data_folder):
            os.mkdir(self._data_folder)
        for file in self._db_files.values():
            if not os.path.exists(os.path.join(self._data_folder, file)):
                item = [] if file != self._db_files['admin'] else {}
                self._save_items(item, file)

    def _save_items(self, items, filename):
        with open(os.path.join(self._data_folder, filename), 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)

    def _load_items(self, filename):
        with open(os.path.join(self._data_folder, filename), 'r', encoding='utf-8') as f:
            return json.load(f)

    def refresh_from_spotify(self, spotify_library):
        self._update_saved_tracks(spotify_library['saved_tracks'])
        # self._update_saved_albums(spotify_library['saved_albums'])
        # self._update_saved_playlists(spotify_library['saved_playlists'])
        self._save_last_import_dt()

    def _update_saved_tracks(self, fetched_tracks):
        if not fetched_tracks: return
        # write fetched tracks to spotify tracks db:
        self._save_items(fetched_tracks, self._db_files['saved_tracks'])
        # update tracks in local library:
        fetched_track_ids = [track['id'] for track in fetched_tracks]
        library_saved_track_ids = [track['id'] for track in self._library if track['is_saved_track']]
        deletable_track_ids = [id for id in library_saved_track_ids if id not in fetched_track_ids]
        for id in deletable_track_ids:
            existing_track = next(track for track in self._library if track['id'] == id)
            existing_track['is_saved_track'] = False
        additional_track_ids = [id for id in fetched_track_ids if id not in library_saved_track_ids]
        for id in additional_track_ids:
            additional_track = next(track for track in fetched_tracks if track['id'] == id)
            additional_track['is_saved_track'] = True
            self._library.append(additional_track)
        self._save_items(self._library, self._db_files['library'])

    def _update_saved_albums(self, param):
        pass

    def _update_saved_playlists(self, param):
        pass
