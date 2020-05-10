from .. import db
from ..models import Track, Artist


def _update_saved_tracks(fetched_tracks):
    if not fetched_tracks: return
    # check for existing saved tracks that are no more in the spotify library
    existing_tracks = Track.query.filter_by(is_saved_track=True).all()
    deleted_tracks = [track for track in existing_tracks if track not in fetched_tracks]
    for track in deleted_tracks:
        track.is_saved_track = False
        db.session.add(track)
    # add tracks not already in the library
    for fetched_track in fetched_tracks:
        existing_track = next((track for track in existing_tracks if track.id == fetched_track['id']), None)
        if existing_track:
            existing_track.is_saved_track = True
        else:
            new_track = Track(
                id=fetched_track['id'],
                name=fetched_track['name'],
                is_saved_track=True,
                duration_ms=fetched_track['duration_ms'],
                artists=[]
            )
            print(f"new track: {new_track}")
            db.session.add(new_track)
            for artist in fetched_track['artists']:
                # check if artist exists:
                existing_artist = Artist.query.get(artist['id'])
                if not existing_artist:
                    new_artist = Artist(
                        id=artist['id'],
                        name=artist['name']
                    )
                    print(f"new artist: {new_artist}")
                    db.session.add(new_artist)
                    new_track.artists.append(new_artist)
        db.session.commit()


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
