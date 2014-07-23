from scrim import scrim_app
from flask import json

import requests

def get_match_result(team_blue, log_id):
    """
    Return match result, either "Tied", "Won", "Lost", or "Unknown".

    team_blue: boolean
    log_id: logs.tf log id
    """

    api = "http://logs.tf/json/" + str(log_id)
    match_info = requests.get(url=api)

    if match_info.status_code == 200:
        match_info_json = match_info.json()
    else:
        return "Unknown"
    
    team_red = not team_blue
    try:
        blue_score = match_info_json["teams"]["Blue"]["score"]
        red_score = match_info_json["teams"]["Red"]["score"]
    except KeyError:
        return "Unknown"

    if (blue_score == red_score):
        return "Tied"
    if (team_blue == True and blue_score > red_score):
        return "Won"
    elif (team_blue == True and blue_score < red_score):
        return "Lost"
    elif (team_red == True and red_score > blue_score):
        return "Won"
    elif (team_red == True and red_score < blue_score):
        return "Lost"
    else:
        return "Unknown"
