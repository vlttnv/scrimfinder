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

    if 'user_id' in session:
        g.user = User.query.filter_by(id=session['user_id']).first()
    #    g.user = User.query.get(session['user_id'])
        print ('You are logged in as %s' % g.user.steam_id)
    return render_template('index.html')

_steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')

@scrim_app.route('/login')
@oid.loginhandler
def login():
    """
    Logs in using steam.
    """

    if g.user is not None:
        return redirect(oid.get_next_url())
    return oid.try_login('http://steamcommunity.com/openid')

@oid.after_login
def create_or_login(resp):

    """
    Called after successful log in.
    Creates a new user or gets the existing one
    """

    match = _steam_id_re.search(resp.identity_url)
    g.user = User.get_or_create(match.group(1))
    steam_data = get_steam_userinfo(g.user.steam_id)
    g.user.nickname = steam_data['personaname']
    print g.user.steam_id
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
        g.user = User.query.get(session['user_id'])

@scrim_app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Your are logged out.')
    return redirect(oid.get_next_url())

@scrim_app.route('/user/<id>')
def user_page(id):
    user = User.query.filter_by(steam_id = id).first()
    if user == None:
        flash('User not found')
        return redirect(url_for('index'))
    return render_template('user.html',
            id = user.steam_id,
            nick = user.nickname)
