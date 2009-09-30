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
import sqlite3
from subprocess import call
import OPKG

class OPKGUpgrade:
    def __init__(self):
        self.installstr = ""
        pass

    def setInstalled(self, id, name, version):
        conn = sqlite3.connect('opkg.db')
        curs = conn.cursor()
        try:
            curs.execute('INSERT INTO installed VALUES(?, ?, ?)', (id, name, version))
        except Exception, e:
            print >> sys.stderr, "Coudn't save entry " + name + " to the database! ERROR: ", e
        conn.commit()
        curs.close()

    def updateInstalled(self, id, version):
        conn = sqlite3.connect('opkg.db')
        curs = conn.cursor()
        try:
            curs.execute('UPDATE installed SET version=? WHERE id=?', (version, id))
        except Exception, e:
            print >> sys.stderr, "Coudn't update entry " + str(id) + "! ERROR: ", e
        conn.commit()
        curs.close()

    def upgrade(self):
        conn = sqlite3.connect('opkg.db')
        curs = conn.cursor()
        try:
            curs.execute('SELECT * FROM installed')
        except Exception, e:
            print >> sys.stderr, "Coudn't select entry from the database! ERROR: ", e
        oldpackage = curs.fetchone()
        newpackage = self.getPackagesInfos(oldpackage[0])
        if str(oldpackage[2]) < str(newpackage[0]):
            self.upgradePackage(oldpackage[0], newpackage[0], newpackage[1])
        conn.commit()
        curs.close()

    def upgradePackage(self, id, version, packagelink):
            retvalue = call(['opkg', 'install', packagelink ])
            if retvalue == 0:
                self.updateInstalled(id, version)

    def getPackagesInfos(self, id):
        conn = sqlite3.connect('opkg.db')
        curs = conn.cursor()
        try:
            curs.execute('SELECT version, packagelink FROM packages WHERE id=' + str(id))
        except Exception, e:
            print >> sys.stderr, "Coudn't select entry from the database! ERROR: ", e
        return curs.fetchone()
