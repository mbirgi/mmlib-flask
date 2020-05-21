import datetime
import time

from app import library as lib
from .spotify import Spotify

sp = Spotify()


def _update_audio_features():
    print("updating audio features")
    batch_size = sp.af_batch_size
    # print("batch_size:", batch_size)
    offset = 0
    batch = lib.get_tracks(limit=batch_size, offset=offset)
    # print("batch:", batch)
    while len(batch) > 0:
        features = sp.get_audio_features([track.id for track in batch])
        # print("features:", features)
        lib.save_tracks(features)
        offset += batch_size
        batch = lib.get_tracks(limit=batch_size, offset=offset)


def _get_playlist_tracks(sp_playlists):
    tracks = []
    for pl in sp_playlists:
        tracks.extend(pl['tracks'])
    return tracks


def _refresh_saved_albums():
    saved_albums = sp.get_saved_albums()
    print("saved albums:", len(saved_albums))
    lib.update_saved_albums(saved_albums)
    # album_tracks = []
    # for album in saved_albums:
    #     album_tracks.extend(album['tracks'])
    # _get_audio_features(album_tracks)


def _refresh_saved_playlists():
    saved_playlists = sp.get_saved_playlists()
    print("saved playlists:", len(saved_playlists))
    lib.update_saved_playlists(saved_playlists)
    # _get_audio_features(_get_playlist_tracks(saved_playlists))


def _refresh_saved_tracks():
    saved_tracks = sp.get_saved_tracks()
    print("saved tracks:", len(saved_tracks))
    lib.update_saved_tracks(saved_tracks)
    # _get_audio_features(saved_tracks)


def refresh_library():
    start = time.time()
    # saved_tracks = sp.get_saved_tracks()
    # saved_playlists = sp.get_saved_playlists()
    # saved_albums = sp.get_saved_albums()

    _refresh_saved_tracks()
    _refresh_saved_albums()
    _refresh_saved_playlists()
    _update_audio_features()
    end = time.time()
    print(f"refresh duration (h:m:s): {str(datetime.timedelta(seconds=int(end - start)))}")
