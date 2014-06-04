from datetime import datetime
from scrim import db
from flask.ext.admin.contrib.sqla import ModelView

class User(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    steam_id            = db.Column(db.String(40), unique=True)
    nickname            = db.Column(db.String(80))
    profile_url         = db.Column(db.String(80))
    avatar_url          = db.Column(db.String(80))
    team_name           = db.Column(db.String(80))
    team_skill_level    = db.Column(db.String(80))
    team_time_zone      = db.Column(db.String(80))
    team_availability   = db.relationship('Available', backref='user',
            lazy='dynamic')
    joined_date         = db.Column(db.DateTime)
    last_online         = db.Column(db.DateTime)
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def get_record(steam_id):
        user = User.query.filter_by(steam_id=steam_id).first()
        return user

    @staticmethod
    def get_all_users():
        return User.query.all()

class Available(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    day         = db.Column(db.String(80))
    time_from   = db.Column(db.String(80))
    time_to     = db.Column(db.String(80))
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
