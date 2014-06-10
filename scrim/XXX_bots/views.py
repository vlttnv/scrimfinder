from flask import Blueprint, render_template
from scrim import db
from scrim.models import User, Team

bots = Blueprint('bots', __name__)

@bots.route('/')
def bots_home():
    return 'Sup nigger', 200

@bots.route('/create_users')
def bots_create_users():
    """
    Create 100 bot users.
    """

    from datetime import datetime as dt
    
    time_in_milliseconds = dt.utcnow().strftime('%Y%m%d%H%M%S%f')
    fake_steam_id = 'BotSteamID_' + time_in_milliseconds
    fake_name = 'BotUser_' + time_in_milliseconds
    fake_team = create_fake_team()

    for i in range(100):
        bot_user = User()
        bot_user.role = 1
        bot_user.steam_id = fake_steam_id + '_' + str(i)
        bot_user.nickname = fake_name + '_' + str(i)
        bot_user.profile_url = 'BotProfileURL'
        bot_user.avatar_url = 'BotAvatarURL'
        bot_user.team_id = fake_team.id
        bot_user.join_date = dt.utcnow()
        bot_user.last_online = dt.utcnow()
        bot_user.team_leader = 1
        db.session.add(bot_user)

    db.session.commit()
    return 'Created bots named after ' + fake_name, 200

def create_fake_team():
    fake_team = Team()
    fake_team.name = 'BotFakeTeam'
    fake_team.skill_level = "BotSkillLevel"
    fake_team.time_zone = "BotTimeZone"
    fake_team.reputation = 1
    db.session.add(fake_team)
    db.session.commit()
    return Team.query.filter_by(name='BotFakeTeam').first()

@bots.route('/create_teams')
def bots_create_teams():
    """
    Create 100 bot teams
    """

    from datetime import datetime as dt
    
    time_in_milliseconds = dt.utcnow().strftime('%Y%m%d%H%M%S%f')
    fake_name = 'BotTeam_' + time_in_milliseconds

    for i in range(100):
        bot_team = Team()
        bot_team.name = fake_name + '_' + str(i)
        bot_team.skill_level = 'BotSkillLevel'
        bot_team.time_zone = 'BotTimeZone'
        bot_team.reputation = '-1'
        db.session.add(bot_team)

    db.session.commit()
    return 'Created bots named after ' + fake_name, 200