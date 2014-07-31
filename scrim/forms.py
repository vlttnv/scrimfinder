from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField, TextAreaField
from wtforms.validators import Required, Length
from consts import *

# USER

class EditUserForm(Form):
    skill_level = SelectField('skill_level', choices=CHOICES_SKILLS)
    main_class  = SelectField('main_class', choices=CHOICES_CLASSES)
    is_merc     = BooleanField('Merc')

# SCRIM DAYS

class BaseScrimDay(Form):
    mon = BooleanField('Monday', default=True)
    tue = BooleanField('Tuesday', default=True)
    wed = BooleanField('Wednesday', default=True)
    thu = BooleanField('Thursday', default=True)
    fri = BooleanField('Friday', default=True)
    sat = BooleanField('Saturday', default=True)
    sun = BooleanField('Sunday', default=True)

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

    def fill_scrim_days(self, scrim_days):
        self.mon.data = bool(int(scrim_days[0]))
        self.tue.data = bool(int(scrim_days[1]))
        self.wed.data = bool(int(scrim_days[2]))
        self.thu.data = bool(int(scrim_days[3]))
        self.fri.data = bool(int(scrim_days[4]))
        self.sat.data = bool(int(scrim_days[5]))
        self.sun.data = bool(int(scrim_days[6]))

    def reset_scrim_days(self):
        self.mon.data = True
        self.tue.data = True
        self.wed.data = True
        self.thu.data = True
        self.fri.data = True
        self.sat.data = True
        self.sun.data = True

# CREATE TEAM

class CreateTeamForm(BaseScrimDay):
    team_name        = TextField('team_name', validators=[Required()])
    team_skill_level = SelectField('team_skill_level', choices=CHOICES_SKILLS)
    team_time_zone   = SelectField('team_time_zone', choices=CHOICES_ZONES)
    team_type        = SelectField('team_type', choices=CHOICES_TEAM_TYPE)

class EditTeamForm(CreateTeamForm):
    team_type        = SelectField('team_type', choices=CHOICES_TEAM_TYPE)
    #time_from = SelectField('time_from', 
    #                choices=[("8:00","8:00"),("9:00","9:00"),("10:00","10:00")])

class CommentTeamForm(Form):
    text = TextAreaField('text', validators=[Required()])

# SEARCHES

class BaseSearchForm(Form):
    clear = BooleanField('Clear')

    def reset_clear(self):
        self.clear.data = False;

class TeamSearchForm(BaseSearchForm, BaseScrimDay):
    team_name = TextField('team_name')
    team_skill_level = SelectField('team_skill_level', choices=FILTER_SKILLS)
    team_time_zone   = SelectField('team_time_zone', choices=FILTER_ZONES)

    def reset_team_search(self):
        super(TeamSearchForm, self).reset_clear()
        super(TeamSearchForm, self).reset_scrim_days()
        self.team_name.data = ""
        self.team_skill_level.data = "ALL"
        self.team_time_zone.data = "ALL"

# FILTER

class FilterUserForm(BaseSearchForm):
    nickname = TextField('nickname')
    steam_id = TextField('steam_id')
    is_merc  = BooleanField('is_merc')

    def reset_user_filter(self):
        super(FilterUserForm, self).reset_clear()
        self.nickname.data = ""
        self.steam_id.data = ""
        self.is_merc.data  = False

class FilterTeamForm(TeamSearchForm):
    
    def reset_team_filter(self):
        super(FilterTeamForm, self).reset_team_search()

class FilterScrimForm(TeamSearchForm):

    def reset_scrim_filter(self):
        super(FilterScrimForm, self).reset_team_search()

class FilterSinglesForm(TeamSearchForm):

    def reset_singles_filter(self):
        super(FilterSinglesForm, self).reset_team_search()

# SCRIM PROPOSAL

class ProposeScrimForm(Form):
    """
    The empty choices should be populated dynamically.

    See /scrim/propose/<int:team_id>
    """

    team       = SelectField('team', choices=[])
    time_zone  = SelectField('time_zone', choices=[])
    day        = SelectField('day', choices=[])
    start_time = SelectField('start_time', choices=[])
    utc_time   = TextField('utc_time', validators=[Required()])
    map        = TextField('map', validators=[Required()])
    type       = SelectField('type', choices=[('4v4','4v4'),('6v6','6v6'),('9v9','9v9')])

class AcceptScrimForm(Form):
    map = TextField('map', validators=[Required()])

# SINGLE SCRIM

class AddSingleScrim(Form):
    comment = TextAreaField('text', validators=[Required()])
    type        = SelectField('team_type', choices=CHOICES_TEAM_TYPE)
    maps        = TextField('maps', validators=[Required()])
    time_zone   = SelectField('time_zone', choices=CHOICES_ZONES)
    skill_level = SelectField('skill_level', choices=CHOICES_SKILLS)
