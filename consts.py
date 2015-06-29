ALL             = "ALL"

UGC_PLATINUM    = "UGC Platinum"
UGC_GOLD        = "UGC Gold"
UGC_SILVER      = "UGC Silver"
UGC_STEEL       = "UGC Steel"
UGC_IRON        = "UGC Iron"
UGC_ASIA_GOLD   = "UGC Asia Gold"
UGC_ASIA_STEEL  = "UGC Asia Steel"

ETF_PREMIERSHIP = "ETF2L Premiership"
ETF_OPEN  = "ETF2L Open"
ETF_MID  = "ETF2L Mid"
ETF_HIGH  = "ETF2L High"

AUSTRALIA_NEWZ  = "Australia/New Zealand"

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
    (UGC_ASIA_GOLD,UGC_ASIA_GOLD),
    (UGC_ASIA_STEEL,UGC_ASIA_STEEL),
    (ETF_PREMIERSHIP,ETF_PREMIERSHIP),
    (ETF_OPEN,ETF_OPEN),
    (ETF_MID,ETF_MID),
    (ETF_HIGH,ETF_HIGH),
    (HIGHLANDER_OPEN, HIGHLANDER_OPEN),
    (ESEA_OPEN,ESEA_OPEN),
    (ESEA_INTER,ESEA_INTER),
    (ESEA_INV,ESEA_INV),
    (AUSTRALIA_NEWZ,AUSTRALIA_NEWZ)
]

FILTER_SKILLS = [(ALL, ALL)]
FILTER_SKILLS.extend(CHOICES_SKILLS)
TIME_ZONES_DICT = [
    {
        'label': "UTC",
        'time_zone': "+00:00"
    },
    {
        'label': "CET (UTC+1)",
        'time_zone': "+01:00"
    },
    {
        'label': "CEST (UTC+2)",
        'time_zone': "+02:00"
    },
    {
        'label': "PDT (UTC-7)",
        'time_zone': "-07:00"
    },
    {
        'label': "MDT (UTC-6)",
        'time_zone': "-06:00"
    },
    {
        'label': "CDT (UTC-5)",
        'time_zone': "-05:00"
    },
    {
        'label': "EDT (UTC-4)",
        'time_zone': "-04:00"
    },
    {
        'label': "EEST (UTC+3)",
        'time_zone': "+03:00"
    },
    {
        'label': "MSK (UTC+4)",
        'time_zone': "+04:00"
    },
    {

        'label': "SGT (UTC+8)",
        'time_zone': "+08:00"
    },
    {
        'label': "KST (UTC+9)",
        'time_zone': "+09:00"
    },
    {
        'label': "AEST (UTC+10)",
        'time_zone': "+10:00"
    }
]


TIME_ZONES_DICT_SHORT = [
    {
        'label': "UTC",
        'time_zone': "+00:00"
    },
    {
        'label': "CET (UTC+1)",
        'time_zone': "+01:00"
    },
    {
        'label': "CEST (UTC+2)",
        'time_zone': "+02:00"
    },
    {
        'label': "PDT (UTC-7)",
        'time_zone': "-07:00"
    },
    {
        'label': "SGT (UTC+8)",
        'time_zone': "+08:00"
    },
    {
        'label': "AEST (UTC+10)",
        'time_zone': "+10:00"
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
