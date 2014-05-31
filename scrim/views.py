from scrim import scrim_app, oid, db, models
from models import User
from flask import redirect, session, g, json, render_template, flash
import requests
import re

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

    if g.user is not None:
        flash('You are logged in as %s' % g.user.personaname)
    
    return render_template('index.html')

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
    g.user.personaname = steam_data['personaname']
    
    db.session.commit()
    session['user_id'] = g.user.id
    flash('You are logged in as %s' % g.user.personaname)
    
    return redirect(oid.get_next_url())

@scrim_app.before_request
def before_request():
    """
    This gets called before each request and checks the session.
    Will probably do more stuff.
    """

    g.user = None
    if 'user_id' in session:
        user_object = User.query.get(session['user_id'])
        print user_object
        g.user = User.query.filter_by(id=session['user_id']).first()

@scrim_app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Your are logged out.')
    
    return redirect(oid.get_next_url())
