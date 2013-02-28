`quotapolicy` : Postfix SMTP access policy for Unix filesystem quotas
======================================================================

This program is a dæmon that makes Postfix reject emails if:
 - The recipient is an Unix user, and
 - Their filesystem quota is full.

The quota check is run right during the SMTP transaction, so that Postfix won't
have to run further processing, test for spam, call maildrop/procmail, etc. (It
will also prevent a misconfigured procmail from silently storing messages at
`/var/mail`.)  The sender receives a failure message.

The program uses Postfix access policy delegation; for more info, see
http://www.postfix.org/SMTPD_POLICY_README.html .

Requirements
============

 - Python 2.x
 - python-daemon (available via apt-get or pip)
 - quota (the binary)
 - sudo

Mini-guide
==========

If you want to customize installation, see the Makefile for options.

1. Create user `quotapolicy` however you like. For convenience, the Makefile
   includes a creation command with `adduser`, so you can just use

        make createuser

   if you want.  (It makes the same assumptions as `make install`, see below.)

2. Install the program:

        sudo make install

   This assumes you run a chrooted postfix on `/var/spool/postfix` .  If you
   chroot it elsewhere, you'll have to set it like this:

        sudo make postfix_chroot=/opt/postfix install

   If you don't use chroot (why?), you'll have to choose a directory in which
   to store the Unix socket:

        sudo make socketdir=/var/run/quotapolicy install
   
3. Setup the daemon to run at system startup, before postfix.  Startup scripts
   are provided for Debian, so you can just 

        sudo make install_debian
        # then edit /etc/default/quotapolicy if you want to change options

4. Add to `/etc/sudoers`:

        quotapolicy myhost=NOPASSWD: /usr/bin/quota

   Make sure it works without passwords:

        myuser$ sudo -u quotapolicy sudo /usr/bin/quota someuser

5. Add to Postfix `main.cf` (assuming chrooted postfix):
        smtpd_recipient_restrictions =
          check_policy_service unix:quotapolicy/quotapolicy.sock
          permit_mynetworks
          [other restrictions...]

6. Start the daemon and restart postfix

