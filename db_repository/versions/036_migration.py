from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
scrim = Table('scrim', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('date', DATETIME),
    Column('map1', VARCHAR(length=80)),
    Column('map2', VARCHAR(length=80)),
    Column('connection', VARCHAR(length=80)),
    Column('team1_id', INTEGER),
    Column('team2_id', INTEGER),
    Column('type', VARCHAR(length=80)),
    Column('state', VARCHAR(length=20)),
    Column('log1', VARCHAR(length=40)),
    Column('log2', VARCHAR(length=40)),
    Column('log_team1', VARCHAR(length=10)),
    Column('log_team2', VARCHAR(length=10)),
)

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
    Column('team1_result', String(length=40)),
    Column('team2_result', String(length=40)),
    Column('team1_color', String(length=10)),
    Column('team2_color', String(length=10)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['scrim'].columns['log1'].drop()
    pre_meta.tables['scrim'].columns['log2'].drop()
    pre_meta.tables['scrim'].columns['log_team1'].drop()
    pre_meta.tables['scrim'].columns['log_team2'].drop()
    post_meta.tables['scrim'].columns['team1_color'].create()
    post_meta.tables['scrim'].columns['team1_result'].create()
    post_meta.tables['scrim'].columns['team2_color'].create()
    post_meta.tables['scrim'].columns['team2_result'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['scrim'].columns['log1'].create()
    pre_meta.tables['scrim'].columns['log2'].create()
    pre_meta.tables['scrim'].columns['log_team1'].create()
    pre_meta.tables['scrim'].columns['log_team2'].create()
    post_meta.tables['scrim'].columns['team1_color'].drop()
    post_meta.tables['scrim'].columns['team1_result'].drop()
    post_meta.tables['scrim'].columns['team2_color'].drop()
    post_meta.tables['scrim'].columns['team2_result'].drop()
