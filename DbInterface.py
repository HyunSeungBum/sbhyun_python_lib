#!/usr/local/python2.7/bin/python
# -*- coding: UTF-8 -*-

''' Database Interface '''

__author__ = "Seung-Bum Hyun <orion203@gmail.com>"
__date__ = "27 March 2012"
__version__ = "0.1"
__License__ = "GPL"

interface DbInterface:
        ''' Database Interface '''

        def dbConnect():
                ''' db connect method '''

        def dbClose():
                ''' db close method '''

        def query():
                ''' sql query execute method '''

        def dbInsert():
                ''' insert query execute method '''

        def dbUpdate():
                ''' update query execute method '''

        def dbDelete():
                ''' delete query execute method '''

        def dbSelect():
                ''' select query execute method '''

        def dbList():
                ''' return list '''
