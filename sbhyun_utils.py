#!/usr/local/python2.7/bin/python
# -*- coding: UTF-8 -*-

''' Useful function packages '''

__author__ = "Seung-Bum Hyun <orion203@gmail.com>"
__date__ = "27 March 2012"
__version__ = "0.1"
__License__ = "GPL"

import os
import time
import sys

import socket
import fcntl
import struct

import locale
import logging


def GetIpAddress(ifname):
        '''get the IP address associated with a network interface (linux only)
       http://code.activestate.com/recipes/439094'''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15])
        )[20:24])


def GetHwAddress(ifname):
        '''get the Network Mac Address associated with a network interface (linux only)
        http://code.activestate.com/recipes/439094'''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
        return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]


def GetHostname():
        '''get hostname '''
        return os.uname()[1]


''' GetHumanReadableSize lambda function '''
GetHumanReadableSize = lambda s: [(s % 1024 ** i and "%.1f" % (s / 1024.0 ** i) or str(s / 1024 ** i)) + x.strip()
        for i, x in enumerate(' KMGTPEZY') if s < 1024 ** (i + 1) or i == 8][0]


def human_num(num, divisor=1, power=""):
        """Convert a number for human consumption
        http://www.pixelbeat.org/scripts/human.py"""

        locale.setlocale(locale.LC_ALL, '')
        num = float(num)
        if divisor == 1:
                return locale.format("%ld", int(num), 1)
        elif divisor == 1000:
                powers = [" ", "K", "M", "G", "T", "P"]
        elif divisor == 1024:
                powers = ["  ", "Ki", "Mi", "Gi", "Ti", "Pi"]
        else:
                raise ValueError("Invalid divisor")

        if not power:
                power = powers[0]
        while num >= 1000:  # 4 digits
                num /= divisor
                power = powers[powers.index(power) + 1]
                human_num(num, divisor, power)
        if power.strip():
                return "%6.1f%s" % (num, power)
        else:
                return "%4ld  %s" % (num, power)


def GetLoadAverage():
        """get LoadAverage """
        load = 'load average: %.2f %.2f %.2f' % os.getloadavg()
        return load


def logs(logdir=None):
        """ Cumtomizing logging """
        if logdir is None:
                logdir = os.environ['HOME'] + '/logs/' + time.strftime("%Y") + '/' + time.strftime("%m%d")

        if os.path.exists(logdir) is False:
                os.makedirs(logdir, 0755)

        logger = logging.getLogger('')
        logger.setLevel(logging.DEBUG)

        filename = os.path.basename(sys.argv[0])

        # create file handler which logs even debug messages
        fh = logging.FileHandler(logdir + '/' + filename + '_' + time.strftime("%Y%m%d%H%M%S") + '.log')
        fh.setLevel(logging.INFO)

        # create console handler with a higher log level
        ch = logging.FileHandler(logdir + '/' + filename + '_' + time.strftime("%Y%m%d%H%M%S") + '_error.log')
        ch.setLevel(logging.ERROR)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # add the handlers to logger
        logger.addHandler(ch)
        logger.addHandler(fh)

        return logger

""" require python 2.7 above"""
from collections import namedtuple


def DiskPartitions(all=False):
        """Return all mountd partitions as a nameduple.
        If all == False return phyisical partitions only."""

        phydevs = []
        disk_ntuple = namedtuple('partition', 'device mountpoint fstype')

        f = open("/proc/filesystems", "r")
        for line in f:
                if not line.startswith("nodev"):
                        phydevs.append(line.strip())

        retlist = []
        f = open('/etc/mtab', "r")
        for line in f:
                if not all and line.startswith('none'):
                        continue
                fields = line.split()
                device = fields[0]
                mountpoint = fields[1]
                fstype = fields[2]
                if not all and fstype not in phydevs:
                        continue
                if device == 'none':
                        device = ''
                ntuple = disk_ntuple(device, mountpoint, fstype)
                retlist.append(ntuple)

        return retlist


def DiskUsage(path):
        """Return disk usage associated with path."""

        usage_ntuple = namedtuple('usage', 'total used free percent')
        st = os.statvfs(path)
        free = (st.f_bavail * st.f_frsize)
        total = (st.f_blocks * st.f_frsize)
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        try:
                percent = ret = (float(used) / total) * 100
        except ZeroDivisionError:
                percent = 0

        # NB: the percentage is -5% than what shown by df due to
        # reserved blocks that we are currently not considering:
        # http://goo.gl/sWGbH

        return usage_ntuple(total, used, free, round(percent, 1))


if __name__ == '__main__':
        # get Ip, Mac Address for Network Interface Card
        print GetIpAddress('eth0')
        print GetHwAddress('eth0')

        for part in DiskPartitions():
                print part
                print "    %s\n" % str(DiskUsage(part.mountpoint))

        print GetHumanReadableSize(273675342365) + 'iB'

        print GetLoadAverage()

        print human_num(378682763, 1024) + 'B'

        log = logs()
        log.error('Error: asd')
        log.info('INFO: ad')
