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

import sys
import re
import getpass

from dbUtil import DB
import sharedUtils
import constants as c

class TextUI:
    def __init__(self):
        self.db = None


    def start(self):
        # Compile the regex for pulling the card ID from all the data on a card
        # Do this here so it isn't done multiple times in the functions below
        self.regex = re.compile(";(.+)=")

        try:
            while 1:
                # Get DB info
                self.getDbInfo()

                # Create the DB object
                self.db = DB(self.dbHost, c.DEFAULT_DATABASE, self.dbTable, self.dbUser, self.dbPass)

                # Connect to the database
                connectStatus = self.connectToDatabase()

                # If we failed to connect to the database offer to re-enter db info
                if connectStatus != c.SUCCESS:
                    reenter = input("Failed to connect to database. Re-enter database info? (Y,n) ")
                if reenter.lower() == "n":
                    print("Bye.")
                    sys.exit(0)
                else:
                    break

            # Start the main menu loop
            self.displayMenu()

        except KeyboardInterrupt:
            pass
        finally:
            print("Cleaning up and exiting...")
            if self.db is not None:
                self.db.close()


    def displayMenu(self):
        print("\nType \"back\" at any time to go up a menu level.")

        while 1:
            # Display main menu
            print("\n\t1.) Check-in\n\t2.) Show Visits\n\t3.) Exit")
            try:
                option = input("\n>> ")

                if option == "1":
                    self.checkin()
                elif option == "2":
                    self.showVisits()
                elif option == "3":
                    sys.exit(0)
                elif option == "back" or option == "exit":
                    exit = input("Exit? (y,N) ")
                if exit.lower() == "y":
                    sys.exit(0)
                else:
                    self.invalidInput()

            except ValueError:
                self.invalidInput()

    def connectToDatabase(self):
        # Use stdout.write to prevent newline
        sys.stdout.write("Connecting to database...")

        # Connect to the DB!
        status = self.db.connect()

        if status == c.SUCCESS:
            print("done.")
            return status
        elif status == c.BAD_PASSWD:
            print("\nError connecting to database: Bad username or password.")
            return status
        else:
            print("\nUnknown Error connecting to database.")
            return c.FAILURE


    def checkin(self):
        # Get and validate the visit value for this check-in
        # Limited to 500 visits to prevent bad typos
        while 1:
            visitValue = sharedUtils.sanitizeInput(input("\nVisit Value (" + str(c.DEFAULT_VISITS) + "): "))

            # Validate visit input
            if visitValue == "":
                visitValue = str(c.DEFAULT_VISITS)
                break
            elif (visitValue.isdigit() and int(visitValue) <= 500) or visitValue == "back":
                break
            else:
                print("Invalid input. Try again.")

        while 1:
            cardID = self.getCardSwipe()

            # If the user requested to exit the loop, break
            if cardID == c.BACK:
                break
            elif cardID == c.ERROR_READING_CARD:
                print("Error reading card. Swipe card again.")
                continue

            # Sanitize cardID
            cardID = sharedUtils.sanitizeInput(cardID)
            # cardID will be empty if it failed sanitization. Skip checkin if that is the case
            if cardID == "":
                continue

            # Do the checkin
            checkinResult = self.db.checkin(cardID, visitValue)

            if checkinResult["checkinStatus"] == c.SQL_ERROR:
                self.showDatabaseError(checkinResult["sqlError"])
            elif checkinResult["checkinStatus"] == c.BAD_CHECKIN_TIME:
                print("Error: You may only check-in once per hour.")
            elif checkinResult["checkinStatus"] == c.FUTURE_CHECKIN_TIME:
                print("Error: Previous check-in time was in the future. Check your local system time.")
            elif checkinResult["checkinStatus"] == c.CARD_NOT_IN_DB:
                # Ask if user wants to add the card
                addCard = input("Error: Card not found in database. Add it now? (Y,n) ")
            
            if addCard == "n":
                continue
            
            # Get the userID for the new card
            userID = sharedUtils.sanitizeInput(input("User ID: "))

            # Add the card
            addCardResult = self.db.addCard(cardID, userID, visitValue)

            if addCardResult["addCardStatus"] == c.SUCCESS:
                self.showCheckinConfirmation(userID, visitValue)
            elif addCardResult["addCardStatus"] == c.SQL_ERROR:
                self.showDatabaseError(addCardResult["sqlError"])
            elif checkinResult["checkinStatus"] == c.SUCCESS:
                self.showCheckinConfirmation(checkinResult["userID"], visitValue)
            else:
                print("Unknown error checking in.")


    def showVisits(self):
        userID = sharedUtils.sanitizeInput(input("\nUser ID (blank for all): "))
        showVisitsResult = self.db.showVisits(userID)

        if showVisitsResult["showVisitsStatus"] == c.SQL_ERROR:
            self.showDatabaseError(showVisitsResult["sqlError"])
        elif showVisitsResult["showVisitsStatus"] == c.NO_RESULTS:
            print("\nThere were no results to that query.")
        elif showVisitsResult["showVisitsStatus"] == c.SUCCESS:
            # If showing all users, display a pretty table
            if userID == "":
                print("\n+--------------------+\n| User ID | Visits |\n+--------------------+")

                for i in range(len(showVisitsResult["visitsTuple"])):
                    print("|%10s | %6s |" % (showVisitsResult["visitsTuple"][i][0], showVisitsResult["visitsTuple"][i][1]))
                
                print("+--------------------+")
         
            # Show a single user's visits
            else:
                print("\n%s has %s visits." % (userID, str(showVisitsResult["visitsTuple"][0][0])))


    def getCardSwipe(self):
        # Read the card data as a password so it doesn't show on the screen
        cardID = sharedUtils.sanitizeInput(getpass.getpass("\nWaiting for card swipe..."))
        try:
            # Return the card ID
            return self.regex.search(cardID).group(1)
        except AttributeError:
            # If exit or back, just return to go back
            if "exit" in cardID or "back" in cardID:
                return c.BACK
            # Else, a match wasn't found which probably means there was
            # and error reading the card or the card isn't a PSU ID card
            # but assume the former
            else:
                return c.ERROR_READING_CARD


    def getDbInfo(self):
        self.dbHost = input("Database host: (" + c.DEFAULT_HOST + ") ")

        if self.dbHost == "":
            self.dbHost = c.DEFAULT_HOST

        self.dbTable = input("Database table: (" + c.DEFAULT_TABLE + ") ")

        if self.dbTable == "":
            self.dbTable = c.DEFAULT_TABLE

        self.dbUser = input("Database Username: (" + c.DEFAULT_USER + ") ")

        if self.dbUser == "":
            self.dbUser = c.DEFAULT_USER

        while 1:
            self.dbPass = getpass.getpass("Database Password: ")

            if self.dbPass == "":
                print("Database password cannot be blank.")
            else:
                break


    def showCheckinConfirmation(self, userID, visitValue):
        print("%s +%s visits" % (userID, visitValue))


    def showDatabaseError(self, error):
        print("\nWARNING! Database error:\n%s" % (error.args[1]))


    def invalidInput(self):
        print("Invalid option. Try again.")
