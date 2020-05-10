from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


album_artists = db.Table(
    'album_artists',
    db.Column('album_id', db.String(22), db.ForeignKey('albums.id')),
    db.Column('artist_id', db.String(22), db.ForeignKey('artists.id'))
)

album_tracks = db.Table(
    'album_tracks',
    db.Column('album_id', db.String(22), db.ForeignKey('albums.id')),
    db.Column('track_id', db.String(22), db.ForeignKey('tracks.id'))
)

playlist_tracks = db.Table(
    'playlist_tracks',
    db.Column('playlist_id', db.String(22), db.ForeignKey('playlists.id')),
    db.Column('track_id', db.String(22), db.ForeignKey('tracks.id'))
)

track_artists = db.Table(
    'track_artists',
    db.Column('track_id', db.String(22), db.ForeignKey('tracks.id')),
    db.Column('artist_id', db.String(22), db.ForeignKey('artists.id'))
)


class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.String(22), primary_key=True)  # use Spotify ID
    name = db.Column(db.String(256))
    year = db.Column(db.Integer)
    artists = db.relationship('Artist', secondary=album_artists, backref=db.backref('albums'))
    tracks = db.relationship('Track', secondary=album_tracks, backref=db.backref('albums'))

    def __repr__(self):
        return self.name


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.String(22), primary_key=True)  # use Spotify ID
    name = db.Column(db.String(256))
    # albums = db.relationship('Album', secondary=album_artists, backref=db.backref('artists'))
    # tracks = db.relationship('Track', secondary=track_artists, backref=db.backref('artists'))

    def __repr__(self):
        return self.name


class Track(db.Model):
    __tablename__ = 'tracks'
    id = db.Column(db.String(22), primary_key=True)  # use Spotify ID
    name = db.Column(db.String(256))
    artists = db.relationship('Artist', secondary=track_artists, backref=db.backref('tracks'))
    # albums = db.relationship('Album', secondary=album_tracks, backref=db.backref('tracks'))
    duration_ms = db.Column(db.Integer)
    tempo = db.Column(db.Float)

    def __repr__(self):
        return self.name


class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.String(22), primary_key=True)  # use Spotify ID
    tracks = db.relationship('Track', secondary=playlist_tracks, backref=db.backref('playlists'))
    name = db.Column(db.String(256))
    description = db.Column(db.String(256))

    def __repr__(self):
        return self.name
