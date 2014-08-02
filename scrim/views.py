from scrim import scrim_app, oid, db, models, lm
from models import User, Team, Request, Membership, Comment, Scrim, SingleScrim
from utils import steam_api, logs_tf_api
from consts import *
from flask import request, redirect, session, g, json, render_template, flash, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
import requests
import re
from sqlalchemy import func, and_, or_, desc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import OperationalError

#========================
# Helper function
#========================
def convert_bits_to_days(bit_string):
    days_of_week = [
        "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"
    ]
    aval = [day for day, bit in zip(days_of_week, bit_string) if bit == '1']
    return aval

@scrim_app.before_request
def before_request():
    """
    A handler before every request. TODO: More.
    """

    if 'user_id' in session:
        g.user = User.query.filter_by(id=session['user_id']).first()
    else:
        g.user = None

@scrim_app.route('/')
def index():
    """
    Home page. TODO: More.
    """
    five_teams = Team.query.order_by(Team.id.desc()).limit(5).all()
    five_users = User.query.order_by(User.id.desc()).limit(5).all()
    five_scrims = SingleScrim.query.join(User).filter(User.id==SingleScrim.leader_id).order_by(SingleScrim.id.desc()).limit(5).all()

    count_teams = Team.query.count()
    count_users = User.query.count()

    return render_template('index.html', teams=five_teams, users=five_users,count_teams=count_teams,count_users=count_users,five_scrims=five_scrims)
    #return render_template('index2.html')

@scrim_app.route('/login')
@oid.loginhandler
def login():
    """
    Log in via Steam OpenID.
    """

    if g.user is not None:
        return redirect(oid.get_next_url())
    else:
        return oid.try_login('http://steamcommunity.com/openid')

@oid.after_login
def after_login(resp):
    """
    After the user logged in, create a new user or update the existing one
    """

    from datetime import datetime as dt
    from utils import steam_api

    steam_id_regex = re.compile('steamcommunity.com/openid/id/(.*?)$')
    steam_id = steam_id_regex.search(resp.identity_url).group(1)

    try:
        g.user = User.query.filter_by(steam_id=steam_id).one()
        last_online = g.user.last_online
        # choose to update steam user info (LIMITED API calls)
        g.user.last_online = dt.utcnow()
    except NoResultFound:
        g.user = User()
        steam_data             = steam_api.get_user_info(steam_id)
        g.user.steam_id        = steam_id
        g.user.nickname        = steam_data['personaname']
        g.user.profile_url     = steam_data['profileurl']
        g.user.avatar_url      = steam_data['avatar']
        g.user.avatar_url_full = steam_data['avatarfull']
        g.user.join_date       = dt.utcnow()
        g.user.last_online     = dt.utcnow()
        db.session.add(g.user)
    db.session.commit()
    
    login_user(g.user)

    return redirect(oid.get_next_url())

@scrim_app.route('/logout')
def logout():
    """
    Logout.
    """

    logout_user()
    flash("Logged out", "success")
    return redirect(url_for('index'))

@scrim_app.route('/user/<steam_id>')
def user_page(steam_id):
    """
    Return the user page, containing a list of tuples of Team and Membership, 
    for instance, [(TeamA,"Captain"),(TeamB,"Coach")].
    """
    from forms import CreateTeamForm
    from consts import TIME_ZONES_DICT
    create_team_form = CreateTeamForm()
    try:
        user = User.query.filter_by(steam_id=steam_id).one()
    except NoResultFound:
        flash("User not found", "danger")
        return redirect(url_for('index'))

    team_roles = []
    user_memberships = Membership.query.filter_by(user_id=user.id).all()
    for mem in user_memberships:
        team = Team.query.filter_by(id=mem.team_id).one()
        team_roles.append((team, mem.role))

    single_scrims = SingleScrim.query.filter_by(leader_id=user.id).all()

    return render_template('user.html', user=user, team_roles=team_roles,create_team_form=create_team_form,tz=TIME_ZONES_DICT,single_scrims=single_scrims)

@scrim_app.route('/users', methods=['GET','POST'])
@scrim_app.route('/users/page/<int:page>', methods=['GET','POST'])
def all_users(page=1):
    """
    Show all users, 50 results per page.
    """

    from forms import FilterUserForm

    form = FilterUserForm()
    query = User.query

    if form.clear.data == True:
        form.reset_user_filter()

    if form.validate_on_submit():
        if form.nickname.data != "":
            query = query.filter(User.nickname.like('%'+form.nickname.data+'%')).order_by(User.id.desc())
        if form.steam_id.data != "":
            query = query.filter(User.steam_id.like('%'+form.steam_id.data+'%')).order_by(User.id.desc())
        # ????
        if form.nickname.data == "" and form.steam_id.data =="":
            query = query.filter(User.is_merc==int(form.is_merc.data))


    from config import USERS_PER_PAGE

    try:
        users_list = query.order_by(User.id.desc()).paginate(page, per_page=USERS_PER_PAGE)
    except OperationalError:
        flash("No users in the database.", "danger")
        users_list = None
    
    return render_template('all_users.html', users_list=users_list, form=form)

@scrim_app.route('/teams', methods=['GET','POST'])
@scrim_app.route('/teams/page/<int:page>', methods=['GET','POST'])
def all_teams(page=1):
    """
    Show all teams, 50 results per page.
    """
    
    from forms import FilterTeamForm

    form = FilterTeamForm()
    query = Team.query
    
    if form.clear.data == True:
        form.reset_team_filter()

    from utils import scrim_filter

    if form.validate_on_submit():
        if form.team_name.data != "":
            query = query.filter(Team.name.like('%'+form.team_name.data+'%'))
        if form.team_skill_level.data != "ALL":
            query = query.filter_by(skill_level=form.team_skill_level.data)
        if form.team_time_zone.data != "ALL":
            query = query.filter_by(time_zone=form.team_time_zone.data)
        if form.team_type.data != "ALL":
            query = query.filter(or_(Team.type == form.team_type.data, Team.type == None))

        scrim_days = form.read_scrim_days()
        matched_scrim_days = scrim_filter.scrim_days_combinations(scrim_days)
        query = query.filter(Team.week_days.in_(matched_scrim_days))

    from config import TEAMS_PER_PAGE

    try:
        teams_list = query.order_by(Team.id.desc()).paginate(page, per_page=TEAMS_PER_PAGE)
    except OperationalError:
        flash("No teams in the database.", "danger")
        teams_list = None
    
    return render_template('all_teams.html', teams_list=teams_list, form=form)

@scrim_app.route('/scrims/', methods=['GET','POST'])
@scrim_app.route('/scrims/page/<int:page>', methods=['GET','POST'])
@login_required
def all_scrims(page=1):
    """
    Scrim search page. Only visible for users who are part of a team.

    Search results do not include your own teams. HACK: default search
    parameters are from the user's first team.
    """
    from wtforms import SelectField
    from forms import FilterScrimForm
    form = FilterScrimForm()
    user_memberships = Membership.query.filter_by(user_id=g.user.id).all()
    if len(user_memberships) == 0:
        flash('You are not in a team. Cannot search for scrims.', "warning")
        return render_template('all_scrims.html', teams_list=None, form=form)

    # Set form choices
    your_team_preferences = [("None", "None")]
    your_team_list = []

    for mem in user_memberships:
        your_team_preferences.append((str(mem.team.id), str(mem.team.name)))
        your_team_list.append(mem.team)

    
    FilterScrimForm.team_preference = SelectField('team', choices=your_team_preferences)
    form = FilterScrimForm()

    query = Team.query
    for mem in user_memberships:
        query = query.filter(Team.id != mem.team_id)
   
    if form.clear.data == True:
        form.reset_scrim_filter()

    from utils import scrim_filter

    if form.validate_on_submit():
        if form.team_skill_level.data != "ALL":
            query = query.filter_by(skill_level=form.team_skill_level.data)
        if form.team_time_zone.data != "ALL":
            query = query.filter_by(time_zone=form.team_time_zone.data)
        if form.team_type.data != "ALL":
            query = query.filter(or_(Team.type == form.team_type.data, Team.type == None))

        scrim_days = form.read_scrim_days()
        matched_scrim_days = scrim_filter.scrim_days_combinations(scrim_days)
        query = query.filter(Team.week_days.in_(matched_scrim_days))
    """
    else:
        # HACK
        try:
            player_1st_team_id = user_memberships[0].team_id
            player_1st_team = Team.query.filter_by(id=player_1st_team_id).one()
            scrim_days = player_1st_team.week_days

            form.team_skill_level.data = player_1st_team.skill_level
            form.team_time_zone.data = player_1st_team.time_zone
            form.fill_scrim_days(scrim_days)

            query = query.filter_by(skill_level=player_1st_team.skill_level)            
            query = query.filter_by(time_zone=player_1st_team.time_zone)

            matched_scrim_days = scrim_filter.scrim_days_combinations(scrim_days)
            query = query.filter(Team.week_days.in_(matched_scrim_days))
        except NoResultFound as e:
            print e
    """
    from config import TEAMS_PER_PAGE
    try:
        teams_list = query.paginate(page, per_page=TEAMS_PER_PAGE)
    except OperationalError:
        teams_list = None

    return render_template('all_scrims.html', teams_list=teams_list, form=form, your_team_list=your_team_list)

@scrim_app.route('/singles/', methods=['GET','POST'])
@scrim_app.route('/singles/page/<int:page>', methods=['GET','POST'])
def all_singles(page=1):
    from forms import FilterSinglesForm
    form = FilterSinglesForm()

    if form.clear.data == True:
        form.reset_singles_filter()

    single_scrims = SingleScrim.query
    from utils import scrim_filter

    if form.validate_on_submit():
        if form.team_leader.data != "":
            single_scrims = single_scrims.join(User).filter(User.nickname.like('%'+form.team_leader.data+'%'))
        if form.team_skill_level.data != "ALL":
            single_scrims = single_scrims.filter_by(skill_level=form.team_skill_level.data)
        if form.team_time_zone.data != "ALL":
            single_scrims = single_scrims.filter_by(time_zone=form.team_time_zone.data)
        if form.team_type.data != "ALL":
            single_scrims = single_scrims.filter(or_(SingleScrim.type == form.team_type.data, SingleScrim.type == None))

        # scrim_days = form.read_scrim_days()
        # matched_scrim_days = scrim_filter.scrim_days_combinations(scrim_days)
        # single_scrims = single_scrims.filter(Team.week_days.in_(matched_scrim_days))

    from config import SCRIMS_PER_PAGE
    try:
        single_scrims_list = single_scrims.order_by(SingleScrim.id.desc()).paginate(page, per_page=SCRIMS_PER_PAGE)
    except OperationalError:
        single_scrims_list = None

    return render_template('all_singles.html', single_scrims_list=single_scrims_list, form=form)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
@lm.unauthorized_handler
def unauthorized():
    flash("You need to log in through Steam to access this page. Please do so using the button in the top right corner.", "danger")
    return redirect(url_for('index'))

@scrim_app.route('/profile/edit', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    """
    This can be done once the user model is finalized
    so that constat modifications are avoided
    """

    from forms import EditUserForm
    form = EditUserForm()
    try:
        user_edit = User.query.filter_by(steam_id=g.user.steam_id).one()
    except NoResultFound, e:
        flash("Error getting user.", "danger")
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user_edit.main_class = form.main_class.data
        user_edit.is_merc = int(form.is_merc.data)
        user_edit.skill_level = form.skill_level.data
        db.session.add(user_edit)
        db.session.commit()
        flash("Profile successfully updated.", "success")
        return redirect(url_for('user_page', steam_id=g.user.steam_id))
    else:
        form.main_class.data = user_edit.main_class
        form.is_merc.data = user_edit.is_merc
        form.skill_level.data = user_edit.skill_level
        return render_template('edit_profile.html', form = form)
    #return render_template('edit_profile.html', form=form)

@scrim_app.route('/team/edit/<int:team_id>', methods = ['GET', 'POST'])
@login_required
def edit_team(team_id):
    """
    Edit a team's information.

    The operation is only permitted by the captain.
    """

    have_edit_rights = False
    teams = Membership.query.filter_by(user_id=g.user.id).all()
    for team in teams:
        if team.team_id == team_id and team.role == "Captain":
            have_edit_rights = True
    
    if not have_edit_rights:
        flash("You do not have the rights to edit this team.", "danger")
        return redirect(url_for('team_page', team_id=team_id))

    try:
        team_edit = Team.query.filter_by(id=team_id).one()
    except NoResultFound, e:
        flash("The team you are about to edit does not exist.", "warning")
        return redirect(url_for('index'))

    from forms import EditTeamForm
    form = EditTeamForm()
    
    if form.validate_on_submit():
        team_edit.name = form.team_name.data
        team_edit.skill_level = form.team_skill_level.data
        team_edit.time_zone = form.team_time_zone.data
        team_edit.week_days = form.read_scrim_days()
        #team_edit.time_from = form.time_from.data
        team_edit.type = form.team_type.data
        db.session.add(team_edit)
        db.session.commit()

        return redirect(url_for('team_page', team_id=team_id))
    else:
        form.team_name.data = team_edit.name
        form.team_skill_level.data = team_edit.skill_level
        form.team_time_zone.data = team_edit.time_zone
        form.fill_scrim_days(team_edit.week_days)
        #form.time_from.data = team_edit.time_from
        form.team_type.data = team_edit.type

        return render_template('edit_team.html', form=form, team_id=team_id)

@scrim_app.route('/team/create', methods = ['GET', 'POST'])
@login_required
def create_team():
    """
    A user creates a new team and sets some team parameters
    The suer by default becomes the team leader
    """

    from forms import CreateTeamForm
    form = CreateTeamForm()

    player_memberships = Membership.query.filter_by(user_id=g.user.id).all()
    if len(player_memberships) == 3:
        flash('You are in three teams already. Chill.', "warning")
        return redirect(url_for('user_page', steam_id=g.user.steam_id))

    from consts import TIME_ZONES_DICT

    if form.validate_on_submit():
        team = Team()
        team.name = form.team_name.data
        team.skill_level = form.team_skill_level.data
        team.time_zone = form.team_time_zone.data
        team.week_days = form.read_scrim_days()
        team.type = form.team_type.data
        db.session.add(team)
        db.session.commit()

        membership = Membership()
        membership.team_id = team.id
        membership.user_id = g.user.id
        membership.role = "Captain" 
        db.session.add(membership)
        db.session.commit()

        return redirect(url_for('user_page', steam_id=g.user.steam_id))
    else:
        return render_template('create_team.html', create_team_form=form)

@scrim_app.route('/new_single', methods = ['GET', 'POST'])
@login_required
def new_single():
    from forms import AddSingleScrim
    form = AddSingleScrim()

    if form.validate_on_submit():
        single =  SingleScrim()
        single.comment = form.comment.data
        single.type = form.type.data
        single.time_zone = form.time_zone.data
        single.maps = form.maps.data
        single.leader_id = g.user.id
        single.skill_level = form.skill_level.data
        print form.comment.data
        db.session.add(single)
        db.session.commit()

        return redirect(url_for('all_singles'))
    else:
        return render_template('create_single.html', form=form)
@scrim_app.route('/team/quit/<int:team_id>', methods=['POST'])
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
        flash("Dude you are not in this team", "warning")
        return redirect(url_for('user_page'), steam_id=g.user.steam_id)
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
                    there's no one left in the team, the team is deleted", "info")
        else:
            flash("You quit from team " + user_team_name, "success")
        return redirect(url_for('index'))

@scrim_app.route('/team/times/<team_id>')
def team_times_json(team_id):
    all_scrims = Scrim.query.filter(or_(Scrim.team1_id == team_id, Scrim.team2_id == team_id))
    
    import time
    import datetime
    json_s = '{'
    for scrim in all_scrims.all():
        a = time.strptime(str(scrim.date), "%Y-%m-%d %H:%M:%S")
        fdate = datetime.datetime(a.tm_year,a.tm_mon,a.tm_mday,a.tm_hour,a.tm_min).strftime('%s')
        json_s = json_s + '"' + fdate + '"' + ': 1,'

    json_s = json_s + '"0": 1}'

    return json_s

@scrim_app.route('/team/<int:team_id>', methods=['GET','POST'])
@scrim_app.route('/team/<int:team_id>/scrim_page/<int:scrim_page>', methods=['GET','POST'])
def team_page(team_id, scrim_page=1):
    """
    Currently shows a specific team, with team parameters, current members
    and pending members

    The pending members view will be restricted to the team leader
    """

    from forms import CommentTeamForm
    from config import API_ADDRESS
    from consts import TIME_ZONES_DICT

    form = CommentTeamForm()

    try:
        team = Team.query.filter_by(id=team_id).one()
    except NoResultFound as e:
        flash("Team not found", "danger")
        return redirect(url_for('index'))

    all_members = Membership.query.join(Team).filter_by(id=team_id).all()
    # an arry of tuples of User and role e.g. [(user,"Captain"),(user,"BenchPlayer")]
    members_roles = []
    for mem in all_members:
        user = User.query.filter_by(id=mem.user_id).one()
        members_roles.append((user, mem.role))

    pendings = Request.query.filter_by(team_id=team_id).join(User).filter(User.id==Request.user_id).all()

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

    scrims = Scrim.query.filter(or_(Scrim.team1_id == team_id, Scrim.team2_id == team_id))
    scrims = scrims.order_by(desc(Scrim.date))

    from datetime import datetime as dt
    # ACCEPTED -> FINISHED when time passes
    scrims_finished = scrims.filter(and_(Scrim.state == SCRIM_ACCEPTED, Scrim.date < dt.utcnow()))
    for scrim in scrims_finished:
        scrim.state = SCRIM_FINISHED
    if scrims_finished.count() > 0:
        db.session.commit()

    from config import SCRIMS_PER_PAGE_TEAM
    try:
        scrims_list = scrims.paginate(scrim_page, per_page=SCRIMS_PER_PAGE_TEAM)
    except OperationalError:
        scrims_list = None

    aval = convert_bits_to_days(team.week_days)

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
            cmnts = Comment.query.join(User).filter(Comment.team_id==team_id).all()
            for x in cmnts:
                comment_list.append((x.user.nickname,x.comment,x.user.avatar_url,x.user.steam_id))

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
                propose_scrim=propose_scrim,
                scrims_list=scrims_list,
                addr=API_ADDRESS,
                tz=TIME_ZONES_DICT)

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
        flash("User promoted", "success")
        return redirect(url_for('team_page', team_id=team_id))
    except NoResultFound, e:
        flash("Invalid user or team", "danger")
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
        flash("User promoted", "success")
        return redirect(url_for('team_page', team_id=team_id))
    except NoResultFound, e:
        flash("Invalid user or team", "danger")
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
        flash("User not found", "danger")
        return redirect(url_for('index'))
    
    user_memberships = Membership.query.filter_by(user_id=user.id).all()
    already_in_team = False
    for mem in user_memberships:
        team = Team.query.filter_by(id=mem.team_id).one()
        if (team.id == team_id):
            already_in_team = True
            break

    try:
        req = Request.query.filter(and_(Request.team_id==team_id, Request.user_id==g.user.id)).one()
        flash("You already made a request", "warning")
        return redirect(url_for('team_page', team_id=team_id))
    except NoResultFound, e:
        pass

    if not already_in_team:
        req = Request()
        req.team_id = team_id
        req.user_id = user.id
        db.session.add(req)
        db.session.commit()
        flash("Request made", "success")

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
        flash("No user", "danger")
        return redirect(url_for('index'))

    db.session.delete(user)
    db.session.commit()

    new_membership = Membership()
    new_membership.user_id = user_id
    new_membership.team_id = team_id
    new_membership.role = "Member"

    db.session.add(new_membership)
    db.session.commit()
    
    flash("Accepted", "success")
    return redirect(url_for('team_page', team_id=team_id))         

@scrim_app.route('/team/<team_id>/reject_user/<user_id>')
@login_required
def team_reject_user(team_id, user_id):
    """
    Deletes the request
    """

    try:
        user = Request.query.filter(and_(Request.team_id==team_id, Request.user_id==user_id)).one()
    except NoResultFound, e:
        flash("No user", "danger")
        return redirect(url_for('index'))

    db.session.delete(user)
    db.session.commit()

    flash("Rejected", "success")
    return redirect(url_for('team_page', team_id=team_id))

def hack_timezone(utc_offset):
    print 'something'

@scrim_app.route('/scrim/propose/<int:opponent_team_id>', methods=['GET','POST'])
@login_required
def propose_scrim(opponent_team_id):

    from forms import ProposeScrimForm

    try:
        opponent_team = Team.query.filter_by(id=opponent_team_id).one()
    except NoResultFound as e:
        flash('Cannot find the team', "danger")
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
        flash('You are not a captain. Cannot propose scrims.', "warning")
        return redirect(url_for('team_page', team_id=opponent_team_id))

    from consts import TIME_ZONES_DICT

    # Set form choices
    your_team = []
    your_team_timezone = []
    for team_id in your_teams_id:
        team = Team.query.filter_by(id=team_id).one()
        your_team.append((str(team.id), str(team.name)))

        time_zone_label = None
        for item in TIME_ZONES_DICT:
            if item['time_zone'] == team.time_zone:
                time_zone_label = item['label']
                break
        your_team_timezone.append((team.time_zone, time_zone_label))
    opponent_day = [('1','Mon'),('2','Tue'),('3','Wed'), \
                    ('4','Thurs'),('5','Fri'),('6','Sat'),('7','Sun')]
    opponent_start_time = [('0','0:00'),('1','1:00'),('2','2:00'),('3','3:00'),
                            ('4','4:00'),('5','5:00'),('6','6:00'),('7','7:00'),
                            ('8','8:00'),('9','9:00'),('10','10:00'),('11','11:00'),
                            ('12','12:00'),('13','13:00'),('14','14:00'),('15','15:00'),
                            ('16','16:00'),('17','17:00'),('18','18:00'),('19','19:00'),
                            ('20','20:00'),('21','21:00'),('22','22:00'),('23','23:00')]

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

        new_scrim            = Scrim()
        new_scrim.date       = dt.utcfromtimestamp(int(form.utc_time.data))
        new_scrim.map1       = form.map.data
        new_scrim.connection = 'To be implemented'
        new_scrim.team1_id   = your_team_id
        new_scrim.team1      = your_team
        new_scrim.team2_id   = opponent_team_id
        new_scrim.team2      = opponent_team
        new_scrim.type       = form.type.data
        new_scrim.state      = SCRIM_PROPOSED
        db.session.add(new_scrim)
        db.session.commit()

        flash('Scrim proposed', "success")
        return redirect(url_for('team_page', team_id=opponent_team_id))
    elif request.method == 'POST':
        flash('Scrim proposal not validated', "danger")
    
    return render_template('propose_scrim.html', form=form, team_id=opponent_team_id)

@scrim_app.route('/scrim/accept/', methods=['POST'])
@login_required
def accept_scrim():
    """
    # team1 = who proposes scrim
    # team2 = who accepts/rejects scrim
    """

    if g.user is None:
        abort(404)

    scrim_id = request.form['scrim_id']
    scrim_map = request.form['map']

    if (scrim_id == None or scrim_id == ""):
        return "The form is invalid"

    try:
        scrim = Scrim.query.filter_by(id=request.form['scrim_id']).one()
    except NoResultFound as e:
        return "Cannot find scrim with id: " + scrim_id

    accepting_team_id = scrim.team2_id

    if (scrim_map == None or scrim_map == ""):
        return "Map field is empty"

    # is user the captain of team2
    try:
        team_membership = Membership.query.filter(and_(Membership.team_id==accepting_team_id, Membership.user_id==g.user.id)).one()
    except NoResultFound as e:
        return "You are not part of the team"

    the_captain = team_membership.role == "Captain"
    if not the_captain:
        return "You are not the team captain"

    from consts import SCRIM_ACCEPTED

    scrim.map2  = scrim_map
    scrim.state = SCRIM_ACCEPTED
    db.session.commit()

    flash('Scrim accepted', "success")
    return "OK"

@scrim_app.route('/scrim/reject/', methods=['POST'])
@login_required
def reject_scrim():
    if g.user is None:
        return "You are not logged in"

    scrim_id = request.form['scrim_id']
    if scrim_id == None or scrim_id == "":
        return "'scrim_id' is invalid"

    try:
        scrim = Scrim.query.filter_by(id=scrim_id).one()
    except NoResultFound as e:
        return "No such scrim id"

    accepting_team_id = scrim.team2_id

    # is user the captain of team2
    try:
        team_membership = Membership.query.filter(and_(Membership.team_id==accepting_team_id, Membership.user_id==g.user.id)).one()
    except NoResultFound:
        return "You are not part of the team"

    the_captain = team_membership.role == "Captain"
    if not the_captain:
        return "You are not the team captain"

    from consts import SCRIM_REJECTED
    scrim.state = SCRIM_REJECTED
    db.session.commit()

    flash('Scrim rejected.', "danger")
    return "OK"

@scrim_app.route('/scrim/upload_result/', methods=['POST'])
def upload_scrim_result():
    if g.user is None:
        return "You are not logged in"

    scrim_id = request.form['scrim_id']
    logs_tf_link = request.form['logs_tf_link']
    team_color = request.form['team_color']

    if scrim_id == None or scrim_id == "":
        return "'scrim_id' is invalid"
    if logs_tf_link == None or logs_tf_link == "":
        return "'logs_tf_link' is invalid"
    if team_color == None or team_color == "":
        return "'team_color' is invalid"

    try:
        scrim = Scrim.query.filter_by(id=scrim_id).one()
    except NoResultFound as e:
        return "No such scrim id"

    user_memberships = Membership.query.filter_by(user_id=g.user.id).all()
    if len(user_memberships) == 0:
        return "You don't belong in a team."
    is_team_1 = False;
    is_team_2 = False;
    for mem in user_memberships:
        if (mem.team_id == scrim.team1_id):
            is_team_1 = True
            break
        elif (mem.team_id == scrim.team2_id):
            is_team_2 = True
            break

    if is_team_1 == False and is_team_2 == False:
        return "You are not in the team"
    if is_team_1 == True:
        scrim.team1_log_tf = logs_tf_link
        scrim.team1_color = team_color
        team1_color = team_color
    else:
        scrim.team2_log_tf = logs_tf_link
        scrim.team2_color = team_color
        if team_color == "Blue":
            team1_color = "Red"
        else:
            team1_color = "Blue"

    if logs_tf_link.startswith("http://logs.tf/"):
        log_tf_id = logs_tf_link.split("http://logs.tf/")[1]
    elif logs_tf_link.startswith("logs.tf/"):
        log_tf_id = logs_tf_link.split("logs.tf/")[1]
    else:
        return "'logs_tf_link' is invalid"

    if not log_tf_id.isdigit():
        return "'logs_tf_link' is invalid"

    if team1_color == "Blue":
        scrim.result = logs_tf_api.get_match_result(True, log_tf_id)
    else:
        scrim.result = logs_tf_api.get_match_result(False, log_tf_id)
    db.session.commit()
    return "OK"

@scrim_app.route('/scrim/history/<int:team_id>/page/<int:page>', methods=['GET'])
@login_required
def scrim_history(team_id, page=1):
    from datetime import datetime as dt
    from consts import SCRIM_ACCEPTED
    from config import SCRIMS_PER_PAGE

    if page < 1:
        abort(404)

    scrims = Scrim.query.filter(or_(Scrim.team1_id == team_id, Scrim.team2_id == team_id))
    scrims = scrims.order_by(desc(Scrim.date))
    
    # ACCEPTED -> FINISHED when time passes
    scrims_finished = scrims.filter(and_(Scrim.state == SCRIM_ACCEPTED, Scrim.date < dt.utcnow()))
    for scrim in scrims_finished:
        scrim.state = SCRIM_FINISHED
    if scrims_finished.count() > 0:
        db.session.commit()

    try:
        scrims_list = scrims.paginate(page, per_page=SCRIMS_PER_PAGE)
    except OperationalError:
        scrims_list = None

    return render_template('scrim_history.html', team_id=team_id, scrims_list=scrims_list)

# Bots stuff
# @scrim_app.route('/bots/boom')
# def bots_boom():
#     """
#     Make sure stuff works. Let's say no error = It works!

#     See bots.py
#     """

#     from scrim import bots

#     bots.create_bot_users()
#     bots.create_bot_teams()
#     bots.make_bot_join_team()

#     return 'Trust me. It worked.', 200

# @scrim_app.route('/bots/scrims')
# def bots_scrims():
#     """
#     """

#     from scrim import bots

#     bots.create_scrims()

#     return 'Does it work?', 200

# @scrim_app.route('/bots/accepted_scrim')
# def bots_accepted_scrim():
#     """
#     """

#     from scrim import bots

#     team_id = bots.create_accepted_scrim()

#     return redirect(url_for('team_page', team_id=team_id))

@scrim_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
@scrim_app.route('/delete_single/<single_id>')
def delete_single(single_id):
    try:
        single_scrim = SingleScrim.query.filter_by(id=single_id).one()
    except NoResultFound as e:
        flash("Scrim not found", "danger")
        return redirect(url_for('user_page', steam_id=g.user.steam_id))

    if g.user.id == single_scrim.leader_id:
        db.session.delete(single_scrim)
        db.session.commit()
        flash("Scrim deleted", "success")
        return redirect(url_for('user_page', steam_id=g.user.steam_id))
    else:
        flash("You are not allowed to do this", "danger")
        return redirect(url_for('user_page', steam_id=g.user.steam_id))


