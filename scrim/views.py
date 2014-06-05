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

def get_steam_userinfo(steam_id):
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
    #    flash('You are logged in as %s' % g.user.nickname)
        nname = g.user.nickname

    return render_template('index.html',
            user = nname)

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
def create_or_login(resp):
    """
    Called after successful log in.
    Creates a new user or gets the existing one
    """

    steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')
    match_steam_id = steam_id_re.search(resp.identity_url)
    
    g.user = User.get_or_create(match_steam_id.group(1))
    steam_data = get_steam_userinfo(g.user.steam_id)
    g.user.nickname     = steam_data['personaname']
    g.user.profile_url  = steam_data['profileurl']
    g.user.avatar_url   = steam_data['avatar']
    
    db.session.add(g.user)
    db.session.commit()
    #session['user_id'] = g.user.id
    login_user(g.user)
    #flash('You are logged in as %s' % g.user.nickname)
    
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
    #session.pop('user_id', None)
    #flash('Your are logged out.')
    
    return redirect(oid.get_next_url())

@scrim_app.route('/user/<steam_id>')
def user_page(steam_id):
    user = User.query.filter_by(steam_id=steam_id).one()
    if user == None:
        flash('User not found')
        return redirect(url_for('index'))
    
    recently_played_games = get_recently_played_games(steam_id)

    if g.user.team_id is not None:
        try:
            team = Team.query.filter_by(id=g.user.team_id).one()
            a_team_name = team.name
            a_team_skill = team.skill_level
            a_team_zone = team.time_zone
            a_team_id = team.id
        except MultipleResultsFound, e:
            print e
        except NoResultFound, e:
            print e

    return render_template('user.html',
            id=user.steam_id,
            nick=user.nickname,
            profile_url=user.profile_url,
            avatar=user.avatar_url,
            recently_played_games=recently_played_games,
            team_name=a_team_name,
            skill_level=a_team_skill,
            time_zone=a_team_zone,
            teamid=a_team_id)

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
    
    return render_template('all_users.html',
        users_list=users_list)

# Use with care
@scrim_app.route('/create_test_bots')
def create_test_bots():
    """
    Create 100 test bots.
    """

    from datetime import datetime as dt
    
    time_in_milliseconds = dt.utcnow().strftime('%Y%m%d%H%M%S%f')
    bot_steam_id = 'BOT_STEAM_ID_' + time_in_milliseconds
    bot_nickname = 'BOT_' + time_in_milliseconds

    for i in range(100):
        new_bot = User.get_or_create(bot_steam_id)
        new_bot.nickname = bot_nickname + ' ' + str(i)
        new_bot.profile_url = 'BOT_PROFILE_URL'
        new_bot.avatar_url = 'BOT_AVATAR_URL'
        db.session.add(new_bot)
    db.session.commit()

    return 'Created bots named after ' + bot_nickname, 200

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
def team(team_id):
    try:
        team = Team.query.filter_by(id=team_id).one()
    except NoResultFound, e:
        flash("Team not found")
        return redirect(url_for('index'))
    return render_template('team.html',
          team_name=team.name,
          team_skill=team.skill_level,
          team_zone=team.time_zone)

