#!/usr/bin/env python

import socket
import sys

sockpath = '/var/spool/postfix/quotapolicy/quotapolicy.sock'

recipient = sys.argv[1]

msg='''request=smtpd_access_policy
protocol_state=RCPT
protocol_name=SMTP
helo_name=some.domain.tld
queue_id=8045F2AB23
sender=foo@bar.tld
recipient=%s
recipient_count=0
client_address=1.2.3.4
client_name=another.domain.tld
reverse_client_name=another.domain.tld
instance=123.456.7
sasl_method=plain
sasl_username=you
sasl_sender=
size=12345
ccert_subject=solaris9.porcupine.org
ccert_issuer=Wietse+20Venema
ccert_fingerprint=C2:9D:F4:87:71:73:73:D9:18:E7:C2:F3:C1:DA:6E:04
encryption_protocol=TLSv1/SSLv3
encryption_cipher=DHE-RSA-AES256-SHA
encryption_keysize=256
etrn_domain=
stress=
ccert_pubkey_fingerprint=68:B3:29:DA:98:93:E3:40:99:C7:D8:AD:5C:B9:C9:40
''' # empty line

msg = msg % recipient

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(sockpath)
s.sendall(msg)

try:
    f = s.makefile()
    answer = f.read()
finally:
    s.close()
print("Answer:")
sys.stdout.write(answer)

