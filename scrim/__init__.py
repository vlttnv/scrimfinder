from flask import Flask, redirect, session, json, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID

scrim_app = Flask(__name__)
scrim_app.config.from_pyfile('../config.py')
db = SQLAlchemy(scrim_app)
oid = OpenID(scrim_app)
from scrim import views
