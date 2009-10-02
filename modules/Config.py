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
import ConfigParser

class Config:
    def __init__(self):
        self.cfgparser = ConfigParser.SafeConfigParser()
        self.cfgparser.read('opkg.cfg')

    def getDbfile(self):
        return self.cfgparser.get('persistent', 'dbfile')

    def getPkgtable(self):
        return self.cfgparser.get('persistent', 'pkgtable')

    def getInstalltable(self):
        return self.cfgparser.get('persistent', 'installtable')

    def getHost(self):
        return self.cfgparser.get('opkg.org', 'host')

    def getPort(self):
        return self.cfgparser.getint('opkg.org', 'port')

    def getVersion(self):
        return self.cfgparser.get('core', 'version')

    def getAuthor(self):
        return self.cfgparser.get('core', 'author')


