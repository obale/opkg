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
import socket

class OPKGXml:
    def __init__(self):
        pass

    def getXMLByNumber(self, number):
        command = 'POST /api.php?action=show-package&pid=' + str(number) + ' HTTP/1.1\r\n'
        return self.getXML(command)

    def getXMLBySearchterm(self, searchterm):
        command = 'POST /api.php?action=search-package&q=' + searchterm + ' HTTP/1.1\r\n'
        return self.getXML(command)

    def getXMLAll(self):
        command = 'POST /api.php?action=list-all-packages HTTP/1.1\r\n'
        return self.getXML(command)

    def getXML(self, postcommand):
        self._soc = socket.socket()
        self._soc.connect( ('opkg.org', 80) )
        self._soc.send(postcommand)
        self._soc.send('Host: www.opkg.org\r\n\n')

        data = " "
        buffer = ""
        while data:
            data = self._soc.recv(1024)
            buffer += data
        self._soc.close()
        return self.parseAnswer(buffer)

    def parseAnswer(self, buffer):
        xmldata = buffer.split('<?xml version="1.0"?>')
        header = '<?xml version="1.0" encoding="latin1"?>'
        xmldata = header + xmldata[1]
        xmldata = xmldata.split('\r\n0\r\n\r\n')[0]
        return xmldata

