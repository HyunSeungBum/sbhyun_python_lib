#!/usr/local/python2.7/bin/python
# -*- coding: UTF-8 -*-

SIGTERM_SENT = False


def sigterm_handler(signum, frame):
        print >>sys.stderr, "SIGTERM handler.  Shutting Down."

        global SIGTERM_SENT
        if not SIGTERM_SENT:
                SIGTERM_SENT = True
                print >>sys.stderr, "Sending TERM to PG"
                os.killpg(0, signal.SIGTERM)

        sys.exit()


def main():
        # set session ID to this process so we can kill group in sigterm handler
        os.setsid()
        signal.signal(signal.SIGTERM, sigterm_handler)

        while 1:
                print >> sys.stdout, "Hyun Seung Bum"
                sleep(2)

from daemonize import startstop

if __name__ == "__main__":
        startstop(stdout="/tmp/example.log",
                pidfile="/tmp/example.pid")
        main()
