from datetime import datetime
from scrim import db

class User(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    role                = db.Column(db.Integer)
    steam_id            = db.Column(db.String(40), unique=True)
    nickname            = db.Column(db.String(80))
    profile_url         = db.Column(db.String(80))
    avatar_url          = db.Column(db.String(80))
    team_id             = db.Column(db.Integer, db.ForeignKey('team.id'))
    join_date           = db.Column(db.DateTime)
    last_online         = db.Column(db.DateTime)
    team_leader         = db.Column(db.Integer)
    rq                  = db.relationship('Request', backref='user', lazy='dynamic')
    membership          = db.relationship('Membership', backref='user', lazy='dynamic')

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
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    skill_level = db.Column(db.String(80))
    time_zone = db.Column(db.String(80))
    reputation = db.Column(db.Integer)
    user = db.relationship('User', backref='team', lazy='dynamic')
    membership = db.relationship('Membership', backref='team', lazy='dynamic')
    scrim_team1 = db.relationship('Scrim', foreign_keys='Scrim.team_id1', backref='team', lazy='dynamic')
    scrim_team1 = db.relationship('Scrim', foreign_keys='Scrim.team_id2', backref='team', lazy='dynamic')

class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    role = db.Column(db.String(80))

class Scrim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(80))
    time_zone = db.Column(db.String(80))
    map1 = db.Column(db.String(80))
    map2 = db.Column(db.String(80))
    connection_info = db.Column(db.String(80))
    team_id1 = db.Column(db.Integer, db.ForeignKey('team.id'))
    team_id2 = db.Column(db.Integer, db.ForeignKey('team.id'))
    scrim_type = db.Column(db.String(80))
