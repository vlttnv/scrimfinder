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
#lm.init_app(scrim_app)

from scrim import views, models, momentjs
from models import User

admin.add_view(ModelView(User, db.session))
lm.init_app(scrim_app)
scrim_app.jinja_env.globals['momentjs'] = momentjs
