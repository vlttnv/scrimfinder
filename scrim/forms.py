from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField
from wtforms.validators import Required, Length
from consts import *

class EditForm(Form):
    team_skill_level    = TextField('team_skill_level', validators = [Required()])
    team_skill_level    = SelectField(u'Skill Level', choices=[(UGC_IRON, UGC_IRON),(UGC_STEEL, UGC_STEEL),(UGC_SILVER, UGC_SILVER),(UGC_GOLD, UGC_GOLD), (UGC_PLATINUM, UGC_PLATINUM)])
    team_time_zone      = TextField('team_time_zone', validators = [Required()])

