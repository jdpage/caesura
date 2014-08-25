import sqlalchemy as sa

metadata = sa.MetaData()

# holy datamodel, Batman!
# this is pretty damn complicated due to the fact that we are, by definition,
# dealing with prima donnas who do things like changing their names.
# Friggin' Snoop Dogg, man.

# by splitting up a person from their name, we can encode things like
# "Snoop Dogg" and "Snoop Lion" being the same person.
persons = sa.Table(
    'person', metadata
    , sa.Column('id', sa.Integer, primary_key=True)
    , sa.Column('effective', sa.DateTime, primary_key=True)
    , sa.Column('name', sa.String)
    , sa.Column('last_modified', sa.DateTime)
)

# by splitting up a group from their name, we can encode things like
# "Godspeed You! Black Emperor" and "Godspeed You Black Emperor!" being the
# same group.
groups = sa.Table(
    'group', metadata
    , sa.Column('id', sa.Integer, primary_key=True)
    , sa.Column('effective', sa.DateTime, primary_key=True)
    , sa.Column('name', sa.String)
    , sa.Column('last_modified', sa.DateTime)
)

# we have a personnel table which lets us do things like distinguish between
# Black Sabbath with Ozzy Osbourne and Black Sabbath with Ronnie James Dio.
personnel = sa.Table(
    'personnel', metadata
    , sa.Column('person_id', sa.Integer, primary_key=True)
    , sa.Column('group_id', sa.Integer, primary_key=True)
    , sa.Column('effective', sa.DateTime, primary_key=True)
    , sa.Column('position', sa.String)
    , sa.Column('last_modified', sa.DateTime)
)

# For solo albums, you'd want to have a group containing just the one person
albums = sa.Table(
    'album', metadata
    , sa.Column('id', sa.Integer, primary_key=True)
    , sa.Column('name', sa.String)
    , sa.Column('group_id', sa.Integer, sa.ForeignKey('group.id'))
    , sa.Column('last_modified', sa.DateTime)
)

# releases are separate from albums so we can distinguish between e.g. the
# deluxe edition and the regular edition.
releases = sa.Table(
    'release', metadata
    , sa.Column('album_id', sa.Integer, sa.ForeignKey('album.id'),
                primary_key=True)
    , sa.Column('released', sa.DateTime, primary_key=True)
    , sa.Column('version', sa.String, primary_key=True)
    , sa.Column('cover', sa.String)
    , sa.Column('track_count', sa.Intger)
    , sa.Column('last_modified', sa.DateTime)
)

songs = sa.Table(
    'song', metadata
    , sa.Column('id', sa.Integer, primary_key=True)
    , sa.Column('name', sa.String)
    , sa.Column('group_id', sa.Integer, sa.ForeignKey('group.id'))
    , sa.Column('last_modified', sa.DateTime)
)

tracks = sa.Table(
    'track', metadata
    , sa.Column('id', sa.Integer, primary_key=True)
    , sa.Column('song_id', sa.Integer, sa.ForeignKey('song.id'))
    , sa.Column('group_id', sa.Integer, sa.ForeignKey('group.id'))
    , sa.Column('version', sa.String)
    , sa.Column('duration', sa.Interval)
    , sa.Column('last_modified', sa.DateTime)
)

track_tags = sa.Table(
    'tag', metadata
    , sa.Column('name', sa.String, primary_key=True)
    , sa.Column('track_id', sa.Integer, sa.ForeignKey('track.id'),
                primary_key=True)
    , sa.Column('user_id', sa.String, primary_key=True)
    , sa.Column('global', sa.Boolean)
    , sa.Column('last_modified', sa.DateTime)
)

guest_personnel = sa.Table(
    'guest_personnel', metadata
    , sa.Column('track_id', sa.Integer, sa.ForeignKey('track.id'),
                primary_key=True)
    , sa.Column('personnel_id', sa.Integer, sa.ForeignKey('personnel.id'),
                primary_key=True)
    , sa.Column('last_modified', sa.DateTime)
)

album_entries = sa.Table(
    'album_entry', metadata
    , sa.Column('release_id', sa.Integer, sa.ForeignKey('release.id'),
                primary_key=True)
    , sa.Column('track_id', sa.Integer, sa.ForeignKey('track.id'),
                primary_key=True)
    , sa.Column('disc_or_side_number', sa.String)
    , sa.Column('track_number', sa.Integer)
    , sa.Column('padding', sa.Interval)
    , sa.Column('fingerprint', sa.String)
    , sa.Column('last_modified', sa.DateTime)
)

audios = sa.Table(
    'audio', metadata
    , sa.Column('album_id', sa.Integer, sa.ForeignKey('album.id'),
                primary_key=True)
    , sa.Column('track_id', sa.Integer, sa.ForeignKey('track.id'),
                primary_key=True)
    , sa.Column('format', sa.String, primary_key=True)
    , sa.Column('bit_rate', sa.Integer, primary_key=True)
    , sa.Column('sample_rate', sa.Integer, primary_key=True)
    , sa.Column('lossless', sa.Boolean, primary_key=True)
    , sa.Column('data', sa.String)
    , sa.Column('last_modified', sa.DateTime)
)

users = sa.Table(
    'user', metadata
    , sa.Column('id', sa.String, primary_key=True)
    , sa.Column('name', sa.String)
    , sa.Column('email', sa.String)
    , sa.Column('password', sa.String)
    , sa.Column('approved', sa.Boolean)
    , sa.Column('user_group', sa.String, sa.ForeignKey('user_group.id'))
    , sa.Column('last_modified', sa.DateTime)
)

user_groups = sa.Table(
    'user_group', metadata
    , sa.Column('id', sa.String, primary_key=True)
    , sa.Column('can_authorize', sa.Boolean)
    , sa.Column('can_upload', sa.Boolean)
    , sa.Column('can_download', sa.Boolean)
    , sa.Column('can_edit', sa.Boolean)
    , sa.Column('can_trash', sa.Boolean)
    , sa.Column('can_purge', sa.Boolean)
    , sa.Column('can_force_flush', sa.Boolean)
    , sa.Column('last_modified', sa.DateTime)
)

playlists = sa.Table(
    'playlist', metadata
    , sa.Column('id', sa.Integer, primary_key=True)
    , sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'))
    , sa.Column('name', sa.String)
    , sa.Column('last_modified', sa.DateTime)
)

playlist_entries = sa.Table(
    'playlist_entry', metadata
    , sa.Column('playlist_id', sa.Integer, sa.ForeignKey('playlist.id'),
                primary_key=True)
    , sa.Column('track_id', sa.Integer, sa.ForeignKey('track.id'),
                primary_key=True)
    , sa.Column('entry_number', sa.Integer)
    , sa.Column('last_modified', sa.DateTime)
)

