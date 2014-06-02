from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField
from wtforms.validators import Required, Length
import consts

class EditForm(Form):
    team_skill_level    = TextField('team_skill_level', validators = [Required()])
    team_skill_level    = SelectField(u'Skill Level', choices=[('UGC_PLATINUM', 'UGC Platinum'), ('UGC_GOLD', 'UGC Gold'), ('UGC_SILVER', 'UGC Silver')])
    team_time_zone      = TextField('team_time_zone', validators = [Required()])

