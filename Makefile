SHELL = /bin/sh

prefix = /usr/local
exec_prefix = $(prefix)
bindir = $(exec_prefix)/bin
srcdir = .

debian_initdir = /etc/init.d
debian_defaultdir = /etc/default

homedir = /var/spool/postfix/quotapolicy

user = quotapolicy

createuser:
	@if ! getent passwd $(user) >/dev/null; then \
	  adduser --system --home $(homedir) \
		  --gecos 'Postfix quota access policy daemon' \
		  $(user) ; \
	fi

install:
	@if ! getent passwd $(user) >/dev/null; then \
	  echo "'getent passwd $(user)' failed." ;\
	  echo "Please create the user $(user), or run 'make createuser'." ;\
	else \
	  install -m 0755 -v $(srcdir)/bin/quotapolicy $(bindir)/ ;\
	  mkdir -v -p $(homedir) ;\
	  chown -v $(user):  $(homedir) ;\
	fi

install_debian: install
	@install -v -m 0755 $(srcdir)/debian/init.d/quotapolicy \
		$(debian_initdir)/quotapolicy
	@install -v -m 0644 $(srcdir)/debian/default/quotapolicy \
		$(debian_defaultdir)/quotapolicy
	update-rc.d quotapolicy defaults

.PHONY: createuser install install_debian

