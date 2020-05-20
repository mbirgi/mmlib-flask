from .json_library import JSONLibrary
from .sql_library import SQLLibrary

lib = SQLLibrary()


class Library():
    def save_tracks(self, sp_tracks):
        lib.save_tracks(sp_tracks)

    def update_saved_tracks(self, sp_tracks):
        lib.update_saved_tracks(sp_tracks)

    def update_saved_albums(self, sp_albums):
        lib.update_saved_albums(sp_albums)
