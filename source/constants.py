#===============================================================================
#    Magstripe Attendance Database System
#===============================================================================
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>. 
#===============================================================================

VERSION = "6.0"
GROUP_NAME = "Clemson University Makerspace"
GROUP_INITIALS = "CMS"

DEFAULT_HOST                = "localhost"
DEFAULT_USER                = "test"
DEFAULT_DATABASE            = "test"
TABLE_USERS                 = "users"
TABLE_VISITS                = "visits"
DEFAULT_VISITS              = 0
ALLOW_CHECKIN_WITHIN_HOUR   = 1
TIME_BETWEEN_CHECKINS       = 2 # In seconds

CUID_COLUMN_USER            = "cuid"
LAST_CHECKIN_COLUMN_USER    = "last_checkin"
FIRST_NAME_COLUMN_USER      = "first_name"
LAST_NAME_COLUMN_USER       = "last_name"
EMAIL_COLUMN_USER           = "email"
ISIN_COLUMN_USER            = "isIn"
VISIT_NUM_COLUMN_USER       = "visit_num"

CUID_COLUMN_VISIT           = "cuid"
VISIT_NUM_COLUMN_VISIT      = "visit_num"
TIMEIN_COLUMN_VISIT         = "timeIn"
TIMEOUT_COLUMN_VISIT        = "timeOut"

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
CUID_NOT_IN_DB      = 3
BAD_CHECKIN_TIME    = 4
FUTURE_CHECKIN_TIME = 5
SQL_ERROR           = 6
NO_RESULTS          = 7
