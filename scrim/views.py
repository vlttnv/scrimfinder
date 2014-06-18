from scrim import scrim_app, oid, db, models, lm
from models import User, Team, Request, Membership, Comment, Scrim
from utils import steam_api
from consts import *
from flask import request, redirect, session, g, json, render_template, flash, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
import requests
import re
from sqlalchemy import func, and_, or_, desc
from forms import UserEditForm, CreateTeamForm, TeamEditForm, FilterTeamForm, \
    FilterScrimForm, TeamCommentForm, ProposeScrimForm, AcceptScrimForm
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import OperationalError

#========================
# Helper function
#========================

def map_days(days):
        # Map a list of words to the "bit string"
        # Maybe there's a shorter and cleverer way to do it
        # but we wont show it to Tristan so that's fine
        words = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday", "Sunday"]
        aval = [(word if int(day)==1 else False) 
                for day,word in zip(days,words)]
        return aval

@scrim_app.route('/')
@scrim_app.route('/index')
def index():
    """
    Home page. empty for now.
    """

    nname = None
    if g.user is not None:
        nname = g.user.nickname

    return render_template('index.html',user=nname)

@scrim_app.route('/login')
@oid.loginhandler
def login():
    """
    Logs in using steam.
    """

    if g.user is not None:
        return redirect(oid.get_next_url())
    else:
        return oid.try_login('http://steamcommunity.com/openid')

@oid.after_login
def after_login(resp):
    """
    Called after successful log in.
    Creates a new user or gets the existing one
    """

    from datetime import datetime as dt
    from utils import steam_api

    steam_id_regex = re.compile('steamcommunity.com/openid/id/(.*?)$')
    steam_id = steam_id_regex.search(resp.identity_url).group(1)

    try:
        g.user = User.query.filter_by(steam_id=steam_id).one()
    except NoResultFound:
        g.user = User()
        steam_data              = steam_api.get_user_info(steam_id)
        g.user.steam_id         = steam_id
        g.user.nickname         = steam_data['personaname']
        g.user.profile_url      = steam_data['profileurl']
        g.user.avatar_url       = steam_data['avatar']
        g.user.avatar_url_full  = steam_data['avatarfull']
        g.user.join_date        = dt.utcnow()
        g.user.last_online      = dt.utcnow()
        db.session.add(g.user)
    
    last_online = g.user.last_online
    # do something

    g.user.last_online = dt.utcnow()
    db.session.commit()
    login_user(g.user)
    return redirect(oid.get_next_url())

@scrim_app.before_request
def before_request():
    """
    This gets called before each request and checks the session.
    Will probably do more stuff.
    """

    if 'user_id' in session:
        g.user = User.query.filter_by(id=session['user_id']).first()
    else:
        g.user = None

@scrim_app.route('/logout')
def logout():
    logout_user()
    flash("Logged out")
    return redirect(url_for('index'))

@scrim_app.route('/user/<steam_id>')
def user_page(steam_id):
    try:
        user = User.query.filter_by(steam_id=steam_id).one()
    except NoResultFound:
        flash('User not found')
        return redirect(url_for('index'))

    # array of tuples of Team and role e.g. [(team,"Captain"),(team,"Coach")]
    teams_roles = []
    memberships = Membership.query.filter_by(user_id=user.id).all()
    for mem in memberships:
        team = Team.query.filter_by(id=mem.team_id).one()
        teams_roles.append((team, mem.role))

    return render_template('user.html',
            id=user.steam_id,
            nick=user.nickname,
            profile_url=user.profile_url,
            avatar=user.avatar_url,
            avatar_full=user.avatar_url_full,
            teams_roles=teams_roles)

@scrim_app.route('/users')
@scrim_app.route('/users/page/<int:page>')
def show_all_users(page=1):
    """
    Retrieve all users of the application, 50 results per page
    """

    if page < 1:
        abort(404)

    from config import USERS_PER_PAGE
    try:
        users_list = User.query.paginate(page, per_page=USERS_PER_PAGE)
    except OperationalError: # no user in db
        users_list = None
    
    return render_template('all_users.html', users_list=users_list)

@scrim_app.route('/teams', methods=['GET','POST'])
@scrim_app.route('/teams/page/<int:page>', methods=['GET','POST'])
def show_all_teams(page=1):
    if page < 1:
        abort(404)

    query = Team.query

    form = FilterTeamForm()
    if form.validate_on_submit():
        if form.team_name != "":
            query = query.filter(Team.name.like('%'+form.team_name.data+'%'))
        if form.team_skill_level.data != "ALL":
            query = query.filter_by(skill_level=form.team_skill_level.data)
        if form.team_time_zone.data != "ALL":
            query = query.filter_by(time_zone=form.team_time_zone.data)

    from config import TEAMS_PER_PAGE
    try:
        teams_list = query.paginate(page, per_page=TEAMS_PER_PAGE)
    except OperationalError: # no team in db
        teams_list = None
    
    return render_template('all_teams.html', teams_list=teams_list, form=form)

@scrim_app.route('/scrims/', methods=['GET','POST'])
@scrim_app.route('/scrims/page/<int:page>', methods=['GET','POST'])
@login_required
def show_all_scrims(page=1):
    """
    Scrim search page. Only visible for users who are part of a team
    """

    if page < 1:
        abort(404)

    form = FilterScrimForm()

    player_memberships = Membership.query.filter_by(user_id=g.user.id).all()
    if len(player_memberships) == 0:
        flash('You are not in a team. Cannot search for scrims.')
        return render_template('all_scrims.html', teams_list=None, form=form)

    # Ignore your own teams
    query = Team.query
    for mem in player_memberships:
            query = query.filter(Team.id != mem.team_id)

    from utils import scrim_filter
    if page == 1 and form.clear.data == True:
        form.team_skill_level.data = 'ALL'
        form.team_time_zone.data = 'ALL'
        form.mon.data = False
        form.tue.data = False
        form.wed.data = False
        form.thu.data = False
        form.fri.data = False
        form.sat.data = False
        form.sun.data = False
        form.clear.data = False
    elif form.validate_on_submit():
        if form.team_skill_level.data != 'ALL':
            query = query.filter_by(skill_level=form.team_skill_level.data)
        if form.team_time_zone.data != 'ALL':
            query = query.filter_by(time_zone=form.team_time_zone.data)

        scrim_days = form.read_scrim_days()
        matched_scrim_days = scrim_filter.scrim_days_combinations(scrim_days)
        query = query.filter(Team.week_days.in_(matched_scrim_days))
    else:
        # HACK - set default values using the player's 1st team info
        try:
            player_1st_team_id = player_memberships[0].team_id
            player_1st_team = Team.query.filter_by(id=player_1st_team_id).one()

            form.team_skill_level.data = player_1st_team.skill_level
            form.team_time_zone.data = player_1st_team.time_zone

            query = query.filter_by(skill_level=player_1st_team.skill_level)            
            query = query.filter_by(time_zone=player_1st_team.time_zone)
        
            scrim_days = player_1st_team.week_days
           
            form.mon.data = bool(int(scrim_days[0]))
            form.tue.data = bool(int(scrim_days[1]))
            form.wed.data = bool(int(scrim_days[2]))
            form.thu.data = bool(int(scrim_days[3]))
            form.fri.data = bool(int(scrim_days[4]))
            form.sat.data = bool(int(scrim_days[5]))
            form.sun.data = bool(int(scrim_days[6]))

            matched_scrim_days = scrim_filter.scrim_days_combinations(scrim_days)
            query = query.filter(Team.week_days.in_(matched_scrim_days))
        except NoResultFound as e:
            print e

    from config import TEAMS_PER_PAGE
    try:
        teams_list = query.paginate(page, per_page=TEAMS_PER_PAGE)
    except OperationalError:
        teams_list = None

    return render_template('all_scrims.html', teams_list=teams_list, form=form)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@scrim_app.route('/edit_profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    """
    This can be done once the user model is finalized
    so that constat modifications are avoided
    """
    form = EditForm()
    if form.validate_on_submit():
        #g.user.team_name = form.team_name.data
        #g.user.team_skill_level = form.team_skill_level.data
        #g.user.team_time_zone = form.team_time_zone.data
        #db.session.add(g.user)
        #db.session.commit()
        #flash('Your changes have been saved')
        return redirect(url_for('user_page', steam_id=g.user.steam_id))
    else:
        #form.team_name.data = g.user.team_name
        #form.team_skill_level.data = g.user.team_skill_level
        #form.team_time_zone.data = g.user.team_time_zone
        #times.day.data = aval.day
        #times.time_from.data = aval.time_from
        #times.time_to.data = aval.time_to
        return render_template('edit_profile.html', form = form)

@scrim_app.route('/edit_team/<int:team_id>', methods = ['GET', 'POST'])
@login_required
def edit_team(team_id):
    """

    """
    has_right = False

    # Need to check if the user has the right to edit this team
    # Search through his memberships
    #teams = Team.query.join(Membership).filter_by(user_id=g.user.id).all()
    teams = Membership.query.filter_by(user_id=g.user.id).all()
    for team in teams:
        if team.team_id == int(team_id) and team.role == "Captain":
            has_right = True
    
    # Kick him out if not
    if not has_right:
        flash("You should not be here")
        return redirect(url_for('index'))

    # Get the team the is being edited
    try:
        team_edit = Team.query.filter_by(id=team_id).one()
    except NoResultFound, e:
        flash("Team not found")
        return redirect(url_for('index'))

    form = TeamEditForm()
    if form.validate_on_submit():
        team_edit.name = form.team_name.data
        team_edit.skill_level = form.team_skill_level.data
        team_edit.time_zone = form.team_time_zone.data

        # Make week string
        week = list("0000000")
        week[0] = str(int(form.mon.data))
        week[1] = str(int(form.tue.data))
        week[2] = str(int(form.wed.data))
        week[3] = str(int(form.thu.data))
        week[4] = str(int(form.fri.data))
        week[5] = str(int(form.sat.data))
        week[6] = str(int(form.sun.data))
        week = "".join(week)

        team_edit.time_from = form.time_from.data
        team_edit.week_days = week
        db.session.add(team_edit)
        db.session.commit()
        return redirect(url_for('team_page', team_id=team_id))
    else:
        wk = team_edit.week_days
        print wk
        form.team_name.data = team_edit.name
        form.team_skill_level.data = team_edit.skill_level
        form.team_time_zone.data = team_edit.time_zone
        form.time_from.data = team_edit.time_from
        form.mon.data = bool(int(wk[0]))
        form.tue.data = bool(int(wk[1]))
        form.wed.data = bool(int(wk[2]))
        form.thu.data = bool(int(wk[3]))
        form.fri.data = bool(int(wk[4]))
        form.sat.data = bool(int(wk[5]))
        form.sun.data = bool(int(wk[6]))
        return render_template('edit_team.html', form=form, team_id=team_id)

@scrim_app.route('/create_team', methods = ['GET', 'POST'])
@login_required
def create_team():
    """
    A user creates a new team and sets some team parameters
    The suer by default becomes the team leader
    """

    form = CreateTeamForm()

    user_membership = Membership.query.filter_by(user_id=g.user.id).all()
    if len(user_membership) == 3:
        flash('You are in three teams already. Chill.')
        return redirect(url_for('user_page', steam_id=g.user.steam_id))

    if form.validate_on_submit():
        new_team = Team()
        new_team.name = form.team_name.data
        new_team.skill_level = form.team_skill_level.data
        new_team.time_zone = form.team_time_zone.data

        week = list("0000000")
        week[0] = str(int(form.mon.data))
        week[1] = str(int(form.tue.data))
        week[2] = str(int(form.wed.data))
        week[3] = str(int(form.thu.data))
        week[4] = str(int(form.fri.data))
        week[5] = str(int(form.sat.data))
        week[6] = str(int(form.sun.data))
        week = "".join(week)
        new_team.week_days = week

        db.session.add(new_team)
        db.session.commit()
        mem = Membership()
        mem.team_id = new_team.id
        mem.user_id = g.user.id
        mem.role = "Captain" 
        db.session.add(mem)
        db.session.commit()
        return redirect(url_for('user_page', steam_id=g.user.steam_id))
    else:
        return render_template('create_team.html', create_team_form=form)

@scrim_app.route('/quit_team/<int:team_id>', methods=['POST'])
@login_required
def quit_team(team_id):
    if team_id < 1:
        abort(404)

    team_membership = None
    user_membership = Membership.query.filter_by(user_id=g.user.id).all()
    for membership in user_membership:
        if membership.team_id == team_id:
            team_membership = membership

    if team_membership is None:
        flash("Dude you are not in this team")
        redirect(url_for('user_page'), steam_id=g.user.steam_id)
    else:
        db.session.delete(team_membership)
        db.session.commit()

        user_team = Team.query.filter_by(id=team_id).one()
        user_team_name = user_team.name
        members = Team.query.join(Membership).filter_by(team_id=team_id).all()
        if len(members) == 0:
            db.session.delete(user_team)
            db.session.commit()
            flash("You quit from team " + user_team_name + " , and since \
                    there's no one left in the team, the team is deleted")
        else:
            flash("You quit from team " + user_team_name)
        return redirect(url_for('user_page', steam_id=g.user.steam_id))

@scrim_app.route('/team/<int:team_id>', methods=['GET','POST'])
def team_page(team_id):
    """
    Currently shows a specific team, with team parameters, current members
    and pending members

    The pending members view will be restricted to the team leader
    """

    form = TeamCommentForm()

    try:
        team = Team.query.filter_by(id=team_id).one()
    except NoResultFound as e:
        flash("Team not found")
        return redirect(url_for('index'))

    all_members = Membership.query.join(Team).filter_by(id=team_id).all()
    # an arry of tuples of User and role e.g. [(user,"Captain"),(user,"BenchPlayer")]
    members_roles = []
    for mem in all_members:
        user = User.query.filter_by(id=mem.user_id).one()
        members_roles.append((user, mem.role))

    #
    #   This can be optimized by first filtering then joining
    #
    pendings = User.query.join(Request).filter(User.id==Request.user_id) \
                .filter(Request.team_id==team_id).all()
    
    # Is the user in the team
    in_team = False
    if g.user in (x[0] for x in members_roles):
            in_team = True

    # propose scrim if and only if the user is not in the team & is a captain
    # of some team
    is_captain = False
    if g.user is not None:
        user_memberships = Membership.query.filter_by(user_id=g.user.id)
        for mem in user_memberships:
            if mem.role == 'Captain':
                is_captain = True
                break

    propose_scrim = False
    if in_team == False and is_captain:
        propose_scrim = True

    all_scrims = Scrim.query.filter(or_(Scrim.team1_id == team_id, Scrim.team2_id == team_id))
    all_scrims = all_scrims.order_by(desc(Scrim.date))
    scrims_list = []
    # {
    #   'state',
    #   'opponent',
    #   'scrim'
    # }

    # still need to cover scrim finished
    for scrim in all_scrims.all():
        print scrim.state

        if scrim.state == SCRIM_ACCEPTED:
            opponent = None
            if scrim.team1_id == team_id:
                opponent = Team.query.filter_by(id=scrim.team2_id).one()
            else:
                opponent = Team.query.filter_by(id=scrim.team1_id).one()
            scrims_list.append({
                'state': SCRIM_ACCEPTED,
                'opponent': opponent,
                'scrim': scrim
            })
        elif scrim.state == SCRIM_REJECTED:
            opponent = None
            if scrim.team1_id == team_id:
                opponent = Team.query.filter_by(id=scrim.team2_id).one()
            else:
                opponent = Team.query.filter_by(id=scrim.team1_id).one()
            scrims_list.append({
                'state': SCRIM_REJECTED,
                'opponent': opponent,
                'scrim': scrim
            })
        elif scrim.state == SCRIM_PROPOSED and scrim.team2_id == team_id:
            proposing_team = Team.query.filter_by(id=scrim.team1_id).one()
            scrims_list.append({
                'state': SCRIM_RECEIVED,
                'opponent': proposing_team,
                'scrim': scrim
            })
        elif scrim.state == SCRIM_PROPOSED and scrim.team1_id == team_id:
            print 'here2'
            responding_team = Team.query.filter_by(id=scrim.team2_id).one()
            scrims_list.append({
                'state': SCRIM_SENT,
                'opponent': responding_team,
                'scrim': scrim
            })

    # What's the team availability in days
    days = team.week_days
    aval = map_days(days)
    
    if form.validate_on_submit():
        com = Comment()
        com.team_id = team_id
        com.user_id = g.user.id
        com.comment = form.text.data
        db.session.add(com)
        db.session.commit()
        return redirect(url_for("team_page", team_id=team_id))
    else:
        comment_list =[]
        try:
            cmnts = Comment.query.join(User).all()
            for x in cmnts:
                comment_list.append((x.user.nickname,x.comment))

        except NoResultFound, e:
            comment_list = False

        if g.user == None:
            dont_show = True
        else:
            dont_show = False

        return render_template('team.html',
                team=team,
                members_roles=members_roles,
                pendings=pendings,
                in_team=in_team,
                aval=aval,
                form=form,
                com_list=comment_list,
                dont_show=dont_show,
                scrims_list=scrims_list)

@scrim_app.route('/team/<team_id>/promote/<user_id>')
@login_required
def promote(team_id, user_id):
    """
    Promote a user to Captain

    TODO: Need to add safety checks
    """
    
    try:
        mem = Membership.query.filter(and_(Membership.team_id==team_id, Membership.user_id==user_id)).one()
        mem.role = "Captain"
        db.session.add(mem)
        db.session.commit()
        flash("User promoted")
        return redirect(url_for('team_page', team_id=team_id))
    except NoResultFound, e:
        flash("Invalid user or team")
        return redirect(url_form('team_page', team_id=team_id))

@scrim_app.route('/team/<team_id>/demote/<user_id>')
@login_required
def demote(team_id, user_id):
    """
    Demote user to a member

    TODO: Need to add safety checks
    """
    
    try:
        mem = Membership.query.filter(and_(Membership.team_id==team_id, Membership.user_id==user_id)).one()
        mem.role = "Member"
        db.session.add(mem)
        db.session.commit()
        flash("User promoted")
        return redirect(url_for('team_page', team_id=team_id))
    except NoResultFound, e:
        flash("Invalid user or team")
        return redirect(url_form('team_page', team_id=team_id))



@scrim_app.route('/team/join/<team_id>')
@login_required
def team_join(team_id):
    """
    Makes a new request to join a certain team
    """

    try:
        user = User.query.filter_by(id=g.user.id).one()
    except NoResultFound, e:
        flash("User not found")
        return redirect(url_for('index'))
    
    user_memberships = Membership.query.filter_by(user_id=user.id).all()
    already_in_team = False
    for mem in user_memberships:
        team = Team.query.filter_by(id=mem.team_id).one()
        if (team.id == team_id):
            already_in_team = True
            break

    if not already_in_team:
        req = Request()
        req.team_id = team_id
        req.user_id = user.id
        db.session.add(req)
        db.session.commit()
        flash("Request made")

    return redirect(url_for('team_page', team_id=team_id))

@scrim_app.route('/team/<team_id>/accept_user/<user_id>')
@login_required
def team_accept_user(team_id, user_id):
    """
    Deletes the request and makes a new memebrship
    """

    try:
        user = Request.query.filter(and_(Request.team_id==team_id, Request.user_id==user_id)).one()
    except NoResultFound, e:
        flash("No user")
        return redirect(url_for('index'))

    db.session.delete(user)
    db.session.commit()

    new_membership = Membership()
    new_membership.user_id = user_id
    new_membership.team_id = team_id
    new_membership.role = "Member"

    db.session.add(new_membership)
    db.session.commit()
    
    flash("Accepted")
    return redirect(url_for('team_page', team_id=team_id))         

@scrim_app.route('/scrim/propose/<int:opponent_team_id>', methods=['GET','POST'])
@login_required
def propose_scrim(opponent_team_id):

    try:
        opponent_team = Team.query.filter_by(id=opponent_team_id).one()
    except NoResultFound as e:
        flash('Cannot find the team')
        return redirect(url_for('index'))

    # Check if the user is a captain
    a_captain = False
    your_teams_id = []
    if g.user is not None:
        user_memberships = Membership.query.filter_by(user_id=g.user.id)
        for mem in user_memberships:
            if mem.role == 'Captain':
                a_captain = True
                your_teams_id.append(mem.team_id)

    if not a_captain:
        flash('You are not a captain. Cannot propose scrims.')
        return redirect(url_for('team_page', team_id=opponent_team_id))

    # Set form choices
    your_team = []
    your_team_timezone = []
    for team_id in your_teams_id:
        team = Team.query.filter_by(id=team_id).one()
        your_team.append((str(team.id), str(team.name)))
        your_team_timezone.append((str(team.time_zone), str(team.time_zone)))
    opponent_day = [('1','Mon'),('2','Tue'),('3','Wed'), \
                    ('4','Thurs'),('5','Fri'),('6','Sat'),('7','Sun')]
    opponent_start_time = [('8','8:00'),('9','9:00'),('10','10:00')]

    from wtforms import SelectField
    ProposeScrimForm.team = SelectField('team', choices=your_team)
    ProposeScrimForm.time_zone = SelectField('team', choices=your_team_timezone)
    ProposeScrimForm.day = SelectField('day', choices=opponent_day)
    ProposeScrimForm.start_time = SelectField('start_time', choices=opponent_start_time)
    
    form = ProposeScrimForm()

    if form.validate_on_submit():
        your_team_id = form.team.data
        your_team = Team.query.filter_by(id=your_team_id).one()
        opponent_team = Team.query.filter_by(id=opponent_team_id).one()

        from datetime import datetime as dt
        from consts import SCRIM_PROPOSED

        new_scrim               = Scrim()
        new_scrim.date          = dt.utcfromtimestamp(int(form.utc_time.data))
        new_scrim.map1          = form.map.data
        new_scrim.connection    = 'To be implemented'
        new_scrim.team1_id      = your_team_id
        new_scrim.team1         = your_team
        new_scrim.team2_id      = opponent_team_id
        new_scrim.team2         = opponent_team
        new_scrim.type          = form.type.data
        new_scrim.state         = SCRIM_PROPOSED
        db.session.add(new_scrim)
        db.session.commit()

        flash('Scrim proposed')
        return redirect(url_for('team_page', team_id=opponent_team_id))
    elif request.method == 'POST':
        flash('Scrim proposal not validated')
    
    return render_template('propose_scrim.html', form=form)

@scrim_app.route('/scrim/accept/<int:scrim_id>', methods=['GET', 'POST'])
@login_required
def accept_scrim(scrim_id):
    # team1 = who proposes scrim
    # team2 = who accepts/rejects scrim

    if g.user is None:
        abort(404)

    form = AcceptScrimForm()

    if form.validate_on_submit():
        try:
            scrim = Scrim.query.filter_by(id=scrim_id).one()
        except NoResultFound as e:
            flash('Cannot find scrim with id: ' + str(scrim_id))
            return render_template('accept_scrim.html', form=form)

        accepting_team_id = scrim.team2_id

        # is user the captain of team2
        # try:
        #     team_membership = Membership.query.filter(and_(Membership.team_id==accepting_team_id, Membership.user_id==g.user.id)).one()
        # except NoResultFound as e:
        #     flash('You are not part of the team')
        #     return render_template('accept_scrim.html', form=form)

        # the_captain = team_membership.role == 'Captain'
        # if not the_captain:
        #     flash('You are not the captain of the responding team')
        #     return render_template('accept_scrim.html', form=form)

        from consts import SCRIM_ACCEPTED
        scrim.map2  = form.map.data
        scrim.state = SCRIM_ACCEPTED
        db.session.commit()
        return redirect(url_for('team_page', team_id=accepting_team_id))
    else:
        return render_template('accept_scrim.html', form=form)

@scrim_app.route('/scrim/reject/<int:scrim_id>', methods=['GET'])
@login_required
def reject_scrim(scrim_id):
    if g.user is None:
        abort(404)

    try:
        scrim = Scrim.query.filter_by(id=scrim_id).one()
    except NoResultFound as e:
        flash('Cannot find scrim with id: ' + str(scrim_id))
        return redirect(url_for('index.html'))

    accepting_team_id = scrim.team2_id

    # is user the captain of team2
    # try:
    #     team_membership = Membership.query.filter(and_(Membership.team_id==accepting_team_id, Membership.user_id==g.user.id)).one()
    # except NoResultFound as e:
    #     flash('You are not part of the team')
    #     return render_template('accept_scrim.html', form=form)

    # the_captain = team_membership.role == 'Captain'
    # if not the_captain:
    #     flash('You are not the captain of the responding team')
    #     return render_template('accept_scrim.html', form=form)

    from consts import SCRIM_REJECTED
    scrim.state = SCRIM_REJECTED
    db.session.commit()
    return redirect(url_for('team_page', team_id=accepting_team_id))

@scrim_app.route('/scrim/history/<int:team_id>/page/<int:page>', methods=['GET'])
@login_required
def scrim_history(team_id, page=1):
    from datetime import datetime as dt
    from consts import SCRIM_FINISHED
    from config import SCRIMS_PER_PAGE

    if page < 1:
        abort(404)

    scrims = Scrim.query.filter(or_(Scrim.team1_id == team_id, Scrim.team2_id == team_id))
   
    # check if scrims expired 
    current_time = dt.utcnow()
    scrims_finished = scrims.filter_by(state=SCRIM_FINISHED)

    try:
        scrims_list = scrims_finished.paginate(page, per_page=SCRIMS_PER_PAGE)
    except OperationalError:
        scrims_list = None
    
    return render_template('scrim_history.html', team_id=team_id, scrims_list=scrims_list)

@scrim_app.route('/bots/boom')
def bots_boom():
    """
    Make sure stuff works. Let's say no error = It works!

    See bots.py
    """

    from scrim import bots

    bots.create_bot_users()
    bots.create_bot_teams()
    bots.make_bot_join_team()

    return 'Trust me. It worked.', 200

@scrim_app.route('/bots/scrims')
def bots_scrims():
    """
    """

    from scrim import bots

    bots.create_scrims()

    return 'Does it work?', 200