#===============================================================================
#    Magstripe Attendance Database System
#===============================================================================
#
#    Magstripe Attendance is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Magstripe Attendance is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>. 
#===============================================================================

from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal

from dbUtil import DB
import constants as c


class LoginThread(QThread):
    postLoginSignal = pyqtSignal(int, object)

    def __init__(self, dbHost, dbDatabase, dbUsersTable, dbVisitsTable, dbUser, dbPass, postLoginCallback):
        super(LoginThread, self).__init__()
        self.dbHost = dbHost
        self.dbDatabase = dbDatabase
        self.dbUsersTable = dbUsersTable
        self.dbVisistsTable = dbVisitsTable
        self.dbUser = dbUser
        self.dbPass = dbPass

        self.postLoginSignal.connect(postLoginCallback)

   
    def run(self):
    #===========================================================================
    # Initialize db object and connect to database
    #===========================================================================
        # Init the db object
        db = DB(self.dbHost, self.dbDatabase, self.dbTable, self.dbUser, self.dbPass)

        # Connect to the remote database server
        loginStatus = db.connect()
   
        self.postLoginSignal.emit(loginStatus, db)


class CheckinThread(QThread):
    postCardSwipeSignal = pyqtSignal(int, str, str, object)

    def __init__(self, db, postCardSwipeCallback):
        super(CheckinThread, self).__init__()

        self.db = db
        self.CUID = None

        self.postCardSwipeSignal.connect(postCardSwipeCallback)


    def setCUID(self, CUID):
    #===========================================================================
    # set CUID
    #===========================================================================
        self.CUID = CUID

   
    def run(self):
    #===========================================================================
    # Verify CUID card length, and attempt checkIn. Return results.
    #===========================================================================
        # Warning: setCUID() must have been called before starting this thread

        # At least make sure the card ID is of the right length. Not much more validation can be done.
        if len(self.CUID) != 9:
            self.postCardSwipeSignal.emit(c.ERROR_READING_CARD, '', '', object())
            return
      
        checkInResult = self.db.checkIn(self.CUID)

        # Don't pass nonetype's through signals expecting an object or seg faults happen
        if checkInResult["sqlError"] is None:
            checkInResult["sqlError"] = object()

        self.postCardSwipeSignal.emit(checkInResult["checkInStatus"], checkInResult["userID"], checkInResult["CUID"], checkInResult["sqlError"])


class AddCardThread(QThread):
    cardAddedSignal = pyqtSignal(int, str, str, object)

    def __init__(self, db, CUID, userID, cardAddedCallback):
        super(AddCardThread, self).__init__()

        self.db = db
        self.CUID = CUID
        self.userID = userID

        self.cardAddedSignal.connect(cardAddedCallback)

   
    def run(self):
    #===========================================================================
    # Request additional data about new card then send to db
    #===========================================================================
        addCardResult = self.db.addCard(self.CUID, self.userID)

        # Don't send nonetype's through signals
        if addCardResult['sqlError'] is None:
            addCardResult['sqlError'] = object()

        self.cardAddedSignal.emit(addCardResult["addCardStatus"], addCardResult["userID"], addCardResult["CUID"], addCardResult["sqlError"])


class ShowVisitsThread(QThread):
    showVisitsSignal = pyqtSignal(int, object, object)

    def __init__(self, db, userID, showVisitsCallback):
        super(ShowVisitsThread, self).__init__()

        self.db = db
        self.userID = userID

        self.showVisitsSignal.connect(showVisitsCallback)
   

    def setUserID(self, userID):
    #===========================================================================
    # set User ID
    #===========================================================================
        self.userID = userID

   
    def run(self):
    #===========================================================================
    # Connect to db and request visits information - then return
    #===========================================================================
        showVisitsResult = self.db.showVisits(self.userID)

        # Don't send nonetype's through a signal or it gets angry and seg faults
        if showVisitsResult["sqlError"] is None:
            showVisitsResult["sqlError"] = object()
        if showVisitsResult["visitsTuple"] is None:
            showVisitsResult["visitsTuple"] = object()

        self.showVisitsSignal.emit(showVisitsResult["showVisitsStatus"], showVisitsResult["visitsTuple"], showVisitsResult["sqlError"])


class SleepThread(QThread):
    wakeupSignal = pyqtSignal()

    def __init__(self, time, wakeupCallback):
        super(SleepThread, self).__init__()

        self.time = time
        self.wakeupSignal.connect(wakeupCallback)


    def setTime(self, time):
    #===========================================================================
    # set the time
    #===========================================================================
        self.time = time


    def getTime(self):
    #===========================================================================
    # Get the time
    #===========================================================================
        return self.time


    def run(self):
    #===========================================================================
    # Wait for an amount of time
    #===========================================================================
        sleep(self.time)
        self.wakeupSignal.emit()
