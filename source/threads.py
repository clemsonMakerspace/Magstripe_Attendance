#===============================================================================
#    Magstripe Attendance Database System
#===============================================================================
#    Copyright (C) 2015 Owen Phillips
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

from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal

from dbUtil import DB
import constants as c


class LoginThread(QThread):
    postLoginSignal = pyqtSignal(int, object)

    def __init__(self, dbHost, dbDatabase, dbTable, dbUser, dbPass, postLoginCallback):
        super(LoginThread, self).__init__()
        self.dbHost = dbHost
        self.dbDatabase = dbDatabase
        self.dbTable = dbTable
        self.dbUser = dbUser
        self.dbPass = dbPass

        self.postLoginSignal.connect(postLoginCallback)

   
    def run(self):
        # Init the db object
        db = DB(self.dbHost, self.dbDatabase, self.dbTable, self.dbUser, self.dbPass)

        # Connect to the remote database server
        loginStatus = db.connect()
   
        self.postLoginSignal.emit(loginStatus, db)


class CheckinThread(QThread):
    postCardSwipeSignal = pyqtSignal(int, str, str, object, str)

    def __init__(self, db, pointValue, postCardSwipeCallback):
        super(CheckinThread, self).__init__()

        self.db = db
        self.pointValue = str(pointValue)
        self.cardID = None

        self.postCardSwipeSignal.connect(postCardSwipeCallback)


    def setCardID(self, cardID):
        self.cardID = cardID
   
    def run(self):
        # Warning: setCardID() must have been called before starting this thread

        # At least make sure the card ID is of the right length. Not much more validation can be done.
        if len(self.cardID) != 16:
            self.postCardSwipeSignal.emit(c.ERROR_READING_CARD, '', '', object(), self.pointValue)
            return
      
        checkinResult = self.db.checkin(self.cardID, self.pointValue)

        # Don't pass nonetype's through signals expecting an object or seg faults happen
        if checkinResult["sqlError"] is None:
            checkinResult["sqlError"] = object()

        self.postCardSwipeSignal.emit(checkinResult["checkinStatus"], checkinResult["userID"], checkinResult["cardID"], checkinResult["sqlError"], self.pointValue)


class AddCardThread(QThread):
    cardAddedSignal = pyqtSignal(int, str, str, object, str)

    def __init__(self, db, cardID, userID, pointValue, cardAddedCallback):
        super(AddCardThread, self).__init__()

        self.db = db
        self.pointValue = str(pointValue)
        self.cardID = cardID
        self.userID = userID

        self.cardAddedSignal.connect(cardAddedCallback)

   
    def run(self):
        addCardResult = self.db.addCard(self.cardID, self.userID, self.pointValue)

        # Don't send nonetype's through signals
        if addCardResult['sqlError'] is None:
            addCardResult['sqlError'] = object()

        self.cardAddedSignal.emit(addCardResult["addCardStatus"], addCardResult["userID"], addCardResult["cardID"], addCardResult["sqlError"], self.pointValue)


class ShowVisitsThread(QThread):
    showVisitsSignal = pyqtSignal(int, object, object)

    def __init__(self, db, userID, showVisitsCallback):
        super(ShowVisitsThread, self).__init__()

        self.db = db
        self.userID = userID

        self.showVisitsSignal.connect(showVisitsCallback)
   

    def setUserID(self, userID):
        self.userID = userID
   
    def run(self):
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
        self.time = time

    def getTime(self):
        return self.time

    def run(self):
        sleep(self.time)
        self.wakeupSignal.emit()
