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
import Config
import OPKGXml
import OPKGParser
import OPKGUpgrade
import OPKGDelete

class OPKG:
    def __init__(self):
        self._opkgxml = OPKGXml.OPKGXml()
        self._opkgupgrade = OPKGUpgrade.OPKGUpgrade()
        self._opkgdelete = OPKGDelete.OPKGDelete()
        self._color = True
        self._nocolor = not self._color
        self._save = True
        self._nosave = not self._save
        self._installstr = ""
        self._installnames = ""
        self._removenames = ""
        self._dbentry = []
        self._rmentry = []
        config = Config.Config()
        self._dbfile = config.getDbfile()
        self._pkgtable = config.getPkgtable()

    def install(self, id, name, version, packagelink):
        self._installstr += packagelink + " "
        self._installnames += name + " "
        self._dbentry.append(  (id, name, version) )

    def remove(self, id, name):
        self._removenames += name + " "
        self._rmentry.append(id)

    def startInstallation(self):
        if self._installstr != "":
            print self._installnames
            answer = 'N'
            print 'Do you want to install the package(s) above (y/N): ',
            answer = sys.stdin.read(1)
            if answer == 'y' or answer == 'Y':
                retvalue = call(['opkg', 'install', self._installstr ])
                if retvalue == 0:
                    for (id, name, version) in self._dbentry:
                        self._opkgupgrade.setInstalled(id, name, version)
                    print '\033[1;32mInstalled successfully\033[0m'
                else:
                    print '\033[1;31mInstalled failed\033[0m'
            else:
                print "Aborted!"
        else:
            print "No package found to install!"

    def startRemove(self):
        if self._removenames != "":
            print self._removenames
            answer = 'N'
            print 'Do you want to remove the package(s) above (y/N): ',
            answer = sys.stdin.read(1)
            if answer == 'y' or answer == 'Y':
                retvalue = call(['opkg', 'remove', self._removenames])
                # Deinstallation is finished successfully!
                if retvalue == 0:
                    for id in self._rmentry:
                        self._opkgdelete.deletePackage(id)
                    print '\033[1;32mDeinstallation successfully\033[0m'
                else:
                    print '\033[1;31mDeinstallation failed\033[0m'
            else:
                print "Aborted!"
        else:
            print "No package found to remove!"

    def getPackageByNumber(self, number, install, remove):
        conn = sqlite3.connect(self._dbfile)
        conn.text_factory = str
        curs = conn.cursor()
        curs.execute('SELECT id, name, homepage, developer, dependency, source,\
                description_short, packagelink, category, version FROM  ' + \
                self._pkgtable + ' WHERE id=' + str(number))
        for row in curs.fetchall():
            if install:
                self.install(row[0], row[1], row[9], row[7])
            elif remove:
                self.remove(row[0], row[1])
            else: self.printPackage(self._color, row)
        conn.commit()
        curs.close()
        if install: self.startInstallation()
        elif remove: self.startRemove()

    def getPackageBySearchterm(self, searchterm, install, remove):
        conn = sqlite3.connect(self._dbfile)
        conn.text_factory = str
        curs = conn.cursor()
        curs.execute('SELECT id, name, homepage, developer, dependency, source,\
                description_short, packagelink, category, version FROM '\
                 + self._pkgtable + ' WHERE name LIKE "%' + searchterm + '%" OR \
                description_short LIKE "%' + searchterm + '%"')
        for row in curs.fetchall():
            if install:
                self.install(row[0], row[1], row[9], row[7])
            elif remove:
                self.remove(row[0], row[1])
            else: self.printPackage(self._color, row)
        conn.commit()
        curs.close()
        if install: self.startInstallation()
        elif remove: self.startRemove()

    def getAllPackages(self):
        conn = sqlite3.connect(self._dbfile)
        conn.text_factory = str
        curs = conn.cursor()
        curs.execute('SELECT id, name, homepage, developer, dependency, source,\
                description_short, packagelink, category, version FROM '\
                + self._pkgtable)
        for row in curs.fetchall():
            self.printPackageShort(self._color, row)
        conn.commit()
        curs.close()

    def printPackage(self, color, entry):
        if color:
            RESET = "\033[0m"
            GREEN = "\033[1;32m"
            BLUE = "\033[1;34m"
            CYAN = "\033[1;36m"
            BOLD = "\033[1m"
        else:
            RESET = ""
            GREEN = ""
            BLUE = ""
            CYAN = ""
            BOLD = ""
        print GREEN + '*********** [' + str(entry[0]) + '] ' + entry[1] + ' ***********  ' + RESET
        if entry[2] != "unknown":
            print BOLD + 'homepage   : ' + RESET + CYAN + entry[2] + RESET
        if entry[3] != "unknown":
            print BOLD + 'developer  : ' + RESET + entry[3]
        if entry[4] != "unknown":
            print BOLD + 'dependency : ' + RESET + entry[4]
        if entry[5] != "unknown":
            print BOLD + 'source     : ' + RESET + CYAN + entry[5] + RESET
        if entry[6] != "unknown":
            print BOLD + 'description: ' + RESET + entry[6]
        if entry[7] != "unknown":
            print BOLD + 'packagelink: ' + RESET + CYAN + entry[7]  + RESET
        if entry[8] != "unknown":
            print BOLD + 'category   : ' + RESET+ entry[8]
        if entry[9] != "unknown":
            print BOLD + 'version    : ' + RESET + entry[9]

    def printPackageShort(self, color, entry):
        if self._color:
            RESET = "\033[0m"
            GREEN = "\033[1;32m"
        else:
            RESET = ""
            GREEN = ""
        print '[' + str(entry[0]) + ']',
        print GREEN + entry[1] + RESET

    def savePackages(self):
        data = self._opkgxml.getXMLAll()
        _opkgparser = OPKGParser.OPKGParser(None, self._save)
        _opkgparser.feed(data)
        _opkgparser.close()

