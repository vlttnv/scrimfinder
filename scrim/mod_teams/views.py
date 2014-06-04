from flask import Blueprint

mod_teams = Blueprint('mod_teams', __name__)

@mod_teams.route('/')
def show_teams():
	return 'Sup nigger', 200