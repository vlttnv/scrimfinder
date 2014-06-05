from flask import Blueprint, render_template
from scrim.models import Team

teams = Blueprint('teams', __name__)

@teams.route('/')
@teams.route('/page/<int:page>')
def show_all_teams(page=1):
    if page < 1:
        abort(404)

    from config import TEAMS_PER_PAGE
    teams_list = Team.query.paginate(page, TEAMS_PER_PAGE, False)
    
    return render_template('all_teams.html', teams_list=teams_list)