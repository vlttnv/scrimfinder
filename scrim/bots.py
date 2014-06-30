from scrim import db, models
from models import User, Team, Scrim

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

    from consts import CHOICES_SKILLS, CHOICES_ZONES
    from utils import scrim_filter

    fake_name = '@_Team'

    for skill,_ in CHOICES_SKILLS:
        for time,_ in CHOICES_ZONES:
            combinations = scrim_filter.scrim_days_combinations('0000000')
            for scrim_days in combinations:
                bot_team = Team()
                bot_team.name = fake_name + '_' + str(skill) + '_' + str(time) + '_' + str(scrim_days)
                bot_team.skill_level = skill
                bot_team.time_zone = time
                bot_team.reputation = '42'
                bot_team.week_days = scrim_days
                db.session.add(bot_team)
    
    db.session.commit()

def make_bot_join_team():
    """
    Get all users to join some team
    """

    all_users = User.query.filter(User.nickname.startswith('@_User')).all()
    all_teams = Team.query.filter(Team.name.startswith('@_Team')).all()

    # TODO: make bot users join team

def create_scrims():

    from consts import UGC_PLATINUM
    from consts import SCRIM_PROPOSED, SCRIM_ACCEPTED, SCRIM_REJECTED, SCRIM_FINISHED
    from datetime import datetime, timedelta

    team1 = Team()
    team1.name = 'Scrim Team 1'
    team1.skill_level = UGC_PLATINUM
    team1.time_zone = "CET"
    db.session.add(team1)

    team2 = Team()
    team2.name = 'Scrim Team 2'
    team2.skill_level = UGC_PLATINUM
    team2.time_zone = "CET"
    db.session.add(team2)

    db.session.flush()

    now = datetime.utcnow()

    scrim_proposed = Scrim()
    scrim_proposed.date     = now
    scrim_proposed.map1     = 'Team Map1'
    scrim_proposed.team1_id = team1.id
    scrim_proposed.team1    = team1
    scrim_proposed.team2_id = team2.id
    scrim_proposed.team2    = team2
    scrim_proposed.type     = 'Proposed by Team 1'
    scrim_proposed.state    = SCRIM_PROPOSED
    db.session.add(scrim_proposed)

    another_day = now - timedelta(days=now.weekday() + 4)
    scrim_proposed2 = Scrim()
    scrim_proposed2.date     = another_day
    scrim_proposed2.map1     = 'Team Map2'
    scrim_proposed2.team1_id = team2.id
    scrim_proposed2.team1    = team2
    scrim_proposed2.team2_id = team1.id
    scrim_proposed2.team2    = team1
    scrim_proposed2.type     = 'Proposed by Team 2'
    scrim_proposed2.state    = SCRIM_PROPOSED
    db.session.add(scrim_proposed2)

    another_day = now - timedelta(days=now.weekday() + 3)
    scrim_accepted = Scrim()
    scrim_accepted.date     = another_day
    scrim_accepted.map1     = 'Team Map1'
    scrim_accepted.map2     = 'Team Map2'
    scrim_accepted.team1_id = team1.id
    scrim_accepted.team1    = team1
    scrim_accepted.team2_id = team2.id
    scrim_accepted.team2    = team2
    scrim_accepted.type     = 'Accepted by Team 2'
    scrim_accepted.state    = SCRIM_ACCEPTED
    db.session.add(scrim_accepted)

    another_day = now - timedelta(days=now.weekday() + 2)
    scrim_rejected = Scrim()
    scrim_rejected.date     = another_day
    scrim_rejected.map1     = 'Team Map1'
    scrim_rejected.map2     = 'Team Map2'
    scrim_rejected.team1_id = team1.id
    scrim_rejected.team1    = team1
    scrim_rejected.team2_id = team2.id
    scrim_rejected.team2    = team2
    scrim_rejected.type     = 'Rejected by Team 2'
    scrim_rejected.state    = SCRIM_REJECTED
    db.session.add(scrim_rejected)

    another_day = now - timedelta(days=now.weekday() + 1)
    scrim_finished = Scrim()
    scrim_finished.date     = another_day
    scrim_finished.map1     = 'Team Map1'
    scrim_finished.map2     = 'Team Map2'
    scrim_finished.team1_id = team1.id
    scrim_finished.team1    = team1
    scrim_finished.team2_id = team2.id
    scrim_finished.team2    = team2
    scrim_finished.type     = 'Won by Team 1'
    scrim_finished.result   = 'Won'
    scrim_finished.state    = SCRIM_FINISHED
    db.session.add(scrim_finished)

    db.session.commit()

def create_accepted_scrim():
    from consts import UGC_PLATINUM
    from consts import SCRIM_ACCEPTED
    from datetime import datetime, timedelta
    
    team1 = Team()
    team1.name = "Team Test Finished Scrim1"
    team1.skill_level = UGC_PLATINUM
    team1.time_zone = "CET"
    db.session.add(team1)

    team2 = Team()
    team2.name = "Team Test Finished Scrim2"
    team2.skill_level = UGC_PLATINUM
    team2.time_zone = "CET"
    db.session.add(team2)

    now = datetime.utcnow()
    past_day = now - timedelta(days=now.weekday() - 4)

    scrim_accepted = Scrim()
    scrim_accepted.date     = past_day
    scrim_accepted.map1     = "Map1"
    scrim_accepted.map2     = "Map2"
    scrim_accepted.team1_id = team1.id
    scrim_accepted.team1    = team1
    scrim_accepted.team2_id = team2.id
    scrim_accepted.team2    = team2
    scrim_accepted.type     = "Accepted scrim"
    scrim_accepted.state    = SCRIM_ACCEPTED
    db.session.add(scrim_accepted)

    db.session.commit()

    return team1.id