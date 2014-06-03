from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField
from wtforms.validators import Required, Length
from consts import *

class EditForm(Form):
    #team_name           = TextField('team_skill_level', validators = [Required()])
    team_skill_level    = SelectField(u'team_skill_level', choices=[(UGC_IRON, UGC_IRON),(UGC_STEEL, UGC_STEEL),(UGC_SILVER, UGC_SILVER),(UGC_GOLD, UGC_GOLD), (UGC_PLATINUM, UGC_PLATINUM)])
    team_time_zone      = SelectField('team_time_zone', choices=[("CET","CET"),("EST","EST")])

