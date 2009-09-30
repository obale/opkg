#!/usr/bin/python
# -*- coding: utf-8 -*-
# opkg.py - Searching and Installing packages on http://www.opkg.org
#
# (C) 2009 by MokSec Project
# Written by Alex Oberhauser <oberhauseralex@networld.to>
# All Rights Reserved
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# hut WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>
import sys
import os
import signal
import socket
import sqlite3
from optparse import OptionParser
from modules import OPKG
from modules import OPKGUpgrade

def sigint(signum, frame):
    print "Thank you for using this piece of software"
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint)
    parser = OptionParser()
    parser.add_option("-n", "--number", type="int", dest="number", help="print information about the package NUMBER", metavar="NUMBER")
    parser.add_option("-s", "--search", type="str", dest="searchterm", help="search for the PACKAGE", metavar="PACKAGE")
    parser.add_option("-a", "--all", action="store_true", dest="all", help="show all packages in the list")
    parser.add_option("-u", "--update", action="store_true", dest="update", help="update the local database")
    parser.add_option("-U", "--upgrade", action="store_true", dest="upgrade", help="update the local database")
    parser.add_option("-i", "--install", action="store_true", dest="install", help="install the package")

    (options, args) = parser.parse_args()

    opkg = OPKG.OPKG()
    opkgupgrade = OPKGUpgrade.OPKGUpgrade()
    if not os.path.isfile('opkg.db') and not options.update:
        print "No database found! Please wait until the update process if finished..."
        opkg.savePackages()
        assert os.path.isfile('opkg.db')

    if options.update:
        opkg.savePackages()
    elif options.upgrade:
        opkgupgrade.upgrade()
    if options.number is not None:
        opkg.getPackageByNumber(options.number, options.install)
    elif options.searchterm is not None:
        opkg.getPackageBySearchterm(options.searchterm, options.install)
    elif options.all:
        opkg.getAllPackages()
        if options.install:
            print "Can't install all packages!"
