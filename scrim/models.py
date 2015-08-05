from datetime import datetime
from scrim import db

class User(db.Model):
    """
    The user model store information about single user
    logged in through steam. Most of the information is set on first
    log in.
    """

    id                  = db.Column(db.Integer, primary_key=True)
    steam_id            = db.Column(db.String(40), unique=True)
    nickname            = db.Column(db.String(80))
    profile_url         = db.Column(db.String(80))
    avatar_url          = db.Column(db.String(80))
    avatar_url_full     = db.Column(db.String(80))
    join_date           = db.Column(db.DateTime)
    last_online         = db.Column(db.DateTime)
    team_leader         = db.Column(db.Boolean)
    is_merc             = db.Column(db.Integer)
    main_class          = db.Column(db.String(80))
    skill_level         = db.Column(db.String(80))
    last_updated        = db.Column(db.String(80))
    # Stores a list of team ids to which the player
    # has given rep to prevent abuse
    # same with played_with
    has_given_rep_to    = db.Column(db.Text)
    has_played_with     = db.Column(db.Text)
    notifications       = db.Column(db.Integer)
    badges              = db.Column(db.String(80))
    frm_rel             = db.relationship('Message',
            backref='user',
            lazy='dynamic')
    request             = db.relationship('Request',
            backref='user',
            lazy='dynamic')
    membership          = db.relationship('Membership',
            backref='user',
            lazy='dynamic')
    comment             = db.relationship('Comment',
            backref='user',
            lazy='dynamic')
    single_scrim        = db.relationship('SingleScrim',
            backref='user',
            lazy='dynamic')
    reputation          = db.relationship('Reputation',
            backref='user',
            lazy='dynamic')
    #user_reputation          = db.relationship('UserReputation',
    #        backref='user',
    #        lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    @staticmethod
    def get_or_create(steam_id):
        rv = User.query.filter_by(steam_id=steam_id).first()
        if rv is None:
            rv = User()
            rv.steam_id = steam_id
        return rv

    def get_id(self):
        return unicode(self.id)

class Request(db.Model):
    """
    A request is made when a certain member wants to join a team.
    There might be multiple requests per user for different teams.
    (need to make checks for that).

    There should be some kind of a limit to the number of requests
    that a user can make.
    """

    id              = db.Column(db.Integer, primary_key=True)
    team_id         = db.Column(db.Integer, db.ForeignKey('team.id'))
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))

class Team(db.Model):
    """
    The team model store single team information. Reputation is an
    incrementing value (write a method for it).
    """

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(80))
    skill_level     = db.Column(db.String(80))
    time_zone       = db.Column(db.String(80))
    time_from       = db.Column(db.String(80))
    reputation      = db.relationship('Reputation',
            backref='team',
            lazy='dynamic')
    week_days       = db.Column(db.String(7), default="0000000")
    avatar_url      = db.Column(db.String(80))
    num_wins        = db.Column(db.Integer)
    num_losses      = db.Column(db.Integer)
    type            = db.Column(db.String(80))
    membership      = db.relationship('Membership',
            backref='team',
            lazy='dynamic')
    comment         = db.relationship('Comment',
            backref='team',
            lazy='dynamic')

class Membership(db.Model):
    """
    A membership is made after a request is approved and deleted
    """

    id              = db.Column(db.Integer, primary_key=True)
    team_id         = db.Column(db.Integer, db.ForeignKey('team.id'))
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    role            = db.Column(db.String(80))

class Scrim(db.Model):
    """
    Scrim stores information about a proposed scrim, challenge
    or finished scrim

    to be added:
    state of scrim - finished, pending, invalid, proposed, challenge...
    """

    id              = db.Column(db.Integer, primary_key=True)
    date            = db.Column(db.DateTime)
    map1            = db.Column(db.String(80))
    map2            = db.Column(db.String(80))
    connection      = db.Column(db.String(80))
    team1_id        = db.Column(db.Integer, db.ForeignKey('team.id'))
    team1           = db.relationship('Team', foreign_keys=team1_id)
    team2_id        = db.Column(db.Integer, db.ForeignKey('team.id'))
    team2           = db.relationship('Team', foreign_keys=team2_id)
    type            = db.Column(db.String(80))
    # possible values in consts.py
    state           = db.Column(db.String(20))
    team1_log_tf    = db.Column(db.String(40))
    team2_log_tf    = db.Column(db.String(40))
    team1_color     = db.Column(db.String(10))
    team2_color     = db.Column(db.String(10))
    result          = db.Column(db.String(10))

class Comment(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    team_id         = db.Column(db.Integer, db.ForeignKey('team.id'))
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment         = db.Column(db.Text)

class SingleScrim(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    leader_id       = db.Column(db.Integer, db.ForeignKey('user.id'))
    skill_level     = db.Column(db.String(80))
    is_accepted     = db.Column(db.Integer)
    type            = db.Column(db.String(45))
    time_zone       = db.Column(db.String(80))
    date            = db.Column(db.DateTime)
    epoch           = db.Column(db.Integer)
    comment         = db.Column(db.Text)
    maps            = db.Column(db.String(400))
    is_flash        = db.Column(db.Integer)
    bumped          = db.Column(db.Integer)

class Reputation(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id         = db.Column(db.Integer, db.ForeignKey('team.id'))
    type            = db.Column(db.String(1))

class UserReputation(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    user1_id        = db.Column(db.Integer, db.ForeignKey('user.id'))
    user1           = db.relationship('User', foreign_keys=user1_id)
    user2_id        = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2           = db.relationship('User', foreign_keys=user2_id)
    type            = db.Column(db.String(1))

class Message(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    to              = db.Column(db.Integer)
    frm             = db.Column(db.Integer, db.ForeignKey('user.id'))
    message         = db.Column(db.Text)
    timestamp       = db.Column(db.String(20))
    subject	    = db.Column(db.String(45))
    is_read         = db.Column(db.Integer, default=0)

class Notification(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    """
    0 = team join req
    1 = scrim proposal
    2 = accept
    3 = reject
    """
    type            = db.Column(db.Integer)
    to              = db.Column(db.Integer)
    text            = db.Column(db.Text)
    timestamp       = db.Column(db.String(20))
    is_read         = db.Column(db.Integer, default=0)
