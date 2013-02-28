#!/usr/bin/env python

import socket
import SocketServer
import sys
import pwd
import subprocess
import os

# make sure script user can run this under sudo, no password
quotapath = '/usr/bin/quota'

# make sure the directory exists, and script user has rwx permissions.
sockpath = '/var/spool/postfix/quotapolicy/quotapolicy.sock'

# set this to the value of recipient_delimiter from postfix
recip_del = '-'

# debug = False
debug = True


devnull = open(os.devnull, 'w')
def overquota(user):
    try:
        pwd.getpwnam(user)
    except KeyError:
        # quota doesn't apply
        return False

    try:
        subprocess.check_call(['sudo', quotapath, user], stdout=devnull)
        return False
    except subprocess.CalledProcessError as e:
        return e.returncode


class QuotaSocketHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        recipient = None
        action = 'OK'

        while True:
            line = self.rfile.readline().strip()
            if line == '':
                break

            a = line.split('=')
            key = a[0]
            val = '='.join(a[1:])

            if key == 'recipient':
                recipient = val
                break

        if recipient:
            user = recipient.split('@')[0].split(recip_del)[0]
            ov = overquota(user)
            if ov:
                action = 'DEFER_IF_PERMIT Quota exceeded: ' \
                        + user \
                        + '(' + str(ov) + ')'

        if debug: print(str(recipient) + ': sending ' + action)
        self.wfile.write('action=' + action + "\n")
        self.wfile.write("\n")


class ForkingUnixStreamServer(
        SocketServer.UnixStreamServer,
        SocketServer.ForkingMixIn
        ):
    pass

try:
    os.unlink(sockpath)
except OSError:
    if os.path.exists(sockpath):
        raise

server = SocketServer.UnixStreamServer(sockpath, QuotaSocketHandler)
os.chmod(sockpath, 0666)
try:
    server.serve_forever()
finally:
    os.unlink(sockpath)
