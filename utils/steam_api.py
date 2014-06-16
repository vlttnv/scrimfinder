from scrim import scrim_app
from flask import json

import requests

def get_user_info(steam_id):
    """
    """

    get_player_summaries_api = \
    'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?'

    params = {
        'key': scrim_app.config['STEAM_API_KEY'],
        'steamids': steam_id,
        'format': json
    }

    response = requests.get(url=get_player_summaries_api, params=params)
    user_info = response.json()

    print user_info['response']['players'][0]

    return user_info['response']['players'][0] or {}

def get_recently_played_games(steam_id):
    """
    """

    get_recently_played_games_api = \
    'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?'

    params = {
        'key': scrim_app.config['STEAM_API_KEY'],
        'steamid': steam_id, 
        'format': json
    }

    response = requests.get(url=get_recently_played_games_api, params=params)
    recently_played_games = response.json()

    print recently_played_games['response']

    return recently_played_games['response'] or {}