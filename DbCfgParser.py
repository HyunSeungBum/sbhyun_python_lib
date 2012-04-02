#!/usr/local/python2.7/bin/python
# -*- coding: UTF-8 -*-

''' Db cfg Parser '''

__author__ = "Seung-Bum Hyun <orion203@gmail.com>"
__date__ = "27 March 2012"
__version__ = "0.1"
__License__ = "GPL"

from ConfigParser import ConfigParser


class dbCfgParser:
        _cfgFile = '/home/orion/dbinfo.cfg'
        _cfg = ''
        _config = {}

        def setParam(self, host=None):
                if host is None:
                        return
                else:
                        self.host = host

                self._cfg = ConfigParser()
                self._cfg.read(self._cfgFile)
                self.parseCfg()

        def parseCfg(self):
                self._config['Host'] = self._cfg.get(self.host, 'Host')
                self._config['User'] = self._cfg.get(self.host, 'User')
                self._config['Password'] = self._cfg.get(self.host, 'Password')
                self._config['DefaultDB'] = self._cfg.get(self.host, 'DefaultDB')
                self._config['Type'] = self._cfg.get(self.host, 'Type')

        def getConfig(self):
                return self._config

if __name__ == '__main__':
        a = dbCfgParser()
        a.setParam('localhost')
        print a.getConfig()
