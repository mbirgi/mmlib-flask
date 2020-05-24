import os

import spotipy
import spotipy.util
from flask import current_app as app

from mmlib import dev_mode


def _login(username, scope):
    spotify_auth_params = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'scope': scope
    }
    try:
        token = spotipy.util.prompt_for_user_token(username, **spotify_auth_params)
    except:
        os.remove(f'.cache-{username}')
        token = spotipy.util.prompt_for_user_token(username, **spotify_auth_params)
    return spotipy.Spotify(auth=token)


class Spotify():
    af_batch_size = 50

    def __init__(self, username='mbirgi', scope='user-library-read'):
        # print(f"dev mode: {_dev}")
        self._dev = dev_mode
        self._instance = _login(username, scope)
        # self.market = 'CH'

    def get_saved_tracks(self):
        results = self._instance.current_user_saved_tracks()
        tracks = results['items']
        if not self._dev:
            while results['next']:
                results = self._instance.next(results)
                tracks.extend(results['items'])
        return self._sanitize_tracks([track['track'] for track in tracks])

    def get_saved_albums(self):
        results = self._instance.current_user_saved_albums(limit=50)
        albums = results['items']
        if (self._dev) and (len(albums) > 3):
            del albums[3:]
            app.logger.debug("dev mode: albums curtailed")
        else:
            while results['next']:
                results = self._instance.next(results)
                albums.extend(results['items'])
        return self._sanitize_albums(albums)

    def get_saved_playlists(self):
        results = self._instance.current_user_playlists(limit=50)
        playlists = results['items']
        if self._dev and len(playlists) > 3:
            del playlists[3:]
            app.logger.debug("dev mode: playlists curtailed")
            app.logger.debug(f"playlists: {[pl['name'] for pl in playlists]}")
        else:
            while results['next']:
                results = self._instance.next(results)
                playlists.extend(results['items'])
        return self._sanitize_playlists(playlists)

    def _sanitize_tracks(self, tracks):
        sanitized_tracks = []
        for track in tracks:
            sanitized_track = {
                "id": track['id'],
                "name": track['name'],
                "artists": [{'id': artist['id'], 'name': artist['name']} for artist in track['artists']],
                "duration_ms": track['duration_ms'],
                'track_number': track.get('track_number'),
            }
            sanitized_tracks.append(sanitized_track)
        return sanitized_tracks

    def _sanitize_albums(self, albums):
        sanitized_albums = []
        for album in albums:
            sanitized_tracks = self._sanitize_tracks(album['album']['tracks']['items'])
            sanitized_album = {
                "id": album['album']['id'],
                "name": album['album']['name'],
                "artists": [{'id': artist['id'], 'name': artist['name']} for artist in album['album']['artists']],
                "total_tracks": album['album']['total_tracks'],
                "tracks": sanitized_tracks,
            }
            sanitized_albums.append(sanitized_album)
        return sanitized_albums

    def _sanitize_playlists(self, playlists):
        sanitized_playlists = []
        for playlist in playlists:
            tracks = self._get_playlist_tracks(playlist['id'])
            sanitized_playlist = {
                "id": playlist['id'],
                "name": playlist['name'],
                "description": playlist['description'],
                "tracks": self._sanitize_tracks(tracks),
            }
            sanitized_playlists.append(sanitized_playlist)
        return sanitized_playlists

    def _get_playlist_tracks(self, playlist_id):
        results = self._instance.playlist_tracks(playlist_id)
        tracks = results['items']
        if not self._dev:
            while results['next']:
                results = self._instance.next(results)
                tracks.extend(results['items'])
        return [track['track'] for track in tracks]

    def get_audio_features(self, tracks):
        track_features = self._instance.audio_features(tracks)
        return track_features
