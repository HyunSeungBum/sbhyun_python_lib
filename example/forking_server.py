#!/usr/local/python2.7/bin/python
# -*- coding: UTF-8 -*-

''' Sample Forking TCPServer
       Feature:
       1. Ip AccessList
'''

__author__ = "Seung-Bum Hyun <orion203@gmail.com>"
__date__ = "30 March 2012"
__version__ = "0.1"
__License__ = "GPL"

import os
import time
import socket
from SocketServer import ForkingMixIn, ForkingTCPServer, StreamRequestHandler, TCPServer

accessList = (
        '123.140.249.179',
        '127.0.0.1'
        )


class ForkingTCPRequestHandler(StreamRequestHandler):

        client_addr = ''
        client_port = ''

        def handle(self):
                # self.rfile is a file-like object created by the handler;
                # we can now use e.g. readline() instead of raw recv() calls
                self.data = self.rfile.readline().strip()
                print "{} wrote:".format(self.client_address[0])
                print self.data
                # Likewise, self.wfile is a file-like object used to write back
                # to the client

                # asign client info
                client_addr, client_port = self.client_address

                self.wfile.write(self.data.upper())


class AsyncFrokingTCPServer(ForkingMixIn, TCPServer):
        def verify_request(self, request, client_address):
                if client_address[0] in accessList:
                        return 1
                else:
                        return 0


if __name__ == '__main__':
        HOST, PORT = socket.gethostbyname(socket.gethostname()), 31000
        server = AsyncFrokingTCPServer((HOST, PORT), ForkingTCPRequestHandler)
        server.allow_reuse_address = 1
        server.timeout = 60
        server.serve_forever()
