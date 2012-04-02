#!/usr/local/python2.7/bin/python
# -*- coding: UTF-8 -*-

''' Sample Threaded XmlRPC Server
       Feature:
       1. Ip AccessList
'''

__author__ = "Seung-Bum Hyun <orion203@gmail.com>"
__date__ = "30 March 2012"
__version__ = "0.1"
__License__ = "GPL"

import SocketServer
from DocXMLRPCServer import DocXMLRPCServer, DocXMLRPCRequestHandler

accessList = (
        '123.140.249.179',
        '127.0.0.1'
        )


class TestObject:
        def pow(self, x, y):
                return pow(x, y)

        def add(self, x, y):
                return x + y

        def divide(self, x, y):
                return float(x) / float(y)


class AsyncXMLRPCServer(SocketServer.ThreadingMixIn, DocXMLRPCServer):
        def verify_request(self, request, client_address):
                if client_address[0] in accessList:
                        return 1
                else:
                        return 0

from daemonize import startstop

if __name__ == '__main__':
        # daemonize
        startstop(stdout='/tmp/deamonize.log',
                pidfile='/tmp/deamonize.pid')

        server = AsyncXMLRPCServer(('', 8000), DocXMLRPCRequestHandler)
        server.register_instance(TestObject())
        server.serve_forever()
	