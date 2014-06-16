from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField, TextAreaField
from wtforms.validators import Required, Length
from consts import *

class UserEditForm(Form):
    team_name           = TextField('team_name', validators = [Required()])
    #team_skill_level    = SelectField(u'team_skill_level', choices=[(UGC_IRON, UGC_IRON),(UGC_STEEL, UGC_STEEL),(UGC_SILVER, UGC_SILVER),(UGC_GOLD, UGC_GOLD), (UGC_PLATINUM, UGC_PLATINUM)])
    team_skill_level    = SelectField(u'team_skill_level', choices=[SKILL_LEVEL])
    team_time_zone      = SelectField('team_time_zone', choices=CHOICES_ZONES)

class TeamEditForm(Form):
    team_name           = TextField('team_name')
    team_skill_level = SelectField('team_skill_level', choices=CHOICES_SKILLS)
    team_time_zone      = SelectField('team_time_zone', 
            choices=CHOICES_ZONES)

    mon = BooleanField('Monday')
    tue = BooleanField('Tuesday')
    wed = BooleanField('Wednesday')
    thu = BooleanField('Thursday')
    fri = BooleanField('Friday')
    sat = BooleanField('Saturday')
    sun = BooleanField('Sunday')
    time_from = SelectField('time_from',
            choices=[("8:00","8:00"),
                ("9:00","9:00"),
                ("10:00","10:00")])

class TeamCommentForm(Form):
    text                = TextAreaField('text', validators=[Required()])

class CreateTeamForm(Form):
    team_name           = TextField('team_name', validators = [Required()])
    team_skill_level    = SelectField(u'team_skill_level', 
            choices=CHOICES_SKILLS)
    team_time_zone      = SelectField('team_time_zone', 
            choices=CHOICES_ZONES)

    mon = BooleanField('Monday')
    tue = BooleanField('Tuesday')
    wed = BooleanField('Wednesday')
    thu = BooleanField('Thursday')
    fri = BooleanField('Friday')
    sat = BooleanField('Saturday')
    sun = BooleanField('Sunday')

class FilterTeamForm(Form):
    team_name           = TextField('team_name')
    team_skill_level    = SelectField(u'team_skill_level', 
            choices=[(ALL, ALL),
                (UGC_IRON, UGC_IRON),
                (UGC_STEEL, UGC_STEEL),
                (UGC_SILVER, UGC_SILVER),
                (UGC_GOLD, UGC_GOLD), 
                (UGC_PLATINUM, UGC_PLATINUM)])
    team_time_zone      = SelectField('team_time_zone', 
            choices=[("ALL", "ALL"),
                ("CET","CET"),
                ("EST","EST")])

    mon = BooleanField('Monday')
    tue = BooleanField('Tuesday')
    wed = BooleanField('Wednesday')
    thu = BooleanField('Thursday')
    fri = BooleanField('Friday')
    sat = BooleanField('Saturday')
    sun = BooleanField('Sunday')

class FilterScrimForm(Form):
    team_skill_level    = SelectField(u'team_skill_level', 
            choices=[(ALL, ALL),
                (UGC_IRON, UGC_IRON),
                (UGC_STEEL, UGC_STEEL),
                (UGC_SILVER, UGC_SILVER),
                (UGC_GOLD, UGC_GOLD), 
                (UGC_PLATINUM, UGC_PLATINUM)])
    team_time_zone      = SelectField('team_time_zone', 
            choices=[("ALL", "ALL"),
                ("CET","CET"),
                ("EST","EST")])

    mon = BooleanField('Monday')
    tue = BooleanField('Tuesday')
    wed = BooleanField('Wednesday')
    thu = BooleanField('Thursday')
    fri = BooleanField('Friday')
    sat = BooleanField('Saturday')
    sun = BooleanField('Sunday')

class ProposeScrimForm(Form):
    team = SelectField('team', choices=[])
    time_zone = SelectField('time_zone', choices=[])
    day = SelectField('day', choices=[])
    start_time = SelectField('start_time', choices=[])
    utc_time = TextField('utc_time', validators=[Required()])
    map = TextField('map', validators=[Required()])
    type = SelectField('type', choices=[('4v4','4v4'),('6v6','6v6'),('9v9','9v9')])

class AcceptScrimForm(Form):
    map = TextField('map', validators=[Required()])


# HACK
def read_scrim_days(form):
    scrim_days    = list('0000000')
    scrim_days[0] = str(int(form.mon.data))
    scrim_days[1] = str(int(form.tue.data))
    scrim_days[2] = str(int(form.wed.data))
    scrim_days[3] = str(int(form.thu.data))
    scrim_days[4] = str(int(form.fri.data))
    scrim_days[5] = str(int(form.sat.data))
    scrim_days[6] = str(int(form.sun.data))
    scrim_days    = ''.join(scrim_days)
    return scrim_days