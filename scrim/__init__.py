from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.openid import OpenID

scrim_app = Flask(__name__)
scrim_app.config.from_pyfile('../config.py')

db = SQLAlchemy(scrim_app)
oid = OpenID(scrim_app)
admin = Admin(scrim_app, name='Scrim Finder')

from scrim import views, models
from models import User

admin.add_view(ModelView(User, db.session))