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
    (ETF_DIVISION_6,ETF_DIVISION_6)]
        
FILTER_SKILLS = [(ALL, ALL)]
FILTER_SKILLS.extend(CHOICES_SKILLS)

TIME_EDT = "EDT", TIME_EDT_OFF = "-0400"
TIME_CLT = "CLI", TIME_CLT_OFF = "-0400"
TIME_BRT = "BRT", TIME_BRT_OFF = "-0300"
TIME_UTC = "GMT/UTC", TIME_UTC_OFF = "+0000"
TIME_CET = "CET", TIME_CET_OFF = "+0100"
TIME_RST = "RST", TIME_RST_OFF = "+0000"
TIME_AUS = "AUS", TIME_AUS_OFF = "+0000"
TIME_NZ  = "NZ", TIME_NZ_OFF = "+1200"

ZONES_DICT = [
    {
        'time': TIME_EDT,
        'offset': TIME_EDT_OFF, 
    },
    {
        'time': TIME_CLT,
        'offset': TIME_CLT_OFF, 
    },
    {
        'time': TIME_BRT,
        'offset': TIME_BRT_OFF, 
    },
    {
        'time': TIME_UTC,
        'offset': TIME_UTC_OFF, 
    },
    {
        'time': TIME_CET,
        'offset': TIME_CET_OFF, 
    },
    {
        'time': TIME_RST,
        'offset': TIME_RST_OFF, 
    },
    {
        'time': TIME_AUS,
        'offset': TIME_AUS_OFF, 
    },
    {
        'time': TIME_NZ,
        'offset': TIME_NZ_OFF, 
    },
]

CHOICES_ZONES = [
    (TIME_EDT,TIME_EDT),
    (TIME_CLI,TIME_CLT),
    (TIME_BRT,TIME_BRT),
    (TIME_UTC,TIME_UTC),
    (TIME_CET_OFF,TIME_CET),
    (TIME_RST,TIME_RST),
    (TIME_AUS,TIME_AUS),
    (TIME_NZ,TIME_NZ)]

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
    SCRIM_FINISHED]

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