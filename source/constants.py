VERSION = "6.0"
GROUP_NAME = "Clemson University Makerspace"
GROUP_INITIALS = "CMS"

DEFAULT_HOST                = "localhost"
DEFAULT_USER                = "user"
DEFAULT_DATABASE            = "user"
DEFAULT_TABLE               = "visits_spring_16"
DEFAULT_POINTS              = 0
ALLOW_CHECKIN_WITHIN_HOUR   = 0
TIME_BETWEEN_CHECKINS       = 2 # In seconds

# TextUtil constants
BACK = 10

# Generic return codes
SUCCESS = 0
FAILURE = -1

# Login errors
BAD_PASSWD = 2

# Card swipe errors
ERROR_READING_CARD = 11

# Database errors
CARD_NOT_IN_DB      = 3
BAD_CHECKIN_TIME    = 4
FUTURE_CHECKIN_TIME = 5
SQL_ERROR           = 6
NO_RESULTS          = 7
