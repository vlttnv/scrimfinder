from scrim import db

class Team(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(80))
    timezone    = db.Column(db.String(40))