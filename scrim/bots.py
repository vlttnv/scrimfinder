from scrim import db, models
from models import User, Team
from utils import utils
import random

def create_bot_users():
    """
    Create 100 bot users.
    """

    from datetime import datetime as dt
    
    current_time = dt.utcnow().strftime('%Y%m%d%H%M%S%f')[-10:]
    fake_steam_id = '@_SteamID_' + current_time
    fake_name = '@_User' + current_time

    for i in range(100):
        bot_user = User()
        bot_user.steam_id = fake_steam_id + '_' + str(i)
        bot_user.nickname = fake_name + '_' + str(i)
        bot_user.profile_url = '@_ProfileURL'
        bot_user.avatar_url = '@_AvatarURL'
        bot_user.join_date = dt.utcnow()
        bot_user.last_online = dt.utcnow()
        bot_user.team_leader = False
        db.session.add(bot_user)

    db.session.commit()

def create_bot_teams():
    """
    Create enough teams - all possible combinations of skill level, 
    time zone, scrim time, etc.
    """

    from consts import SKILL_LEVEL, TIME_ZONE

    fake_name = '@_Team'

    for skill in SKILL_LEVEL:
        for time in TIME_ZONE:
            possible_weekdays = utils.get_bit_combinations("0000000")
            for weekday in possible_weekdays:
                bot_team = Team()
                bot_team.name = fake_name + '_' + str(skill) + '_' + str(time) + '_' + str(weekday)
                bot_team.skill_level = skill
                bot_team.time_zone = time
                bot_team.reputation = '42'
                bot_team.week_days = weekday
                db.session.add(bot_team)
    
    db.session.commit()

def make_bot_join_team():
    """
    Get all users to join some team
    """

    all_users = User.query.filter(User.nickname.startswith('@_User')).all()
    all_teams = Team.query.filter(Team.name.startswith('@_Team')).all()

    # TODO: make bot users join team
