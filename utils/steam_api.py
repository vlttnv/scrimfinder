from scrim import scrim_app
from flask import json

import requests

def get_user_info(steam_id):
    """
    Return player summaries of the user with steam id = steam_id.

    Example:
    {
        u'steamid': u'steamid',
        u'personaname': u'personaname',
        ...
    }

    See: https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_.28v0002.29
    """

    api = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?'
    params = {
        'key': scrim_app.config['STEAM_API_KEY'],
        'steamids': steam_id,
        'format': json
    }
    user_info = requests.get(url=api, params=params)
    user_info_json = user_info.json()
    
    return user_info_json['response']['players'][0] or {}
