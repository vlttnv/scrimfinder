from scrim import scrim_app, oid, db, models
from models import User
from flask import redirect, session, g, json, render_template, flash, url_for
import requests
import re
from sqlalchemy import func

def get_steam_userinfo(steam_id):
    get_player_summaries_api = {
        'key': scrim_app.config['STEAM_API_KEY'],
        'steamids': steam_id,
        'format': json
    }

    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?'
    response = requests.get(url=url, params=get_player_summaries_api)
    user_info = response.json()

    return user_info['response']['players'][0] or {}

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
    session['user_id'] = g.user.id
    flash('You are logged in as %s' % g.user.nickname)
    
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
    session.pop('user_id', None)
    flash('Your are logged out.')
    
    return redirect(oid.get_next_url())

@scrim_app.route('/user/<steam_id>')
def user_page(steam_id):
    user = User.query.filter_by(steam_id=steam_id).first()
    if user == None:
        flash('User not found')
        return redirect(url_for('index'))
    return render_template('user.html',
            id=user.steam_id,
            nick=user.nickname,
            profile_url=user.profile_url,
            avatar=user.avatar_url)

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
