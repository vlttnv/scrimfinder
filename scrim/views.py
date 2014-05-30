from scrim import scrim_app, oid, db, models
from models import User
from flask import redirect, session, g, json, render_template, flash
import urllib
import urllib2
import re

def get_steam_userinfo(steam_id):
    options = {
        'key': scrim_app.config['STEAM_API_KEY'],
        'steamids': steam_id
    }
    url = 'http://api.steampowered.com/ISteamUser/' \
          'GetPlayerSummaries/v0001/?%s' % urllib.urlencode(options)
    rv = json.load(urllib2.urlopen(url))
    return rv['response']['players']['player'][0] or {}

@scrim_app.route('/')
@scrim_app.route('/index')
def index():
    return render_template('index.html')

_steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')

@scrim_app.route('/login')
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    return oid.try_login('http://steamcommunity.com/openid')

@oid.after_login
def create_or_login(resp):
    match = _steam_id_re.search(resp.identity_url)
    g.user = User.get_or_create(match.group(1))
    steamdata = get_steam_userinfo(g.user.steam_id)
    g.user.nickname = steamdata['personaname']
    db.session.commit()
    session['user_id'] = g.user.id
    flash('You are logged in as %s' % g.user.nickname)
    return redirect(oid.get_next_url())

@scrim_app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@scrim_app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(oid.get_next_url())
