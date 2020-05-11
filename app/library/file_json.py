import json
import os


class JSONLibrary():
    DATA_FOLDER = 'data'
    SPOTIFY_SAVED_TRACKS_DB = 'spotify_saved_tracks.json'
    SPOTIFY_SAVED_ALBUMS_DB = 'spotify_saved_albums.json'
    SPOTIFY_SAVED_PLAYLISTS_DB = 'spotify_saved_playlists.json'
    LIBRARY_DB = 'library.json'

    def __init__(self):
        self._init_files()
        self.library = self._load_items(self.LIBRARY_DB)
        self.saved_tracks = self._load_items(self.SPOTIFY_SAVED_TRACKS_DB)
        self.saved_albums = self._load_items(self.SPOTIFY_SAVED_ALBUMS_DB)
        self.saved_playlists = self._load_items(self.SPOTIFY_SAVED_PLAYLISTS_DB)

    def _update_saved_tracks(self, fetched_tracks):
        if not fetched_tracks: return
        # write fetched tracks to spotify tracks db:
        self._save_items(fetched_tracks, self.SPOTIFY_SAVED_TRACKS_DB)
        # update tracks in local library:
        fetched_track_ids = [track['id'] for track in fetched_tracks]
        library_saved_track_ids = [track['id'] for track in self.library if track['is_saved_track']]
        deletable_track_ids = [id for id in library_saved_track_ids if id not in fetched_track_ids]
        for id in deletable_track_ids:
            existing_track = next(track for track in self.library if track['id'] == id)
            existing_track['is_saved_track'] = False
        additional_track_ids = [id for id in fetched_track_ids if id not in library_saved_track_ids]
        for id in additional_track_ids:
            additional_track = next(track for track in fetched_tracks if track['id'] == id)
            additional_track['is_saved_track'] = True
            self.library.append(additional_track)
        self._save_items(self.library, self.LIBRARY_DB)
        # for fetched_track in fetched_tracks:
        #     existing_track = next((track for track in library if track['id'] == fetched_track['id']))
        #     if existing_track and existing_track.is_saved_track == False:
        #         existing_track.is_saved_track = True
        #     else:
        #         fetched_track['is_saved_track'] = True
        #         library
        #
        # # check for existing saved tracks that are no more in the spotify library

    def _init_files(self):
        if not os.path.exists(self.DATA_FOLDER):
            os.mkdir(self.DATA_FOLDER)
        for file in [self.SPOTIFY_SAVED_TRACKS_DB,
                     self.SPOTIFY_SAVED_ALBUMS_DB,
                     self.SPOTIFY_SAVED_PLAYLISTS_DB,
                     self.LIBRARY_DB]:
            if not os.path.exists(os.path.join(self.DATA_FOLDER, file)):
                self._save_items([], file)

    def _save_items(self, items, filename):
        with open(os.path.join(self.DATA_FOLDER, filename), 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)

    def _load_items(self, filename):
        with open(os.path.join(self.DATA_FOLDER, filename), 'r', encoding='utf-8') as f:
            return json.load(f)

    def refresh_from_spotify(self, spotify_library):
        self._update_saved_tracks(spotify_library['saved_tracks'])
        # _update_saved_albums(spotify_library['saved_albums'])
        # update saved albums
        # update playlists
        # delete no more needed tracks
        # get audio features for new tracks



#     existing_tracks = Track.query.filter_by(is_saved_track=True).all()
#     deleted_tracks = [track for track in existing_tracks if track not in fetched_tracks]
#     for track in deleted_tracks:
#         track.is_saved_track = False
#         db.session.add(track)
#     # add tracks not already in the library
#     for fetched_track in fetched_tracks:
#         existing_track = next((track for track in existing_tracks if track.id == fetched_track['id']), None)
#         if existing_track and existing_track.is_saved_track == False:
#             existing_track.is_saved_track = True
#         else:
#             new_track = Track(
#                 id=fetched_track['id'],
#                 name=fetched_track['name'],
#                 is_saved_track=True,
#                 duration_ms=fetched_track['duration_ms'],
#                 artists=[]
#             )
#             print(f"new track: {new_track}")
#             db.session.add(new_track)
#             for artist in fetched_track['artists']:
#                 # check if artist exists:
#                 existing_artist = Artist.query.get(artist['id'])
#                 if not existing_artist:
#                     new_artist = Artist(
#                         id=artist['id'],
#                         name=artist['name']
#                     )
#                     print(f"new artist: {new_artist}")
#                     db.session.add(new_artist)
#                     new_track.artists.append(new_artist)
#         db.session.commit()


# def _update_saved_albums(fetched_albums):
#     if not fetched_albums: return
#     # check for existing saved albums that are no more in the spotify library
#     existing_albums = Album.query.filter_by(is_saved_album=True).all()
#     deleted_albums = [album for album in existing_albums if album not in fetched_albums]
#     for album in deleted_albums:
#         album.is_saved_album = False
#         db.session.add(album)
#     # add albums not already in the library
#     for fetched_album in fetched_albums:
#         existing_album = next((album for album in existing_albums if album.id == fetched_album['id']), None)
#         if existing_album and existing_album.is_saved_album == False:
#             existing_album.is_saved_album = True
#         else:
#             new_album = Track(
#                 id=fetched_album['id'],
#                 name=fetched_album['name'],
#                 is_saved_album=True,
#                 artists=[]
#             )
#             print(f"new album: {new_album}")
#             db.session.add(new_album)
#             for artist in fetched_album['artists']:
#                 # check if artist exists:
#                 existing_artist = Artist.query.get(artist['id'])
#                 if not existing_artist:
#                     new_artist = Artist(
#                         id=artist['id'],
#                         name=artist['name']
#                     )
#                     print(f"new artist: {new_artist}")
#                     db.session.add(new_artist)
#                     new_album.artists.append(new_artist)
#             for track in fetched_album['tracks']:
#                 # check if track exists:
#                 existing_track = Artist.query.get(track['id'])
#                 if not existing_track:
#                     new_track = Track(
#                         id=track['id'],
#                         name=track['name'],
#                         duration_ms = track['duration_ms'],
#                         artists = []
#                     )
#                     print(f"new track: {new_track}")
#                     db.session.add(new_track)
#                     new_album.tracks.append(new_track)
#                     for artist in track['artists']:
#                         # check if artist exists or if it was already added to the session:
#                         existing_artist = Artist.query.get(artist['id'])
#                         if not existing_artist:
#                             existing_artist = db.session.query.get(artist['id'])
#                         # if still not found, add it:
#                         if not existing_artist:
#                             new_artist = Artist(
#                                 id=artist['id'],
#                                 name=artist['name']
#                             )
#                             print(f"new artist: {new_artist}")
#                             db.session.add(new_artist)
#                             new_track.artists.append(new_artist)
#     db.session.commit()

#
#
#
#
# def load_saved_tracks():
#     with open(os.path.join(DATA_FOLDER, SAVED_TRACKS_DB)) as f:
#         return json.load(f)
#
#
#
# def sync_library(tracks=None, albums=None, playlists=None):
#     spotify_tracks = []
#     spotify_tracks.extend(tracks)
#     # print(spotify_tracks[-1])
#     for album in albums:
#         spotify_tracks.extend(album['tracks'])
#     # print(spotify_tracks[-1])
#     playlist_tracks = []
#     for playlist in playlists:
#         playlist_tracks.extend(playlist['tracks'])
#     spotify_tracks.extend([{'id': track_id} for track_id in playlist_tracks])
#     # print(spotify_tracks[-1])
#     sync_tracks(spotify_tracks)
#
#
# def sync_tracks(spotify_tracks):
#     library_tracks = load_library()
#     library = dict((track['id'], track) for track in library_tracks)
#     spotify = dict((track['id'], track) for track in spotify_tracks)
#     # first, drop items no more needed
#     library = {k: v for k, v in library.items() if k in spotify.keys()}
#     # then, add items not already in the library
#     for track in spotify_tracks:
#         library_track = library.get(track['id'], None)
#         if not library_track:
#             library[track['id']] = track
#     save_library(list(library.values()))
#
#
# def save_library(tracks):
#     print(tracks)
#     with open(os.path.join(DATA_FOLDER, LIBRARY_DB), 'w', encoding='utf-8') as f:
#         json.dump(tracks, f, ensure_ascii=False, indent=4)
#
