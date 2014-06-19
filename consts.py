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
    (ETF_DIVISION_6,ETF_DIVISION_6)
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
        'label': "Los Angeles",
        'time_zone': "America/Los_Angeles"
    },
    {
        'label': "Vancouver",
        'time_zone': "America/Vancouver"
    },
    {
        'label': "Seoul",
        'time_zone': "Asia/Seoul"
    },
    {
        'label': "Singapore",
        'time_zone': "Asia/Singapore"
    },
    {
        'label': "Perth",
        'time_zone': "Australia/Perth"
    },
    {
        'label': "Sydney",
        'time_zone': "Australia/Sydney"
    },
    {
        'label': "Amsterdam",
        'time_zone': "Europe/Amsterdam"
    },
    {
        'label': "London",
        'time_zone': "Europe/London"
    },
        {
        'label': "Luxembourg",
        'time_zone': "Europe/Luxembourg"
    },
    {
        'label': "Moscow",
        'time_zone': "Europe/Moscow"
    },
    {
        'label': "Sofia",
        'time_zone': "Europe/Sofia"
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