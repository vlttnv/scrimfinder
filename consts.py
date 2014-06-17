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
        
FILTER_SKILLS = list(CHOICES_SKILLS)
FILTER_SKILLS.append((ALL, ALL))

TIME_EDT = "EDT"
TIME_CLI = "CLI"
TIME_BRT = "BRT"
TIME_UTC = "GMT/UTC"
TIME_CET = "CET"
TIME_RST = "RST"
TIME_AUS = "AUS"
TIME_NZ  = "NZ"

CHOICES_ZONES = [
    (TIME_EDT,TIME_EDT),
    (TIME_CLI,TIME_CLI),
    (TIME_BRT,TIME_BRT),
    (TIME_UTC,TIME_UTC),
    (TIME_CET,TIME_CET),
    (TIME_RST,TIME_RST),
    (TIME_AUS,TIME_AUS),
    (TIME_NZ,TIME_NZ)]

FILTER_ZONES = list(CHOICES_ZONES)
FILTER_ZONES.append((ALL, ALL))

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

# scrim results
SCRIM_LOST = "Lost"
SCRIM_WON  = "Won"
SCRIM_TIE  = "Tie"

SCRIM_RESULTS  = [
    SCRIM_LOST,
    SCRIM_WON,
    SCRIM_TIE]