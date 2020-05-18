import json
import os
from datetime import datetime

from .. import spotify
from ..utils import debug


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
        tags = []
        artists = []
        for track in self._library:
            t = track.get('tags')
            if t: tags.extend(t)
            artists.extend(track.get('artists'))
        self._library_tags = tags
        self._library_artists = artists
        self._saved_tracks = self._load_items(self._db_files['saved_tracks'])
        self._saved_albums = self._load_items(self._db_files['saved_albums'])
        self._saved_playlists = self._load_items(self._db_files['saved_playlists'])
        self._admin = self._load_items(self._db_files['admin'])

    def get_all_tags(self):
        return self._library_tags

    def get_all_artists(self):
        return self._library_artists

    def get_all_albums(self):
        return self._saved_albums

    def get_total_tracks(self):
        return len(self._library)

    def get_last_import_dt(self):
        dt = self._admin.get('last_import_dt', None)
        return datetime.fromisoformat(dt) if dt else None

    def _save_last_import_dt(self):
        self._admin['last_import_dt'] = datetime.utcnow().isoformat()
        self._save_items(self._admin, self._db_files['admin'])

    def get_all(self):
        return self._library

    def get_saved_tracks(self):
        return self._saved_tracks

    def get_saved_albums(self):
        return self._saved_albums

    def get_saved_albums_for_artists(self, artists):
        # artists is a list artist ids!
        albums_for_artists = []
        if artists:
            for album in self._saved_albums:
                for artist in album['artists']:
                    if artist['id'] in artists:
                        albums_for_artists.append(album)
        return albums_for_artists

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
        self._write_saved_tracks(spotify_library['saved_tracks'])
        self._update_saved_albums(spotify_library['saved_albums'])
        self._update_saved_playlists(spotify_library['playlists'])
        self._update_audio_features()
        self._save_last_import_dt()

    def _write_saved_tracks(self, tracks):
        """Writes saved tracks

        Writes several tracks to the saved tracks db file and to the
        corresponding local variable, and also updates the custom
        library accordingly.

        Args:
            tracks: a list of track objects
        """

        self._save_items(tracks, self._db_files['saved_tracks'])
        self._saved_tracks = tracks
        self._update_library_tracks(tracks)

    def _update_library_tracks(self, tracks):
        """Updates tracks in custom library

        Library tracks not in incoming track list are marked as "not part of saved tracks", but they are not
        deleted to preserve existing add-ons like tags.
        Incoming tracks not yet in library are added.
        Audio features are fetched and saved where missing.

        Args:
            tracks: a list of track objects
        """

        track_ids = [track['id'] for track in tracks]
        library_saved_track_ids = [track['id'] for track in self._library if track['is_saved_track']]
        deletable_track_ids = [id for id in library_saved_track_ids if id not in track_ids]
        for id in deletable_track_ids:
            existing_track = next(track for track in self._library if track['id'] == id)
            existing_track['is_saved_track'] = False
        additional_track_ids = [id for id in track_ids if id not in library_saved_track_ids]
        for id in additional_track_ids:
            additional_track = next(track for track in tracks if track['id'] == id)
            additional_track['is_saved_track'] = True
            self._library.append(additional_track)
        self._update_audio_features()
        self._save_items(self._library, self._db_files['library'])

    def _update_saved_albums(self, fetched_albums):
        if not fetched_albums: return
        debug("fetched_albums", fetched_albums[0])
        self._save_items(fetched_albums, self._db_files['saved_albums'])
        self._saved_albums = fetched_albums
        fetched_tracks = []
        for album in fetched_albums:
            fetched_tracks.extend([track for track in album['tracks']])
        self._update_library_tracks(fetched_tracks)

    def _update_saved_playlists(self, fetched_playlists):
        if not fetched_playlists: return
        debug("fetched_playlists", fetched_playlists[0])
        self._save_items(fetched_playlists, self._db_files['saved_playlists'])
        self._saved_playlists = fetched_playlists
        fetched_tracks = []
        for playlist in fetched_playlists:
            fetched_tracks.extend([track for track in playlist['tracks']])
        self._update_library_tracks(fetched_tracks)

    def save_track_tags(self, track_id, track_tags):
        track = next(track for track in self._library if track['id'] == track_id)
        track['tags'] = track_tags
        self._save_items(self._library, self._db_files['library'])

    def _update_audio_features(self):
        tracks = []
        for track in self._library:
            if not track.get('audio_features'):
                tracks.append(track)
        features = spotify.get_audio_features_for_tracks([track['id'] for track in tracks])
        debug("features", features[0])
        for f in features:
            id = list(f)[0]
            lib_track = next(track for track in self._library if track['id'] == id)
            lib_track['audio_features'] = f[id]
