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

# Even though MySQLdb performs input sanitization internally, 
# it doesn't hurt to do it oursevles just to be on the safe side
def sanitizeInput(input):
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
