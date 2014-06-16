from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
<<<<<<< HEAD
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('steam_id', String(length=40)),
    Column('nickname', String(length=80)),
    Column('profile_url', String(length=80)),
    Column('avatar_url', String(length=80)),
    Column('avatar_url_full', String(length=80)),
    Column('join_date', DateTime),
    Column('last_online', DateTime),
    Column('team_leader', Boolean),
    Column('has_given_rep_to', Text),
    Column('has_played_with', Text),
=======
scrim = Table('scrim', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('date', DateTime),
    Column('map1', String(length=80)),
    Column('map2', String(length=80)),
    Column('connection', String(length=80)),
    Column('team1_id', Integer),
    Column('team2_id', Integer),
    Column('type', String(length=80)),
    Column('state', String(length=20)),
    Column('result', String(length=20)),
>>>>>>> e1758e7df61e0660a6f3ad8129fb1f7c201be280
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
<<<<<<< HEAD
    post_meta.tables['user'].columns['avatar_url_full'].create()
=======
    post_meta.tables['scrim'].columns['result'].create()
>>>>>>> e1758e7df61e0660a6f3ad8129fb1f7c201be280


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
<<<<<<< HEAD
    post_meta.tables['user'].columns['avatar_url_full'].drop()
=======
    post_meta.tables['scrim'].columns['result'].drop()
>>>>>>> e1758e7df61e0660a6f3ad8129fb1f7c201be280
