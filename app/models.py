from . import db

album_artists = db.Table(
    'album_artists',
    db.Column('album_id', db.String(22), db.ForeignKey('albums.id'), primary_key=True),
    db.Column('artist_id', db.String(22), db.ForeignKey('artists.id'), primary_key=True)
)

# album_tracks = db.Table(
#     'album_tracks',
#     db.Column('album_id', db.String(22), db.ForeignKey('albums.id'), primary_key=True),
#     db.Column('track_id', db.String(22), db.ForeignKey('tracks.id'), primary_key=True),
#     # db.Column('track_num', db.Integer, primary_key=True)
# )

playlist_tracks = db.Table(
    'playlist_tracks',
    db.Column('playlist_id', db.String(22), db.ForeignKey('playlists.id')),
    db.Column('track_id', db.String(22), db.ForeignKey('tracks.id'))
)

track_artists = db.Table(
    'track_artists',
    db.Column('track_id', db.String(22), db.ForeignKey('tracks.id'), primary_key=True),
    db.Column('artist_id', db.String(22), db.ForeignKey('artists.id'), primary_key=True)
)

track_tags = db.Table(
    'track_tags',
    db.Column('track_id', db.String(22), db.ForeignKey('tracks.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.String(22), primary_key=True)  # use Spotify ID
    name = db.Column(db.String(256))
    is_saved_album = db.Column(db.Boolean, default=False)
    year = db.Column(db.Integer)
    artists = db.relationship('Artist', secondary=album_artists, backref=db.backref('albums'), lazy='joined')
    tracks = db.relationship('Track', backref='album', lazy='joined')
    total_tracks = db.Column(db.Integer)

    def __repr__(self):
        return f"<Album {self.name}>"


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.String(22), primary_key=True)  # use Spotify ID
    name = db.Column(db.String(256))

    def __repr__(self):
        return f"<Artist {self.name}>"


class Track(db.Model):
    __tablename__ = 'tracks'
    id = db.Column(db.String(22), primary_key=True)  # use Spotify ID
    name = db.Column(db.String(256))
    is_saved_track = db.Column(db.Boolean, default=False)
    album_id = db.Column(db.String, db.ForeignKey('albums.id'))
    artists = db.relationship('Artist', secondary=track_artists, backref=db.backref('tracks'), lazy='joined')
    track_number = db.Integer()
    duration_ms = db.Column(db.Integer)
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    key = db.Column(db.Integer)
    loudness = db.Column(db.Float)
    mode = db.Column(db.Integer)
    speechiness = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    valence = db.Column(db.Float)
    tempo = db.Column(db.Float)
    time_signature = db.Column(db.Integer)

    def __repr__(self):
        return f"<Track {self.name}>"


class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.String(22), primary_key=True)  # use Spotify ID
    tracks = db.relationship('Track', secondary=playlist_tracks, backref=db.backref('playlists'), lazy='joined')
    name = db.Column(db.String(256), default="New Playlist")
    description = db.Column(db.String(256))
    is_saved_playlist = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Playlist {self.name}>"


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    tracks = db.relationship('Track', secondary=track_tags, backref=db.backref('tags'), lazy='joined')

    def __repr__(self):
        return f"<Tag {self.name}>"



# class SavedTrack(db.Model):
#     __tablename__ = 'saved_tracks'
#     id = db.Column(db.String(22), primary_key=True)  # use Spotify ID
#     track = db.Column(db.String(22), db.ForeignKey('tracks.id'))
#
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     def __repr__(self):
#         return '<Role %r>' % self.name
#
#
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#
#     def __repr__(self):
#         return '<User %r>' % self.username
#
