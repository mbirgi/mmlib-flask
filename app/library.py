import json
import os
from datetime import datetime

from app import db
from app.models import Track, Artist, Album, Playlist, Tag

_data_folder = 'data'
_admin_file = 'admin.json'


def _add_item_artists(item, artists):
    for artist in artists:
        item_artist = Artist.query.get(artist['id']) or _make_db_artist(artist)
        item.artists.append(item_artist)


def _add_item_tracks(item, tracks):
    for track in tracks:
        item_track = Track.query.get(track['id']) or _make_db_track(track)
        item.tracks.append(item_track)


def _make_db_album(sp_album):
    db_album = Album(
        id=sp_album['id'],
        name=sp_album['name'],
        total_tracks=sp_album['total_tracks']
    )
    db.session.add(db_album)
    _add_item_artists(db_album, sp_album['artists'])
    _add_item_tracks(db_album, sp_album['tracks'])
    return db_album


def _make_db_artist(artist):
    db_artist = Artist(
        id=artist['id'],
        name=artist['name'],
    )
    db.session.add(db_artist)
    return db_artist


def _make_db_playlist(sp_playlist):
    db_playlist = Playlist(
        id=sp_playlist['id'],
        name=sp_playlist['name'],
        description=sp_playlist['description'],
    )
    db.session.add(db_playlist)
    _add_item_tracks(db_playlist, sp_playlist['tracks'])
    return db_playlist


def _make_db_track(sp_track):
    lib_track = Track()
    _update_lib_track(lib_track, sp_track)
    db.session.add(lib_track)
    _add_item_artists(lib_track, sp_track['artists'])
    return lib_track


def _update_lib_playlist(lib_playlist, sp_playlist):
    lib_playlist.id = sp_playlist['id']
    lib_playlist.name = sp_playlist['name']
    lib_playlist.description = sp_playlist['description']
    db.session.add(lib_playlist)
    lib_playlist.tracks = []
    _add_item_tracks(lib_playlist, sp_playlist['tracks'])
    return lib_playlist


def _update_lib_track(lib_track, sp_track):
    lib_track.id = sp_track['id']
    if sp_track.get('name'): lib_track.name = sp_track.get('name')
    if sp_track.get('duration_ms'): lib_track.duration_ms = sp_track.get('duration_ms')
    if sp_track.get('track_number'): lib_track.track_number = sp_track.get('track_number')
    if sp_track.get('danceability'): lib_track.danceability = sp_track.get('danceability')
    if sp_track.get('energy'): lib_track.energy = sp_track.get('energy')
    if sp_track.get('key'): lib_track.key = sp_track.get('key')
    if sp_track.get('loudness'): lib_track.loudness = sp_track.get('loudness')
    if sp_track.get('mode'): lib_track.mode = sp_track.get('mode')
    if sp_track.get('speechiness'): lib_track.speechiness = sp_track.get('speechiness')
    if sp_track.get('acousticness'): lib_track.acousticness = sp_track.get('acousticness')
    if sp_track.get('instrumentalness'): lib_track.instrumentalness = sp_track.get('instrumentalness')
    if sp_track.get('liveness'): lib_track.liveness = sp_track.get('liveness')
    if sp_track.get('valence'): lib_track.valence = sp_track.get('valence')
    if sp_track.get('tempo'): lib_track.tempo = sp_track.get('tempo')
    if sp_track.get('time_signature'): lib_track.time_signature = sp_track.get('time_signature')
    return lib_track


def get_saved_albums():
    return Album.query.filter_by(is_saved_album=True).all()


def get_saved_albums_count():
    return Album.query.filter_by(is_saved_album=True).count()


def get_saved_playlists():
    return Playlist.query.all()


def get_saved_playlists_count():
    return Playlist.query.count()


def get_saved_tracks():
    return Track.query.filter_by(is_saved_track=True).all()


def get_saved_tracks_count():
    return Track.query.filter_by(is_saved_track=True).count()


def get_total_tracks_count():
    return Track.query.count()


def _make_dict_tracks(lib_tracks):
    tracks = []
    for lib_track in lib_tracks:
        track = dict(lib_track.__dict__)
        track.pop('_sa_instance_state', None)
        tracks.append(track)
    return tracks


def get_db_tracks(offset=0, limit=None):
    return Track.query.limit(limit).offset(offset).all()


def get_tracks(track_ids=None):
    lib_tracks = []
    for id in track_ids:
        track = Track.query.get(id)
        lib_tracks.append(track)
    tracks = _make_dict_tracks(lib_tracks)
    return tracks


def get_album_tracks(album_ids):
    tracks = []
    for album_id in album_ids:
        album = Album.query.get(album_id)
        tracks.extend(album.tracks)
    return tracks


def get_artist_tracks(artist_ids):
    tracks = []
    for artist_id in artist_ids:
        artist = Artist.query.get(artist_id)
        tracks.extend(artist.tracks)
    return tracks


def get_tagged_tracks(tag_ids):
    tracks = []
    for tag_id in tag_ids:
        tag = Tag.query.get(tag_id)
        tracks.extend(tag.tracks)
    return tracks


def get_filtered_track_ids(tags_filter=[], artist_filter=[], album_filter=[]):
    # if tags_filter is None: tags_filter = Tag.query.all()
    # if artist_filter is None: artist_filter = Artist.query.all()
    # if album_filter is None: album_filter = Album.query.all()
    all_tracks = Track.query.all()
    filtered_tracks = []
    for track in all_tracks:
        # print("track.album_id:", track.album_id)
        # print("album_filter:", album_filter)
        if len(album_filter) == 0 or track.album_id in album_filter:
            # print("album ok")
            for artist in track.artists:
                # print("artist.id:", artist.id)
                # print("artist_filter:", artist_filter)
                if len(artist_filter) == 0 or artist.id in artist_filter:
                    # print("artist ok")
                    # print("track.tags:", track.tags)
                    # print("tags_filter:", tags_filter)
                    for tag in track.tags:
                        if tag.id in tags_filter:
                            tags_ok = True
                    if len(tags_filter) == 0 or tags_ok:
                        # print("tags ok")
                        filtered_tracks.append(track)
                        break
                # else:
                    # print("artist not ok")
            # break
        # else:
        #     pass
    print("filtered_tracks:", filtered_tracks)
    return [track.id for track in filtered_tracks]


def get_all_tags():
    return Tag.query.all()


def get_all_albums():
    return Album.query.all()


def get_all_artists():
    return Artist.query.all()


def get_all_playlists():
    return Playlist.query.all()


def save_tracks(sp_tracks):
    for sp_track in sp_tracks:
        if not sp_track: continue
        lib_track = Track.query.get(sp_track['id'])
        if lib_track is None:
            print("track not found")
            print("sp_track:", sp_track)
            print("lib_track:", lib_track)
            lib_track = _make_db_track(sp_track)
        else:
            _update_lib_track(lib_track, sp_track)
            # print("updated lib_track:", lib_track)
        db.session.add(lib_track)
    db.session.commit()


def update_saved_albums(sp_albums):
    for sp_album in sp_albums:
        lib_album = Album.query.get(sp_album['id']) or _make_db_album(sp_album)
        lib_album.is_saved_album = True
        db.session.add(lib_album)
    db.session.commit()


def update_saved_playlists(sp_playlists):
    for sp_playlist in sp_playlists:
        lib_playlist = Playlist.query.get(sp_playlist['id'])
        if lib_playlist is None:
            lib_playlist = _make_db_playlist(sp_playlist)
        else:
            _update_lib_playlist(lib_playlist, sp_playlist)
        lib_playlist.is_saved_playlist = True
        db.session.add(lib_playlist)
    db.session.commit()


def update_saved_tracks(sp_tracks):
    for sp_track in sp_tracks:
        lib_track = Track.query.get(sp_track['id']) or _make_db_track(sp_track)
        lib_track.is_saved_track = True
        db.session.add(lib_track)
    db.session.commit()


def get_last_import_dt():
    with open(os.path.join(_data_folder, _admin_file), 'r', encoding='utf-8') as f:
        items = json.load(f)
    return datetime.fromisoformat(items.get('last_import_dt'))


def update_last_import_dt():
    last_import_dt = datetime.utcnow().isoformat()
    with open(os.path.join(_data_folder, _admin_file), 'w', encoding='utf-8') as f:
        json.dump({'last_import_dt': last_import_dt}, f, ensure_ascii=False, indent=4)
