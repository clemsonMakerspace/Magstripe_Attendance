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

import re
import getpass  

class Utils:
    def __init__(self):
    #===========================================================================
    # Compile regex for CUID on Tiger One card. Do this here to avoid duplicates
    #===========================================================================
        self.regex = re.compile("%(.+)..\?;")
    
    
    def sanitizeInput(self, input):
    #===========================================================================
    # Sanitize inputs to save your database
    #===========================================================================
        # Keep a copy of the possibly mixed-case input
        origInput = input
        input.upper()

        # The reserved words to check for
        # There are many more, of course, but these should thwart the most dangerous attacks
        keywords = ["DELETE", "UPDATE", "DROP", "CREATE", "SELECT", "INSERT", "ALTER"]
  
        # Check for a match
        for i in keywords:
            if i in input:
                return ""
     
        # If no match, return the original input
        return origInput
    
    
    def getCardSwipe(self):
    #===========================================================================
    # Listen for card swipe as a password and then regex it for CUID
    #===========================================================================
        # Read the card data as a password so it doesn't show on the screen
        CUID = self.sanitizeInput(getpass.getpass("\nWaiting for card swipe..."))
        try:
            # Return the card ID
            return self.regex.search(CUID).group(1)
        except AttributeError:
            # If exit or back, just return to go back
            if "exit" in CUID or "back" in CUID:
                return c.BACK
            # Else card read error or not a Tiger One Card
            else:
                return c.ERROR_READING_CARD
