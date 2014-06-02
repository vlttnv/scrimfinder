from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
available = Table('available', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('time_from', String),
    Column('time_to', String),
    Column('user_id', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('steam_id', String(length=40)),
    Column('nickname', String(length=80)),
    Column('profile_url', String(length=80)),
    Column('avatar_url', String(length=80)),
    Column('team_skill_level', Integer),
    Column('team_time_zone', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['available'].create()
    post_meta.tables['user'].columns['team_skill_level'].create()
    post_meta.tables['user'].columns['team_time_zone'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['available'].drop()
    post_meta.tables['user'].columns['team_skill_level'].drop()
    post_meta.tables['user'].columns['team_time_zone'].drop()
