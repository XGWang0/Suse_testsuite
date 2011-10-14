# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************

## Process this file with automake to produce Makefile.in -*-Makefile-*-.

# Sort in traditional ASCII order, regardless of the current locale;
# otherwise we may get into trouble with distinct strings that the
# current locale considers to be equal.
ASSORT = LC_ALL=C sort

all_programs = (cd ../src && MAKEFLAGS= $(MAKE) -s all_programs.list)

TESTS = help-version
TESTS_ENVIRONMENT = \
  all_programs="`$(all_programs)`" \
  PACKAGE_BUGREPORT=$(PACKAGE_BUGREPORT) \
  PATH="`pwd`/../src$(PATH_SEPARATOR)$$PATH"

EXTRA_DIST = \
  $(TESTS) .env-warn Coreutils.pm Makefile.am.in README envvar-check \
  expensive group-names input-tty lang-default mk-script priv-check \
  rwx-to-mode sample-test setgid-check umask-check

SUBDIRS = \
  basename chgrp chmod chown cp cut dd dircolors du expr factor \
  fmt head install join ln ls ls-2 md5sum misc mkdir mv od pr readlink \
  rm rmdir seq sha1sum shred sort stty sum tac tail tail-2 tee test \
  touch tr tsort unexpand uniq wc

.PHONY: check-root
check-root:
	cd chown && $(MAKE) check TESTS=basic
	cd cp    && $(MAKE) check TESTS=special-bits
	cd rm    && $(MAKE) check TESTS=no-give-up
	cd rm    && $(MAKE) check TESTS=fail-2eperm

check-recursive: evar-check root-hint

# Warn when `make check' is run with POSIXLY_CORRECT or CDPATH set.
.PHONY: evar-check
evar-check:
	../src/printenv POSIXLY_CORRECT >/dev/null \
	  && sed s/%%/POSIXLY_CORRECT/ $(srcdir)/.env-warn || :
	test "$${CDPATH+set}" = set \
	  && sed s/%%/CDPATH/ $(srcdir)/.env-warn || :

# Advertise `check-root' target.
.PHONY: root-hint
root-hint:
	@echo '***********************************************************'
	@echo "NOTICE: Some tests may be run only as root."
	@echo "  Do \`make check-root' as \`root' to run these tests."
	@echo '***********************************************************'
