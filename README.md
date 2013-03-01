Quotapolicy: Postfix SMTP access policy for Unix filesystem quotas
==================================================================

This program is a policy dæmon to make Postfix reject emails if:
 - The recipient is an Unix user, and
 - Their filesystem quota is full.

The quota check is run right during the SMTP transaction, so that Postfix won't
have to run further processing, test for spam, call maildrop/procmail, etc. (It
will also prevent a misconfigured procmail from silently storing messages at
`/var/mail` or elsewhere.)  The sender receives a failure message.

The program uses Postfix access policy delegation; for more info, see
http://www.postfix.org/SMTPD_POLICY_README.html .

Requirements
============

 - Python 2.x
 - If your python is < 2.7: python-argparse (available via apt-get or pip)
 - python-daemon (available via apt-get or pip)
 - quota (the binary)
 - sudo

Installation
============

I recommend this dæmon to be run under its own user, for security reasons.
Quotapolicy must create a socket file, and a pid file; it creates both of them
in a directory we’ll call its homedir.

 - If your postfix is chrooted, the quotapolicy homedir must be inside the
   chroot.  If the chroot is at `/var/spool/postfix` , then
   `/var/spool/postfix/quotapolicy` is as good as any.

 - If you don't chroot postfix, then the standards-compliant place would be
   `/var/run/quotapolicy` .

The quotapolicy user needs the following privileges:

 - Read/write/execute permissions on the homedir.

 - Ability to run `sudo /usr/bin/quota` without a password (you can customize
   the path to quota(1)).

Once you have decided on a homedir, proceed with the installation.  The default
homedir is `/var/spool/postfix/quotapolicy`.

1. Get the sources:

        $ git clone git://github.com/leoboiko/quotapolicy.git
        $ cd quotapolicy

2. Create user `quotapolicy` however you like. For convenience, the Makefile
   includes a creation command with `adduser`, so if you want, you can just use

        $ sudo make createuser

   If your homedir isn't the default, call it like

        $ sudo make homedir=/some/other/dir createuser

3. Install the program:

        $ sudo make install

   Again, use `make homedir=` if your homedir isn't the default.
   
4. Setup the dæmon to run at system startup, before Postfix.  Startup scripts
   are provided for Debian (`/etc/init.d/quotapolicy`), so you can just 

        $ sudo make install_debian
        # then edit /etc/default/quotapolicy if you want to change options

   See `quotapolicy --help` for options.

5. Add to `/etc/sudoers` (using visudo(8)):

        $ quotapolicy myhost=NOPASSWD: /usr/bin/quota

   Make sure it works without passwords:

        myuser$ sudo -u quotapolicy sudo /usr/bin/quota someuser

6. Add the quotapolicy socket to your `smtpd_recipient_restrictions` in Postfix
   `main.cf`.  Chrooted postfix example:

        smtpd_recipient_restrictions =
          check_policy_service unix:quotapolicy/quotapolicy.socket
          permit_mynetworks
          [other restrictions...]

   Non-chrooted example:

        smtpd_recipient_restrictions =
          check_policy_service unix:/var/run/quotapolicy/quotapolicy.socket
          permit_mynetworks
          [other restrictions...]

7. Start the dæmon and restart postfix.

Bugs, suggestions, comments
===========================

 - http://github.com/leoboiko/quotapolicy
 - leoboiko@namakajiri.net

