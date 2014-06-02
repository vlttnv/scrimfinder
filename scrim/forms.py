from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required, Length

class EditForm(Form):
    team_skill_level    = TextField('team_skill_level', validators = [Required()])
    team_time_zone      = TextField('team_time_zone', validators = [Required()])
