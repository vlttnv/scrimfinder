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
    Column('join_date', DateTime),
    Column('last_online', DateTime),
    Column('team_leader', Boolean),
    Column('has_given_rep_to', Text),
    Column('has_played_with', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['has_given_rep_to'].create()
    post_meta.tables['user'].columns['has_played_with'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['has_given_rep_to'].drop()
    post_meta.tables['user'].columns['has_played_with'].drop()
