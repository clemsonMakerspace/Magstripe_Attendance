Clemson University Makerspace Magstripe Attendance Tracker (CUMMAT)
=======================

#### Owen Phillips (ophilli@clemson.edu)

### Dependencies

This is a Python 3.x program depending on the following additional libraries
   1. `PyQt` - Python bindings for QT
   1. `psycopg2` - Python Postgres library

### Configuration

This program requires a database server (remote or local), that is configurable in 'Constants.py' or may be selected during login.

For the database, this application expects two tables - users & checkIns

Setup the users table with 3 columns: 
   1. card ID        - card ID from ID card (`varchar`, `primary key`)
   1. user ID        - university username (`varchar`)
   1. visits         - the number of check-ins (`int`)
   
Setup the checkIns table with 2 columns:
   1. card ID
   1. checkIn  - the time of last check-in (`timestamp`)
   
This application was built for a card reader that uses keyboard emulation. You can type the card info in, but a card reader is suggested.

### Usage

Simply run "./Check-in.py" to start the GUI.

There is also a text-only mode. This can be started by using the "--nogui" argument.
In text mode, enter "back" at any time to go up a menu level or exit the check-in loop.

To populate your database, select the check-in option and begin adding users.

After your database is populated you can use the "Show Points" option to show a single user's points or view a pretty
table of all users in descending order from most to least points.

By default a card is only allowed to check-in once per hour to prevent abuse. This can
be modified by changing the value of `ALLOW_CHECKIN_WITHIN_HOUR` in `Constants.py`.

### Packaging

A PyInstaller .spec file is provided to package the program and all dependencies into a single binary file for Linux, Windows, or Mac.

To create this binary, download PyInstaller and run `make.py dist [path to pyinstaller]`. The resulting binary will be in the `dist` directory.
Alternatively, precompiled binaries are available on the releases page on the GitHub repo.

### License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
