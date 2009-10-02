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
import sqlite3
import Config

class OPKGDelete:
    def __init__(self):
        config = Config.Config()
        self._dbfile = config.getDbfile()
        self._installtable = config.getInstalltable()

    def deletePackage(self, id):
        conn = sqlite3.connect(self._dbfile)
        curs = conn.cursor()
        curs.execute('DELETE FROM ' + self._installtable + ' WHERE id=' + str(id))
        conn.commit()
        curs.close()

