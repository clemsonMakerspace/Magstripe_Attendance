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
    #===========================================================================
    # Compile regex for CUID on Tiger One card. Do this here to avoid duplicates
    #===========================================================================
    def __init__(self):
        self.regex = re.compile("%(.+)..\?;")
    
    
    #===========================================================================
    # Sanitize inputs to save your database
    #===========================================================================
    def sanitizeInput(self, input):
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
    
    
    #===========================================================================
    # Listen for card swipe as a password and then regex it for CUID
    #===========================================================================
    def getCardSwipe(self):
        # Read the card data as a password so it doesn't show on the screen
        cardID = self.sanitizeInput(getpass.getpass("\nWaiting for card swipe..."))
        try:
            # Return the card ID
            return self.regex.search(cardID).group(1)
        except AttributeError:
            # If exit or back, just return to go back
            if "exit" in cardID or "back" in cardID:
                return c.BACK
            # Else, a match wasn't found which probably means there was
            # ann error reading the card or the card isn't a Tiger One card
            # but assume the former
            else:
                return c.ERROR_READING_CARD
