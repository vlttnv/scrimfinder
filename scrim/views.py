from scrim import scrim_app, oid, db, models, lm
from models import User, Team, Request, Membership
from flask import redirect, session, g, json, render_template, flash, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
import requests
import re
from sqlalchemy import func, and_
from forms import EditForm, CreateTeamForm, FilterTeamForm
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import OperationalError

# Steam Web APIs...

def get_steam_user_info(steam_id):
    get_player_summaries_api = \
    'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?'

    params = {
        'key': scrim_app.config['STEAM_API_KEY'],
        'steamids': steam_id,
        'format': json
    }

    response = requests.get(url=get_player_summaries_api, params=params)
    user_info = response.json()

    return user_info['response']['players'][0] or {}

def get_recently_played_games(steam_id):
    get_recently_played_games_api = \
    'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?'

    params = {
        'key': scrim_app.config['STEAM_API_KEY'],
        'steamid': steam_id, 
        'format': json
    }

    response = requests.get(url=get_recently_played_games_api, params=params)
    recently_played_games = response.json()

    return recently_played_games['response'] or {}

@scrim_app.route('/')
@scrim_app.route('/index')
def index():
    """
    Home page. empty for now.
    """

    nname = None
    if g.user is not None:
        nname = g.user.nickname

    return render_template('index.html',user=nname)

@scrim_app.route('/login')
@oid.loginhandler
def login():
    """
    Logs in using steam.
    """

    if g.user is not None:
        return redirect(oid.get_next_url())
    else:
        return oid.try_login('http://steamcommunity.com/openid')

@oid.after_login
def after_login(resp):
    """
    Called after successful log in.
    Creates a new user or gets the existing one
    """

    steam_id_regex = re.compile('steamcommunity.com/openid/id/(.*?)$')
    steam_id = steam_id_regex.search(resp.identity_url).group(1)

    from datetime import datetime as dt

    try:
        g.user = User.query.filter_by(steam_id=steam_id).one()
    except NoResultFound:
        g.user = User()
        steam_data = get_steam_user_info(steam_id)
        g.user.steam_id     = steam_id
        g.user.nickname     = steam_data['personaname']
        g.user.profile_url  = steam_data['profileurl']
        g.user.avatar_url   = steam_data['avatar']
        g.user.join_date    = dt.utcnow()
        g.user.last_online  = dt.utcnow()
        db.session.add(g.user)
    
    last_online = g.user.last_online
    # do something

    g.user.last_online = dt.utcnow()
    db.session.commit()
    login_user(g.user)
    return redirect(oid.get_next_url())

@scrim_app.before_request
def before_request():
    """
    This gets called before each request and checks the session.
    Will probably do more stuff.
    """

    g.user = None
    if 'user_id' in session:
        g.user = User.query.filter_by(id=session['user_id']).first()

@scrim_app.route('/logout')
def logout():
    logout_user()
    flash("Logged out")
    return redirect(url_for('index'))

@scrim_app.route('/user/<steam_id>')
def user_page(steam_id):
    try:
        user = User.query.filter_by(steam_id=steam_id).one()
    except NoResultFound:
        flash('User not found')
        return redirect(url_for('index'))

    team_info = {}

    teams = Team.query.join(Membership).filter_by(user_id=user.id).all()

    if user.team_id is not None:
        print user.team_id
        try:
            team = Team.query.filter_by(id=user.team_id).one()
            team_info['id'] = team.id
            team_info['name'] = team.name
            team_info['skill'] = team.skill_level
            team_info['time_zone'] = team.time_zone
        except MultipleResultsFound as e:
            print e
        except NoResultFound as e:
            print e

    return render_template('user.html',
            id=user.steam_id,
            nick=user.nickname,
            profile_url=user.profile_url,
            avatar=user.avatar_url,
            mems=teams)

@scrim_app.route('/users')
@scrim_app.route('/users/page/<int:page>')
def show_all_users(page=1):
    """
    Retrieve all users of the application, 50 results per page
    """

    if page < 1:
        abort(404)

    from config import USERS_PER_PAGE
    try:
        users_list = User.query.paginate(page, per_page=USERS_PER_PAGE)
    except OperationalError: # no user in db
        users_list = None
    
    return render_template('all_users.html', users_list=users_list)

@scrim_app.route('/teams', methods=['GET', 'POST'])
@scrim_app.route('/teams/page/<int:page>', methods=['GET', 'POST'])
def show_all_teams(page=1):
    if page < 1:
        abort(404)

    query = Team.query
    form = FilterTeamForm()
    if form.validate_on_submit():
        if form.team_name != "":
            query = query.filter(Team.name.like('%'+form.team_name.data+'%'))
        if form.team_skill_level.data != "ALL":
            query = query.filter_by(skill_level=form.team_skill_level.data)
        if form.team_time_zone.data != "ALL":
            query = query.filter_by(time_zone=form.team_time_zone.data)

    from config import TEAMS_PER_PAGE
    try:
        teams_list = query.paginate(page, per_page=TEAMS_PER_PAGE)
    except OperationalError: # no team in db
        teams_list = None
    
    return render_template('all_teams.html', teams_list=teams_list, form=form)
    
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@scrim_app.route('/edit_profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm()
    if form.validate_on_submit():
        #g.user.team_name = form.team_name.data
        #g.user.team_skill_level = form.team_skill_level.data
        #g.user.team_time_zone = form.team_time_zone.data
        #db.session.add(g.user)
        #db.session.commit()
        #flash('Your changes have been saved')
        return redirect(url_for('user_page', steam_id=g.user.steam_id))
    else:
        #form.team_name.data = g.user.team_name
        #form.team_skill_level.data = g.user.team_skill_level
        #form.team_time_zone.data = g.user.team_time_zone
        #times.day.data = aval.day
        #times.time_from.data = aval.time_from
        #times.time_to.data = aval.time_to
        return render_template('edit_profile.html', form = form)

@scrim_app.route('/create_team', methods = ['GET', 'POST'])
@login_required
def create_team():
    create_team_form = CreateTeamForm()

    if g.user.team_id is not None:
        flash("You already have a team")
        return redirect(url_for('user_page', steam_id=g.user.steam_id))

    if create_team_form.validate_on_submit():
        new_team = Team()
        new_team.name = create_team_form.team_name.data
        new_team.skill_level = create_team_form.team_skill_level.data
        new_team.time_zone = create_team_form.team_time_zone.data
        db.session.add(new_team)
        db.session.commit()
        mem = Membership()
        mem.team_id = new_team.id
        mem.user_id = g.user.id
        mem.role = "Leader"
        db.session.add(mem)
        db.session.commit()
        return redirect(url_for('user_page', steam_id=g.user.steam_id))
    else:
        return render_template('create_team.html', create_team_form=create_team_form)

@scrim_app.route('/team/<team_id>')
def team_page(team_id):
    try:
        team = Team.query.filter_by(id=team_id).one()
        members = User.query.join(Membership).filter_by(team_id=team_id).all()
        
        #
        #   This can be optimized by first filtering then joining
        #
        pendings = User.query.join(Request).filter(User.id==Request.user_id).filter(Request.team_id==team_id).all()

    except NoResultFound, e:
        flash("Team not found")
        return redirect(url_for('index'))
    return render_template('team.html',
          team_name=team.name,
          team_skill=team.skill_level,
          team_zone=team.time_zone,
          members=members,
          team_id=team.id,
          pendings=pendings)

@scrim_app.route('/team/join/<team_id>')
@login_required
def team_join(team_id):
    try:
        user = User.query.filter_by(id=g.user.id).one()
    except NoResultFound, e:
        flash("User not found")
        return redirect(url_for('index'))
    
    req = Request()
    req.team_id = team_id
    req.user_id = user.id





    #user.team_id=team_id
    db.session.add(req)
    db.session.commit()
    flash("Request made")
    return redirect(url_for('team_page', team_id=team_id))

@scrim_app.route('/team/<team_id>/accept_user/<user_id>')
@login_required
def team_accept_user(team_id, user_id):
    try:
        user = Request.query.filter(and_(Request.team_id==team_id, Request.user_id==user_id)).one()
    except NoResultFound, e:
        flash("No user")
        return redirect(url_for('index'))

    db.session.delete(user)
    db.session.commit()

    #try:
    #    new_user = User.query.filter_by(id=user_id).one()
    #    
    #except NoResultFound, e:
    #    flash("No user")
    #    return redirect(url_for('index'))

    new_membership = Membership()
    new_membership.user_id = user_id
    new_membership.team_id = team_id
    new_membership.role = "Member"

    #new_user.team_id = team_id
    db.session.add(new_membership)
    db.session.commit()
    
    flash("Accepted")
    return redirect(url_for('team_page', team_id=team_id))


               

@scrim_app.route('/bots/boom')
def bots_create_users():
    """
    Create 100 bot users.
    """

    from datetime import datetime as dt
    import random
    
    time_in_milliseconds = dt.utcnow().strftime('%Y%m%d%H%M%S%f')
    fake_steam_id = 'BotSteamID_' + time_in_milliseconds
    fake_name = 'BotUser_' + time_in_milliseconds
    fake_team_ids = bots_create_fake_teams()

    for i in range(100):
        bot_user = User()
        bot_user.role = 1
        bot_user.steam_id = fake_steam_id + '_' + str(i)
        bot_user.nickname = fake_name + '_' + str(i)
        bot_user.profile_url = 'BotProfileURL'
        bot_user.avatar_url = 'BotAvatarURL'
        bot_user.team_id = random.choice(fake_team_ids)
        bot_user.join_date = dt.utcnow()
        bot_user.last_online = dt.utcnow()
        bot_user.team_leader = 1
        db.session.add(bot_user)

    db.session.commit()
    return 'Created bots named after ' + fake_name, 200

def bots_create_fake_teams():
    """
    Create 10 fake teams
    """

    from consts import SKILL_LEVEL, TIME_ZONE
    import random

    fake_name = 'BotTeam'
    fake_team_ids = []

    for skill in SKILL_LEVEL:
        for time in TIME_ZONE:
            bot_team = Team()
            bot_team.name = fake_name + '_' + str(skill) + '_' + str(time)
            bot_team.skill_level = skill
            bot_team.time_zone = time
            bot_team.reputation = '42'
            db.session.add(bot_team)
            db.session.flush()
            fake_team_ids.append(bot_team.id)
    db.session.commit()
    
    return fake_team_ids
