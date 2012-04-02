#!/usr/local/python2.7/bin/python
# -*- coding: UTF-8 -*-

''' MySQL Database Object '''

__author__ = "Seung-Bum Hyun <orion203@gmail.com>"
__date__ = "2 April 2012"
__version__ = "1.0"
__License__ = "GPL"

import os
import sys

try:
        import MySQLdb
except ImportError, e:
        raise ImportError("%s" % e)

try:
        sys.path.append(os.getcwd())
        from sbhyun_utils import logs
        from DbCfgParser import dbCfgParser
except ImportError, e:
        raise ImportError("%s" % e)


class dbMysql(dbCfgParser):

        def __init__(self, host=None):
                self._log = logs()

                if host is not None:
                        self.setParam(host)
                        self._serverCfg = self.getConfig()
                        self.dbConnect()

        def dbConnect(self, host=None, dbName=None, userId=None, passwd=None):
                if host is None:
                        host = self._serverCfg['Host']

                if dbName is None:
                        dbName = self._serverCfg['DefaultDB']

                if userId is None:
                        userId = self._serverCfg['User']

                if passwd is None:
                        passwd = self._serverCfg['Password']

                try:
                        self._db = MySQLdb.connect(host=host, user=userId, passwd=passwd, db=dbName)
                except Exception, e:
                        raise self._log.error('%s' % str(e))

                self._cursor = self._db.cursor()
                self._DictCursor = MySQLdb.cursors.DictCursor(self._db)

        def dbClose(self):
                self._cursor.close()
                self._DictCursor.close()
                self._db.close()

        def query(self, sql):
                try:
                        sql = str(MySQLdb.escape_string(sql))
                        self._cursor.execute(sql)
                except Exception, e:
                        self._log.error('%s, query: ' % (str(e), sql))

        def dbInsert(self, sql):
                self.query(sql)
                return self._cursor.lastrowid

        def dbUpdate(self, sql):
                self.query(sql)
                return self._cursor.rowcount

        def dbDelete(self, sql):
                self.query(sql)
                return self._cursor.rowcount

        def dbSelect(self, sql):
                self._DictCursor.execute(sql)
                result = self._DictCursor.fetchone()
                return result

        def dbList(self, sql):
                self._DictCursor.execute(sql)
                result = self._DictCursor.fetchall()
                return result

if __name__ == '__main__':
        ob = dbMysql('localhost')
        ob.query('use mysql')
        sql = 'SELECT * FROM user'
        results = ob.dbList(sql)
        for result in results:
                print result
        sql = 'SELECT * FROM user LIMIT 1'
        result = ob.dbSelect(sql)
        print result
        ob.dbClose()
