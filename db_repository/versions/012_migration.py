from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('steam_id', String(length=40)),
    Column('nickname', String(length=80)),
    Column('profile_url', String(length=80)),
    Column('avatar_url', String(length=80)),
    Column('team_name', String(length=80)),
    Column('team_skill_level', String(length=80)),
    Column('team_time_zone', String(length=80)),
    Column('joined_date', DateTime),
    Column('last_online', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['joined_date'].create()
    post_meta.tables['user'].columns['last_online'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['joined_date'].drop()
    post_meta.tables['user'].columns['last_online'].drop()
