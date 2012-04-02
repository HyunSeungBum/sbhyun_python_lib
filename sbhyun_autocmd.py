#!/usr/local/python2.7/bin/python
# -*- coding: utf-8 -*-

# To change this template, choose Tools | Templates
# and open the template in the editor.

# /usr/local/python2.7/bin/python autocmd.py -sf /home/orion/serverlist.txt -s 192.168.0.13 192.168.0.14
#   -c "uptime" -cf /home/orion/commandList.txt

import os
import sys
import argparse
import Queue
import threading
import pxssh
import logging
import time
from progressbar import *

__author__ = "orion"
__date__ = "$2011. 4. 7 오후 8:08:48$"

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


class AutoCmd(threading.Thread):

    def __init__(self, queue, commandList, session_timeout):
        threading.Thread.__init__(self)

        self.queue = queue
        self.commandList = commandList
        self.session_timeout = session_timeout

    def run(self):
        while True:
            host = self.queue.get()
            result = BOLDGREEN + 'OK' + ENDC
            try:
                flag = 1

                s = pxssh.pxssh()
                try:
                    s.login(host, 'userid', 'passwd', login_timeout=60)
                except pxssh.ExceptionPxssh, e:
                    flag = 0
                    s.close()
                    log.error(host + ' - ' + str(e))
                    result = RED + 'Failed' + ENDC

                if flag == 1:
                    for command in self.commandList:
                        s.sendline(command)
                        flag = s.prompt(self.session_timeout)
                        if flag is False:
                                log.error(host + ' - ' + command + "\n Time out")
                                s.terminate()
                                result = RED + 'TimeOut' + ENDC
                        print host + ' - ' + s.before
                        log.info(host + ' - ' + s.before)

                    s.logout()
            except Exception, e:
                log.error(host + ' - ' + str(e))
                result = RED + 'Failed' + ENDC

            global update
            update += 1
            result = host + ' [ ' + result + ' ]'
            pbar.update_time(result, update)
            print pbar
            self.queue.task_done()


def logs():
    logdir = os.environ['HOME'] + '/logs/' + time.strftime("%Y") + '/' + time.strftime("%m%d")

    if os.path.exists(logdir) is False:
        os.makedirs(logdir, 0755)

    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(logdir + '/' + sys.argv[0] + '_' + time.strftime("%Y%m%d%H%M%S") + '.log')
    fh.setLevel(logging.INFO)

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
    parser.add_argument('-cf', '--commandfile', dest='commandfile', help='command list file')
    parser.add_argument('-c', dest='command', help='exec command')
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

    commandList = None
    if args.commandfile is not None:
        commandList = [x.strip() for x in open(args.commandfile)]

    if args.command is not None:
        if commandList is not None:
            commandList.append(args.command)
        elif commandList is None:
            commandList = [args.command]

    if commandList is None:
        print RED + "Error: Command List empty!" + ENDC
        sys.exit()

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
        t = AutoCmd(queue, commandList, session_timeout)
        t.setDaemon(True)
        t.start()

    for server in serverList:
        queue.put(server)

    queue.join()
