from .. import db
from ..models import Track


def _fetch_saved_tracks():
    print(f"fetching saved tracks from library")
    # TODO: fetch tracks from db
    return []


def _delete_saved_tracks(tracks):
    if not tracks: return
    print(f"deleting saved tracks: {tracks}")


def _add_saved_tracks(tracks):
    if not tracks: return
    print(f"adding saved tracks: {tracks}")
    for track in tracks:
        db.session.add(Track(
            id=track['id'],
            name=track['name'],
            duration_ms=track['duration_ms']
        ))
    db.session.commit()


def _update_saved_tracks(new_saved_tracks):
    old_saved_tracks = _fetch_saved_tracks()
    deletable_saved_tracks = [track for track in old_saved_tracks if track not in new_saved_tracks]
    additional_saved_tracks = [track for track in new_saved_tracks if track not in old_saved_tracks]
    _delete_saved_tracks(deletable_saved_tracks)
    _add_saved_tracks(additional_saved_tracks)


def refresh_from_spotify(spotify_library):
    _update_saved_tracks(spotify_library['saved_tracks'])
    # update saved albums
    # update playlists
    # delete no more needed tracks
    # get audio features for new tracks
    pass

# import json
# import os
#
# DATA_FOLDER = 'data'
# SAVED_TRACKS_DB = 'saved_tracks.json'
# SAVED_ALBUMS_DB = 'saved_albums.json'
# SAVED_PLAYLISTS_DB = 'saved_playlists.json'
# LIBRARY_DB = 'library.json'
#
#
# def save_items(items, libname):
#     if not os.path.exists(DATA_FOLDER):
#         os.mkdir(DATA_FOLDER)
#     with open(os.path.join(DATA_FOLDER, f"{libname}.json"), 'w', encoding='utf-8') as f:
#         json.dump(items, f, ensure_ascii=False, indent=4)
#
#
# def load_saved_tracks():
#     with open(os.path.join(DATA_FOLDER, SAVED_TRACKS_DB)) as f:
#         return json.load(f)
#
#
# def load_saved_albums():
#     with open(os.path.join(DATA_FOLDER, SAVED_ALBUMS_DB)) as f:
#         return json.load(f)
#
#
# def load_saved_playlists():
#     with open(os.path.join(DATA_FOLDER, SAVED_PLAYLISTS_DB)) as f:
#         return json.load(f)
#
#
# def load_library():
#     # with open(os.path.join(DATA_FOLDER, LIBRARY_DB)) as f:
#     #     return json.load(f)
#     return []
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
