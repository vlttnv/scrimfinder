ALL             = "ALL"

UGC_PLATINUM    = "UGC Platinum"
UGC_GOLD        = "UGC Gold"
UGC_SILVER      = "UGC Silver"
UGC_STEEL       = "UGC Steel"
UGC_IRON        = "UGC Iron"

ETF_PREMIERSHIP = "ETF2L Premiership"
ETF_DIVISION_1  = "ETF2L Division 1"
ETF_DIVISION_2  = "ETF2L Division 2"
ETF_DIVISION_3  = "ETF2L Division 3"
ETF_DIVISION_4  = "ETF2L Division 4"
ETF_DIVISION_5  = "ETF2L Division 5"
ETF_DIVISION_6  = "ETF2L Division 6"

HIGHLANDER_OPEN = "Highlander Open"
ESEA_OPEN = "ESEA Open"
ESEA_INTER = "ESEA Intermediate"
ESEA_INV = "ESEA Invite"

CHOICES_TEAM_TYPE = [("4v4","4v4"),("6v6","6v6"),("9v9","9v9")]
FILTER_TEAM_TYPE = [(ALL, ALL)]
FILTER_TEAM_TYPE.extend(CHOICES_TEAM_TYPE)

CHOICES_CLASSES = [("Medic","Medic"),("Heavy","Heavy"),("Demoman","Demoman"),("Soldier","Soldier"),("Scout","Scout"),("Pyro","Pyro"),("Engineer","Engineer"),("Spy","Spy"),("Sniper","Sniper")]


CHOICES_SKILLS = [
    (UGC_PLATINUM,UGC_PLATINUM),
    (UGC_GOLD,UGC_GOLD),
    (UGC_SILVER,UGC_SILVER),
    (UGC_STEEL,UGC_STEEL),
    (UGC_IRON,UGC_IRON),
    (ETF_PREMIERSHIP,ETF_PREMIERSHIP),
    (ETF_DIVISION_1,ETF_DIVISION_1),
    (ETF_DIVISION_2,ETF_DIVISION_2),
    (ETF_DIVISION_3,ETF_DIVISION_3),
    (ETF_DIVISION_4,ETF_DIVISION_4),
    (ETF_DIVISION_5,ETF_DIVISION_5),
    (ETF_DIVISION_6,ETF_DIVISION_6),
    (HIGHLANDER_OPEN, HIGHLANDER_OPEN),
    (ESEA_OPEN,ESEA_OPEN),
    (ESEA_INTER,ESEA_INTER),
    (ESEA_INV,ESEA_INV)
]
        
FILTER_SKILLS = [(ALL, ALL)]
FILTER_SKILLS.extend(CHOICES_SKILLS)
TIME_ZONES_DICT = [
    {
        'label': "UTC",
        'time_zone': "Etc/UTC"
    },
    {
        'label': "CET",
        'time_zone': "CET"
    },
    {
        'label': "PDT (UTC-8)",
        'time_zone': "America/Los_Angeles"
    },
    {
        'label': "MDT (UTC-7)",
        'time_zone': "America/Denver"
    },
    {
        'label': "CDT (UTC-6)",
        'time_zone': "America/Chicago"
    },
    {
        'label': "EDT (UTC-5)",
        'time_zone': "America/New_York"
    },
    {
        'label': "UTC+0",
        'time_zone': "Europe/London"
    },
    {
        'label': "UTC+1",
        'time_zone': "Europe/Amsterdam"
    },
    {
        'label': "UTC+2",
        'time_zone': "Europe/Sofia"
    },
    {
        'label': "UTC+4",
        'time_zone': "Europe/Moscow"
    },
    {

        'label': "UTC+8",
        'time_zone': "Asia/Singapore"
    },
    {
        'label': "UTC+9",
        'time_zone': "Asia/Seoul"
    }, 
    {
        'label': "UTC+10",
        'time_zone': "Australia/Sydney"
    }
]


TIME_ZONES_DICT_SHORT = [
    {
        'label': "UTC",
        'time_zone': "Etc/UTC"
    },
    {
        'label': "CET",
        'time_zone': "CET"
    },
    {
        'label': "Los Angeles (PDT/UTC-8)",
        'time_zone': "America/Los_Angeles"
    },
    {
        'label': "Seoul (UTC+9)",
        'time_zone': "Asia/Seoul"
    },
    {
        'label': "Sydney (UTC+10)",
        'time_zone': "Australia/Sydney"
    },
    {
        'label': "Amsterdam (UTC+1)",
        'time_zone': "Europe/Amsterdam"
    }
]

CHOICES_ZONES = []
for time in TIME_ZONES_DICT:
    CHOICES_ZONES.append((time['time_zone'], time['label']))

FILTER_ZONES = [(ALL, ALL)]
FILTER_ZONES.extend(CHOICES_ZONES)

# scrim states
SCRIM_PROPOSED = "Proposed"
SCRIM_ACCEPTED = "Accepted"
SCRIM_REJECTED = "Rejected"
SCRIM_FINISHED = "Finished"

SCRIM_STATES   = [
    SCRIM_PROPOSED,
    SCRIM_ACCEPTED,
    SCRIM_REJECTED,
    SCRIM_FINISHED
]

# sub scrim states
SCRIM_RECEIVED = "Received"
SCRIM_SENT     = "Sent"

# scrim results
SCRIM_LOST = "Lost"
SCRIM_WON  = "Won"
SCRIM_TIE  = "Tie"

SCRIM_RESULTS  = [
    SCRIM_LOST,
    SCRIM_WON,
    SCRIM_TIE]
