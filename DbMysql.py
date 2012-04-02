#!/usr/local/python2.7/bin/python
# -*- coding: UTF-8 -*-

''' MySQL Database Object '''

import os

try:
        import MySQLdb
except ImportError, e:
        raise ImportError("%s" % e)

try:
        from sbhyun_utils import log
        from DbCfgParser import dbCfgParser
        from DbInterface import DbInterface
except ImportError, e:
        raise ImportError("%s" % e)


class dbMysql(dbCfgParser, log) implements DbInterface:

        def __init__(self, host):
                self.log = log()

                self.setParam(host)
                self._serverCfg = self.getConfig()

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
                        raise self.log.error('%s' % str(e))

                self._cursor = self._db.cursor()
                self._DictCursor = MySQLdb.cursors.DictCursor(self._db)

        def dbClose(self):
                self._cursor.close()
                self._DictCursor.close()
                self._db.close()

        def query(self, sql):
                try:
                        self._cursor.execute(sql)
                except Exception, e:
                        self.log.error('%s, query: ' % (str(e), sql))

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

