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
    # Stores a list of team ids to which the player
    # has given rep to prevent abuse
    # same with played_with
    has_given_rep_to    = db.Column(db.Text)
    has_played_with     = db.Column(db.Text)
    request             = db.relationship('Request',
            backref='user',
            lazy='dynamic')
    membership          = db.relationship('Membership',
            backref='user',
            lazy='dynamic')
    comment             = db.relationship('Comment',
            backref='user',
            lazy='dynamic')

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
    reputation      = db.Column(db.Integer)
    week_days       = db.Column(db.String(7), default="0000000")
    avatar_url      = db.Column(db.String(80))
    num_wins        = db.Column(db.Integer)
    num_losses      = db.Column(db.Integer)
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
    team1_result    = db.Column(db.String(40))
    team2_result    = db.Column(db.String(40))
    team1_color     = db.Column(db.String(10))
    team2_color     = db.Column(db.String(10))

class Comment(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    team_id         = db.Column(db.Integer, db.ForeignKey('team.id'))
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment         = db.Column(db.Text)
