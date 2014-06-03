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

class Available(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    day         = db.Column(db.Integer)
    time_from   = db.Column(db.String)
    time_to     = db.Column(db.String)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
