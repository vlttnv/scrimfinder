from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.openid import OpenID
from flask.ext.login import LoginManager

scrim_app = Flask(__name__)
scrim_app.config.from_pyfile('../config.py')

lm      = LoginManager()
db      = SQLAlchemy(scrim_app)
oid     = OpenID(scrim_app)
admin   = Admin(scrim_app, name='Scrim Finder')

lm.init_app(scrim_app)

from scrim import views, models
from models import User, Team, Scrim

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Team, db.session))
admin.add_view(ModelView(Scrim, db.session))

@scrim_app.context_processor
def utility_processor():
    def convert_days(bit_string):
        days_of_week = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        aval = [day for day, bit in zip(days_of_week, bit_string) if bit == '1']
        return aval
    return dict(convert_days=convert_days)

# Blueprints - Not Working
# from scrim.teams.views import teams as teams_module
# scrim_app.register_blueprint(teams_module, url_prefix='/teams')
# print scrim_app.url_map
# from scrim.bots.views import bots as bots_module
# scrim_app.register_blueprint(bots_module, url_prefix='/bots')
