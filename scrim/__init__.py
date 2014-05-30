from flask import Flask

scrim_app = Flask(__name__)
from scrim import views
