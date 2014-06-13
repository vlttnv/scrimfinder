from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
scrim = Table('scrim', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('start_time', VARCHAR(length=80)),
    Column('map1', VARCHAR(length=80)),
    Column('map2', VARCHAR(length=80)),
    Column('connection_info', VARCHAR(length=80)),
    Column('team_id1', INTEGER),
    Column('team_id2', INTEGER),
    Column('scrim_type', VARCHAR(length=80)),
    Column('day', VARCHAR(length=80)),
)

scrim = Table('scrim', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('date', DateTime),
    Column('map1', String(length=80)),
    Column('map2', String(length=80)),
    Column('connection_info', String(length=80)),
    Column('team_id1', Integer),
    Column('team_id2', Integer),
    Column('scrim_type', String(length=80)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['scrim'].columns['day'].drop()
    pre_meta.tables['scrim'].columns['start_time'].drop()
    post_meta.tables['scrim'].columns['date'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['scrim'].columns['day'].create()
    pre_meta.tables['scrim'].columns['start_time'].create()
    post_meta.tables['scrim'].columns['date'].drop()
