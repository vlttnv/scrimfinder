from scrim import scrim_app, oid, db, models, lm
from models import User, Team
from flask import redirect, session, g, json, render_template, flash, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
import requests
import re
from sqlalchemy import func
from forms import EditForm, CreateTeamForm
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

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
            team_info=team_info)

@scrim_app.route('/all_users')
@scrim_app.route('/all_users/page/<int:page>')
def show_all_users(page=1):
    """
    Retrieve all users of the application, 50 results per page
    """

    if page < 1:
        abort(404)

    from config import USERS_PER_PAGE
    users_list = User.query.paginate(page, USERS_PER_PAGE, False)
    
    return render_template('all_users.html', users_list=users_list)

@scrim_app.route('/teams')
@scrim_app.route('/teams/page/<int:page>')
def show_all_teams(page=1):
    if page < 1:
        abort(404)

    from config import TEAMS_PER_PAGE
    teams_list = Team.query.paginate(page, TEAMS_PER_PAGE, False)
    
    return render_template('all_teams.html', teams_list=teams_list)

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
        g.user.team_id = new_team.id
        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for('user_page', steam_id=g.user.steam_id))
    else:
        return render_template('create_team.html', create_team_form=create_team_form)

@scrim_app.route('/team/<team_id>')
def team_page(team_id):
    try:
        team = Team.query.filter_by(id=team_id).one()
    except NoResultFound, e:
        flash("Team not found")
        return redirect(url_for('index'))
    return render_template('team.html',
          team_name=team.name,
          team_skill=team.skill_level,
          team_zone=team.time_zone)

