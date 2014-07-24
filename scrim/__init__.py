from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask.ext.login import LoginManager

scrim_app = Flask(__name__)
scrim_app.config.from_pyfile('../config.py')

lm      = LoginManager()
db      = SQLAlchemy(scrim_app)
oid     = OpenID(scrim_app)

lm.init_app(scrim_app)

from scrim import views, models
from models import User, Team, Scrim

@scrim_app.context_processor
def utility_processor():
    def convert_days(bit_string):
        days_of_week = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        aval = [day for day, bit in zip(days_of_week, bit_string) if bit == '1']
        return aval
    def get_time_zone_label(time_zone):
		from consts import TIME_ZONES_DICT
		for item in TIME_ZONES_DICT:
			if item['time_zone'] == time_zone:
				return item['label']
		return None
    return dict(convert_days=convert_days, get_time_zone_label=get_time_zone_label)

# Blueprints - Not Working
# from scrim.teams.views import teams as teams_module
# scrim_app.register_blueprint(teams_module, url_prefix='/teams')
# print scrim_app.url_map
# from scrim.bots.views import bots as bots_module
# scrim_app.register_blueprint(bots_module, url_prefix='/bots')
