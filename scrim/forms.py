from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField, TextAreaField
from wtforms.validators import Required, Length
from consts import *

class UserEditForm(Form):
    team_name           = TextField('team_name', validators = [Required()])
    #team_skill_level    = SelectField(u'team_skill_level', choices=[(UGC_IRON, UGC_IRON),(UGC_STEEL, UGC_STEEL),(UGC_SILVER, UGC_SILVER),(UGC_GOLD, UGC_GOLD), (UGC_PLATINUM, UGC_PLATINUM)])
    team_skill_level    = SelectField('team_skill_level', choices=CHOICES_SKILLS)
    team_time_zone      = SelectField('team_time_zone', choices=CHOICES_ZONES)

class BaseTeamForm(Form):
    team_name           = TextField('team_name', validators = [Required()])
    team_skill_level    = SelectField('team_skill_level', choices=CHOICES_SKILLS)
    team_time_zone      = SelectField('team_time_zone', choices=CHOICES_ZONES)

    mon = BooleanField('Monday')
    tue = BooleanField('Tuesday')
    wed = BooleanField('Wednesday')
    thu = BooleanField('Thursday')
    fri = BooleanField('Friday')
    sat = BooleanField('Saturday')
    sun = BooleanField('Sunday')

class TeamEditForm(BaseTeamForm):
    time_from = SelectField('time_from',
            choices=[("8:00","8:00"),
                ("9:00","9:00"),
                ("10:00","10:00")])

class CreateTeamForm(BaseTeamForm):
    pass
    
class TeamCommentForm(Form):
    text                = TextAreaField('text', validators=[Required()])

class SearchTeamForm(Form):
    team_skill_level  = SelectField('team_skill_level', choices=FILTER_SKILLS)
    team_time_zone    = SelectField('team_time_zone', choices=FILTER_ZONES)

    mon = BooleanField('Monday')
    tue = BooleanField('Tuesday')
    wed = BooleanField('Wednesday')
    thu = BooleanField('Thursday')
    fri = BooleanField('Friday')
    sat = BooleanField('Saturday')
    sun = BooleanField('Sunday')

    def read_scrim_days(self):
        scrim_days    = list('0000000')
        scrim_days[0] = str(int(self.mon.data))
        scrim_days[1] = str(int(self.tue.data))
        scrim_days[2] = str(int(self.wed.data))
        scrim_days[3] = str(int(self.thu.data))
        scrim_days[4] = str(int(self.fri.data))
        scrim_days[5] = str(int(self.sat.data))
        scrim_days[6] = str(int(self.sun.data))
        scrim_days    = ''.join(scrim_days)
        return scrim_days

    def reset(self):
        self.team_skill_level.data = 'ALL'
        self.team_time_zone.data = 'ALL'
        self.mon.data = False
        self.tue.data = False
        self.wed.data = False
        self.thu.data = False
        self.fri.data = False
        self.sat.data = False
        self.sun.data = False

class FilterTeamForm(SearchTeamForm):
    team_name = TextField('team_name')

    def reset(self):
        super(FilterTeamForm, self).reset()
        self.team_name.data = ''

class FilterScrimForm(SearchTeamForm):
    clear = BooleanField('Clear')

    def reset(self):
        super(FilterScrimForm, self).reset()
        self.clear.data = False

class ProposeScrimForm(Form):
    team       = SelectField('team', choices=[])
    time_zone  = SelectField('time_zone', choices=[])
    day        = SelectField('day', choices=[])
    start_time = SelectField('start_time', choices=[])
    utc_time   = TextField('utc_time', validators=[Required()])
    map        = TextField('map', validators=[Required()])
    type       = SelectField('type', choices=[('4v4','4v4'),('6v6','6v6'),('9v9','9v9')])

class AcceptScrimForm(Form):
    map = TextField('map', validators=[Required()])
