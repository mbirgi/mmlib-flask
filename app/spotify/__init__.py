import os

import spotipy
import spotipy.util
# from dotenv import load_dotenv

_dev = True

def import_spotify_library():
    sp = Spotify(dev=_dev)
    saved_tracks = sp.get_saved_tracks()
    saved_albums = sp.get_saved_albums()
    playlists = sp.get_saved_playlists()
    return {
        "saved_tracks": saved_tracks,
        "saved_albums": saved_albums,
        "playlists": playlists
    }


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
    def __init__(self, username='mbirgi', scope='user-library-read', dev=False):
        # load_dotenv()
        self._dev = dev
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
        if not self._dev:
            while results['next']:
                results = self._instance.next(results)
                albums.extend(results['items'])
        return self._sanitize_albums(albums)

    def get_saved_playlists(self):
        results = self._instance.current_user_playlists(limit=50)
        playlists = results['items']
        if not self._dev:
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

# def get_genres(track, spotipy_instance):
#     artist_id = track['artists'][0]['id']
#     artist = spotipy_instance.artist(artist_id)
#     genres = artist['genres']
#     return genres
#
#
# def get_playlist_by_name(spotipy_instance, playlist_name, create_if_none=False):
#     user_id = spotipy_instance.current_user()['id']
#     results = spotipy_instance.user_playlists(user_id)
#     user_playlists = results['items']
#     while results['next']:
#         results = spotipy_instance.next(results)
#         user_playlists.extend(results['items'])
#     playlist_id, is_new = None, None
#     for list in user_playlists:
#         if playlist_name == list['name']:
#             playlist_id = list['id']
#             is_new = False
#             break
#     if not playlist_id and create_if_none == True:
#         new_playlist = spotipy_instance.user_playlist_create(user_id, name=playlist_name, public=False)
#         playlist_id = new_playlist['id']
#         is_new = True
#     return playlist_id, is_new
#
#
# def add_tracks(spotipy_instance, playlist_id, track_ids, skip_duplicates=True):
#     # get existing tracks:
#     results = spotipy_instance.playlist_tracks(playlist_id)  # TODO: get only IDs ('fields' filter)
#     existing_tracks = results['items']
#     while results['next']:
#         results = spotipy_instance.next(results)
#         existing_tracks.extend(results['items'])
#     existing_track_ids = [item['track']['id'] for item in existing_tracks]
#     logging.info(f"Playlist has {len(existing_track_ids)} existing tracks")
#     logging.info(f"Skipping duplicates: {skip_duplicates}")
#     if skip_duplicates:
#         new_track_ids = [track_id for track_id in track_ids if track_id not in existing_track_ids]
#     else:
#         new_track_ids = track_ids
#     logging.info(f"{len(new_track_ids)} tracks to be added")
#     user_id = spotipy_instance.current_user()['id']
#     if new_track_ids:
#         limit = 100
#         for i in range(0, len(new_track_ids), limit):
#             ids = new_track_ids[i:(i + limit)]
#             spotipy_instance.user_playlist_add_tracks(user_id, playlist_id, ids)
#             logging.info(f"{len(ids)} tracks added")
#         logging.info("OK")
#         return
#     logging.info("No tracks added")
#
#
# def get_tracks_in_playlists(spotipy_instance, playlist_ids):
#     tracks = []
#     for pl_id in playlist_ids:
#         # print(f"Getting tracks for playlist {pl_id}")
#         results = spotipy_instance.playlist_tracks(pl_id)  # TODO: get only IDs ('fields' filter)
#         pl_tracks = results['items']
#         while results['next']:
#             results = spotipy_instance.next(results)
#             pl_tracks.extend(results['items'])
#         tracks.extend(pl_tracks)
#     return tracks
#
#
# def get_audio_features_for_tracks(spotipy_instance, track_ids):
#     batch_size = 50
#     features = []
#     for i in range(0, len(track_ids), batch_size):
#         results = spotipy_instance.audio_features(track_ids[i:i + batch_size])
#         features.extend(results)
#     return features
