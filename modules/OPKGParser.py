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
from xml.parsers import expat
import Config

class OPKGParser:
    def __init__(self, short, save):
        self._type = None
        self._package = False
        self._parser = expat.ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._save = save
        config = Config.Config()
        self._dbfile = config.getDbfile()
        self._pkgtable = config.getPkgtable()

        self._entry = self.getEmptyEntry()

        if self._save:
            self.createEmptyDatabase()
        self._parser.CharacterDataHandler = self.saveData

    def getEmptyEntry(self):
        return { 'id':None, 'name':None, 'homepage':None, \
                'developer':None, 'dependency':[], 'source': None,\
                'description':None, 'packagelink':None, 'category':None,\
                'version':None }

    def feed(self, data):
        self._parser.Parse(data, 0)

    def close(self):
        self._parser.Parse("", 1)
        del self._parser

    def start(self, tag, attrs):
        if ( tag == 'package' ):
            self._package = True
        self._type = tag

    def end(self, tag):
        if ( tag == self._type ):
            self._type = None
        if ( tag == 'package' ):
            self._package = False
            if self._save:
                self.saveEntry(self._entry)
                del self._entry
                self._entry = self.getEmptyEntry()

    def saveData(self, data):
        if self._package:
            if self._type == 'id':
                self._entry['id'] = data
            elif self._type == 'name':
                self._entry['name'] = data
            elif self._type == 'homepage':
                self._entry['homepage'] = data
            elif self._type == 'developer':
                self._entry['developer'] = data
            elif self._type == 'dependency':
                self._entry['dependency'].append(data)
            elif self._type == 'source':
                self._entry['source'] = data
            elif self._type == 'description_short':
                self._entry['description_short'] = data
            elif self._type == 'packagelink':
                self._entry['packagelink'] = data
            elif self._type == 'category':
                self._entry['category'] = data
            elif self._type == 'version':
                self._entry['version'] = data

    def getEntry(self):
        return self._entry

    def saveEntry(self, entry):
        conn = sqlite3.connect(self._dbfile)
        conn.text_factory = str
        curs = conn.cursor()
        query = 'INSERT INTO ' + self._pkgtable + ' VALUES ( '
        query += entry['id'] + ', '
        query += '"' + entry['name'] + '", '
        if entry['homepage'] is not None:
            query += '"' + str(entry['homepage']) + '", '
        else:
            query += '"unknown", '
        if entry['developer'] is not None:
            query += '"' + entry['developer'] + '", '
        else:
            query += '"unknown", '
        dependency = ''
        for line in entry['dependency']:
            dependency += line + ' '
        if dependency != '':
            query += '"' + str(dependency) + '", '
        else:
            query +='"unknown", '
        if entry['source'] is not None:
            query += '"' + str(entry['source']) + '", '
        else:
            query += '"unknown", '
        if entry['description_short'] is not None:
            query += '"' + entry['description_short'] + '", '
        else:
            query += '"unknown", '
        if entry['packagelink'] is not None:
            query += '"' + str(entry['packagelink']) + '", '
        else:
            query +='"unknown", '
        if entry['category'] is not None:
            query += '"' + str(entry['category']) + '", '
        else:
            query +='"unknown", '
        if entry['version'] is not None:
            query += '"' + str(entry['version']) + '"'
        else:
            query +='"unknown", '
        query += ')'
        try:
            curs.execute(query)
        except sqlite3.OperationalError, e:
            print >> sys.stderr, "Coudn't save entry " + entry['name'] + " to the database! ERROR: ", e
        conn.commit()
        curs.close()

    def createEmptyDatabase(self):
        conn = sqlite3.connect(self._dbfile)
        curs = conn.cursor()
        try:
            curs.execute('DROP TABLE ' + self._pkgtable)
        except sqlite3.OperationalError:
            pass
        curs.execute('CREATE TABLE ' + self._pkgtable + ' (id INTEGER, name VARCHAR, homepage VARCHAR, \
developer VARCHAR, dependency VARCHAR, source VARCHAR, description_short VARCHAR, \
packagelink VARCHAR, category VARCHAR, version VARCHAR)')
        conn.commit()
        curs.close()

