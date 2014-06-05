from scrim import db
from flask.ext.admin.contrib.sqla import ModelView

class User(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    steam_id            = db.Column(db.String(40), unique=True)
    nickname            = db.Column(db.String(80))
    profile_url         = db.Column(db.String(80))
    avatar_url          = db.Column(db.String(80))
    team_id             = db.Column(db.Integer, db.ForeignKey('team.id'))
    join_date           = db.Column(db.String(80))
    last_online         = db.Column(db.String(80))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def get_or_create(steam_id):
        rv = User.query.filter_by(steam_id=steam_id).first()
        if rv is None:
            rv = User()
            rv.steam_id = steam_id
        return rv

    @staticmethod
    def get_all_users():
        return User.query.all()

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    skill_level = db.Column(db.String(80))
    time_zone = db.Column(db.String(80))
    reputation = db.Column(db.Integer)
    user =  db.relationship('User', backref='team', lazy='dynamic')
