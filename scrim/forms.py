from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField
from wtforms.validators import Required, Length
from consts import *

class EditForm(Form):
    team_name           = TextField('team_name', validators = [Required()])
    team_skill_level    = SelectField(u'team_skill_level', choices=[(UGC_IRON, UGC_IRON),(UGC_STEEL, UGC_STEEL),(UGC_SILVER, UGC_SILVER),(UGC_GOLD, UGC_GOLD), (UGC_PLATINUM, UGC_PLATINUM)])
    team_time_zone      = SelectField('team_time_zone', choices=[("CET","CET"),("EST","EST")])

class AvailabilityForm(Form):
    day = SelectField('day', choices=[("Monday", "Monday"),("Tuesday","Tuesday"),("Wednesday","Wednesday"),("Thursday","Thursday"),("Friday","Friday"),("Saturday","Saturday"),("Sunday","Sunday")])
    time_from = SelectField('time_from', choices=[("8:00","8:00"),("9:00","9:00"),("10:00","10:00")])
    time_to = SelectField('time_to', choices=[("8:00","8:00"),("9:00","9:00"),("10:00","10:00")])

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
