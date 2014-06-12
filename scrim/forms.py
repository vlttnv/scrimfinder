from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField
from wtforms.validators import Required, Length
from consts import *

class UserEditForm(Form):
    team_name           = TextField('team_name', validators = [Required()])
    team_skill_level    = SelectField(u'team_skill_level', choices=[(UGC_IRON, UGC_IRON),(UGC_STEEL, UGC_STEEL),(UGC_SILVER, UGC_SILVER),(UGC_GOLD, UGC_GOLD), (UGC_PLATINUM, UGC_PLATINUM)])
    team_time_zone      = SelectField('team_time_zone', choices=[("CET","CET"),("EST","EST")])

class TeamEditForm(Form):
    team_name           = TextField('team_name')
    team_skill_level    = SelectField('team_skill_level', 
            choices=[(UGC_IRON, UGC_IRON),
                (UGC_STEEL, UGC_STEEL),
                (UGC_SILVER, UGC_SILVER),
                (UGC_GOLD, UGC_GOLD), 
                (UGC_PLATINUM, UGC_PLATINUM)])
    team_time_zone      = SelectField('team_time_zone', 
            choices=[("CET","CET"),
                ("EST","EST")])

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


class CreateTeamForm(Form):
    team_name           = TextField('team_name', validators = [Required()])
    team_skill_level    = SelectField(u'team_skill_level', 
            choices=[(UGC_IRON, UGC_IRON),
                (UGC_STEEL, UGC_STEEL),
                (UGC_SILVER, UGC_SILVER),
                (UGC_GOLD, UGC_GOLD), 
                (UGC_PLATINUM, UGC_PLATINUM)])
    team_time_zone      = SelectField('team_time_zone', 
            choices=[("CET","CET"),
                ("EST","EST")])

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
    # team_skill_level    = SelectField(u'team_skill_level', 
    #         choices=[(ALL, ALL),
    #             (UGC_IRON, UGC_IRON),
    #             (UGC_STEEL, UGC_STEEL),
    #             (UGC_SILVER, UGC_SILVER),
    #             (UGC_GOLD, UGC_GOLD), 
    #             (UGC_PLATINUM, UGC_PLATINUM)])
    time_zone = SelectField('team_time_zone', choices=[])

    # mon = BooleanField('Monday')
    # tue = BooleanField('Tuesday')
    # wed = BooleanField('Wednesday')
    # thu = BooleanField('Thursday')
    # fri = BooleanField('Friday')
    # sat = BooleanField('Saturday')
    # sun = BooleanField('Sunday')

    @staticmethod
    def get_instance(time_zone):
        form = ProposeScrimForm()
        for t in time_zone:
            form.time_zone.choices.append((t, t))
        return form
