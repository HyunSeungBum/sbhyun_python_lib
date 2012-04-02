#!/usr/local/python2.7/bin/python
# -*- coding: UTF-8 -*-

''' PostGreSQL Database Object '''

import os

try:
        import pgdb
except ImportError, e:
        raise ImportError("%s" % e)

try:
        from sbhyun_utils import log
        from DbCfgParser import dbCfgParser
        from DbInterface import DbInterface
except ImportError, e:
        raise ImportError("%s" % e)


class dbPgsql(dbCfgParser, log) implements DbInterface:

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

                cString = "%s:%s:%s:%s" % (host, dbName, userId, passwd)
                connectString = cstring.replace('\\', '')
                try:
                        self._db = pgdb.connect(connectString)
                except Exception, e:
                        raise self.log.error('%s', str(e))

                self._cursor = self._db.cursor()

        def dbClose(self):
                self._cursor.close()
                self._db.close()

        def query(self, sql):
                try:
                        self._cursor.execute(sql)
                except Exception, e:
                        self.log.error('%s, query: %s' % (str(e), sql))

        def dbInsert(self, sql):
                self.query(sql)
                return self._cursor.rowcount

        def dbDelete(self, sql):
                self.query(sql)
                return self._cursor.rowcount

        def dbSelect(self, sql):
                self.query(sql)
                try:
                        result = self._cursor.fetchone()
                        return result
                except Exception, e:
                        self.log.error("%s, query: %s" % (str(e), sql))

        def dbList(self, sql):
                self.query(sql)
                try:
                        result = self._cursor.fetchall()
                        return result
                except Exception, e:
                        self.log.error("%s, query: %s" % (str(e), sql))
