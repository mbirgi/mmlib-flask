import os

import spotipy
import spotipy.util

from app.utils import debug

_dev = bool(os.getenv('MMLIB_DEV_MODE') == '1')
print("dev mode:", _dev)


def import_spotify_library():
    sp = Spotify()
    saved_tracks = sp.get_saved_tracks()
    saved_albums = sp.get_saved_albums()
    playlists = sp.get_saved_playlists()
    return {
        "saved_tracks": saved_tracks,
        "saved_albums": saved_albums,
        "playlists": playlists
    }


# def get_audio_features_for_tracks(track_ids):
#     """Gets the audio features for several tracks
#
#     Args:
#         track_ids (list): a list of spotify track ids
#
#     Returns:
#         list: a list of dicts like [{id:<track_id>, tempo:<tempo>, ...}, ...]
#     """
#     sp = Spotify()
#     return sp.get_audio_features_for_tracks(track_ids)

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
        self._dev = _dev
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
            print("dev mode: albums curtailed")
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
            debug("playlists", [pl['name'] for pl in playlists])
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
        # for i in range(0, len(track_ids), batch_size):
        #     results = self._instance.audio_features(track_ids[i:i+batch_size])
        #     features.extend(results)
        # for track in tracks:
        #     track_features = next((f for f in features if f['id'] == track['id']), None)
        #     print(("track:", track))
        # print("track_features:", track_features)
        # if track_features is not None:
        # track['danceability'] = track_features.get('danceability')
        # track['energy'] = track_features.get('energy')
        # track['key'] = track_features.get('key')
        # track['loudness'] = track_features.get('loudness')
        # track['mode'] = track_features.get('mode')
        # track['speechiness'] = track_features.get('speechiness')
        # track['acousticness'] = track_features.get('acousticness')
        # track['instrumentalness'] = track_features.get('instrumentalness')
        # track['liveness'] = track_features.get('liveness')
        # track['valence'] = track_features.get('valence')
        # track['tempo'] = track_features.get('tempo')
        # track['duration_ms'] = track_features.get('duration_ms')
        # track['time_signature'] = track_features.get('time_signature')
        return track_features

