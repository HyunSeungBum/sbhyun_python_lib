#!/usr/local/python2.7/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import paramiko
import Queue
import threading
import time
import logging
from progressbar import *

userId = os.environ['USER']

HEADER = '\033[95m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
PURPLE = '\033[35m'
CYAN = '\033[36m'
LIGHTGRAY = '\033[37m'
BOLDRED = '\033[01;31m'
BOLDGREEN = '\033[01;32m'
BOLDBLUE = '\033[01;34m'
BOLDYELLOW = '\033[01;33m'
BOLDPURPLE = '\033[01;35m'
BOLDCYAN = '\033[01;36m'


class Transfer(threading.Thread):
    def __init__(self, queue, sourcefile, targetfile, session_timeout):
        threading.Thread.__init__(self)

        self.queue = queue
        self.sourcefile = sourcefile
        self.targetfile = targetfile
        self.session_timeout = session_timeout

    def run(self):
        while True:
            host = self.queue.get()
            result = BOLDGREEN + 'OK' + ENDC

            try:
                transport = paramiko.Transport((host, 22))
                transport.connect(username='userid', password='passwd')

                sftp = paramiko.SFTPClient.from_transport(transport)
                sftp.put(self.sourcefile, self.targetfile)

                sftp.close()
                transport.close()
                log.warning(host + ' - ' + self.targetfile)
            except Exception, e:
                log.error(host + ' - ' + str(e))
                result = RED + 'Failed' + ENDC

            global update
            update += 1
            result = host + '[ ' + result + ' ]'
            pbar.update_time(result, update)
            print pbar
            self.queue.task_done()


def logs():
    logdir = os.environ['HOME'] + '/logs/' + time.strftime("%Y") + '/' + time.strftime("%m%d")

    if os.path.exists(logdir) is False:
        os.makedirs(logdir, 0755)

    logger = logging.getLogger('')
    logger.setLevel(logging.WARNING)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(logdir + '/' + sys.argv[0] + '_' + time.strftime("%Y%m%d%H%M%S") + '.log')
    fh.setLevel(logging.WARNING)

    # create console handler with a higher log level
    ch = logging.FileHandler(logdir + '/' + sys.argv[0] + '_' + time.strftime("%Y%m%d%H%M%S") + '_error.log')
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-s', '--servers', dest='servers', metavar='N', type=str, nargs='+',
                        help='server command line list')
    parser.add_argument('-sf', '--serverfile', dest='serverfile', help='server list file')
    parser.add_argument('-of', '--sourcefile', dest='sourcefile', help='source file')
    parser.add_argument('-td', '--targetdir', dest='targetdir', help='target dir')
    parser.add_argument('-t', '--timeout', dest="timeout", type=int, help='session timeout')

    args = parser.parse_args()

    serverList = None
    if args.serverfile is not None:
        serverList = [x.strip() for x in open(args.serverfile)]

    if args.servers is not None:
        if serverList is not None:
            serverList.extend(args.servers)
        elif serverList is None:
            serverList = args.servers

    if serverList is None:
        print RED + "Error: Server List empty!" + ENDC
        sys.exit()

    serverList = list(set(serverList))

    if args.sourcefile is None:
        print RED + "Error: sourcefile empty!" + ENDC
        sys.exit()

    if args.targetdir is None:
        print RED + "Error: targetfile empty!" + ENDC
        sys.exit()

    sourcefile = args.sourcefile
    targetfile = args.targetdir

    if os.path.isfile(sourcefile) is False:
        print RED + "Error: sourcefile is not file!" + ENDC
        sys.exit()

    (dirname, filename) = os.path.split(sourcefile)

    if targetfile[-1:] == '/':
        targetfile = targetfile[:-1] + '/' + filename
    elif targetfile[-2:] == '/.':
        targetfile = targetfile[:-2] + '/' + filename
    else:
        targetfile += '/' + filename

    session_timeout = 30
    if args.timeout is not None:
        session_timeout = args.timeout

    log = logs()

    pbar = ProgressBar(len(serverList))
    pbar.fill_char = '='
    update = 0

    # start thread
    queue = Queue.Queue()
    for i in range(50):
        t = Transfer(queue, sourcefile, targetfile, session_timeout)
        t.setDaemon(True)
        t.start()

    for server in serverList:
        queue.put(server)

    queue.join()
