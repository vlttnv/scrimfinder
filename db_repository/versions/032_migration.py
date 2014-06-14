from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
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
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['scrim'].columns['state'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['scrim'].columns['state'].drop()
