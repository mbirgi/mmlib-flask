from .library import Library
from .spotify import Spotify

sp = Spotify()
lib = Library()


def refresh_library():
    _refresh_saved_tracks()
    _refresh_saved_albums()
    _refresh_saved_playlists()


def _get_audio_features(tracks):
    batch_size = sp.af_batch_size
    for i in range(0, len(tracks), batch_size):
        upd_tracks = tracks[i:i+batch_size]
        sp.get_audio_features(upd_tracks)
        lib.save_tracks(upd_tracks)


def _refresh_saved_tracks():
    saved_tracks = sp.get_saved_tracks()
    print("saved tracks:", len(saved_tracks))
    lib.update_saved_tracks(saved_tracks)
    _get_audio_features(saved_tracks)


def _refresh_saved_albums():
    saved_albums = sp.get_saved_albums()
    print("saved albums:", len(saved_albums))
    lib.update_saved_albums(saved_albums)
    # _get_audio_features(saved_albums)


def _refresh_saved_playlists():
    pass
