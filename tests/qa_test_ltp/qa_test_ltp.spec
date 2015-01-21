#
# spec file for package qa_test_ltp
#
# Copyright (c) 2009-2015 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_ltp

BuildRequires: flex gcc-c++ libaio-devel zip

# Add libcap-devel on everything but SLES9
%if 0%{?suse_version} >= 1000
BuildRequires: libcap-devel
%endif

# SUSE
# Add attr
%if 0%{?suse_version} >= 1000
BuildRequires: attr-devel
%endif

# RedHat and derivates
# Add attr
# Add numactl (for RHEL5 and newer)
%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora}
BuildRequires: libattr-devel
%if 0%{?rhel_version} && 0%{?rhel_version} >= 505
BuildRequires: numactl-devel
%endif
%endif

# SUSE
# Add libnuma
# Does not exists for x86, s390, s390x, arm, on SLES9 SLES10
%ifnarch i386 i486 i586 i686 s390 s390x aarch64 armv7l
%if 0%{?suse_version} >= 1020
BuildRequires: libnuma-devel
%endif
%endif

#
# For quotactl tests
#
# libuuid exists only for SLES11 and newer
%if 0%{?suse_version}
BuildRequires: xfsprogs-devel
%if 0%{?suse_version} >= 1100
BuildRequires: libuuid-devel
%endif
%endif

#
# For tirpc testcases
#
# Enable once errors are fixed
#
%if 0%{?suse_version} >= 1100
BuildRequires: libtirpc-devel
%endif

Url:            http://linux-test-project.github.io
License:        GPL v2 or later
Group:          System/Benchmark
Provides:       runalltests.sh diskio.sh networktests.sh
Provides:	ltp ltp-ctcs2-glue
Obsoletes:	ltp ltp-ctcs2-glue
Requires:       bash
Requires:       perl
Requires:	qa_lib_ctcs2
Requires:       python
AutoReqProv:    on
Summary:        The Linux Test Project
Packager:	Cyril Hrubis chrubis@suse.cz
Version:        20150119
Release:        1
Source:         ltp-full-%{version}.tar.bz2
# CTCS2 Glue
Source1:        ctcstools-%{version}.tar.bz2
Source2:	qa_test_ltp.8

# Compiler warnings and workarounds
Patch102:	disable-min_free_kbytes.patch
# Patches 2xx Build Environment Patches
# Waiting for upstream approval
# Patches 3xx RPMLinit Warning Fixes
# Patches 4xx Real Bug Fixes (from internal)
# Patches 5xx Workarounds
Patch501:	change_ltp_prog_install_dir.patch
# Patches 6xx Realtime related changes
# Patches 7xx Real Bug Fixes from Upstream (e.g. backported patches)
# Patches 8xx CTCS2 related changes
# Patches 9xx LTP runtest control file modifications
Patch900:       add-fsstress.patch
Patch901:       enables_lvm_part_xfs.patch
Patch903:       aiodio-runtest-modification-ctcs2.diff
Patch904:	disable_aio_system_crushers.patch
#Patch1001:      bnc458987_utimensat_tests.sh.diff
# For runltp to be usable on installed system
Patch1002:      allow-symlink-to-runltp.patch
Patch1004:      fix-cpuctl-tests-output-dir.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
A collection of test suites to validate the reliability, robustness and
stability of Linux. It provides tools for testing the kernel and
related features.

This package also adds some additional scripts to the ctcs2 tools directory.
With them it is possible to run all LTP tests via ctcs2 and therefore
to have improved result files. Additionally the script ltp-stress.py
allows to run all (or selected) LTP tests in a randomized manner.

Authors:
--------
    LTP authors.

%prep
%setup -q -n ltp-full-%{version} -a1
# Compiler warnings and workarounds
%patch102 -p1
# Patches 2xx Build Environment Patches
# Patches 3xx RPMLinit Warning Fixes
# Patches 4xx Real Bug Fixes
# Patches 5xx Workarounds
%patch501 -p1
# Patches 6xx Realtime related changes
# Patches 7xx Real Bug Fixes from Upstream (e.g. backported patches)
# Patches 8xx CTCS2 related changes
# Patches 9xx LTP runtest control file modifications
%patch900 -p1
%patch901 -p0
%patch903 -p1
%patch904 -p1
# runltp script fixes
%patch1002 -p1
%patch1004 -p1

%build

%configure --prefix=/opt/ltp --with-openposix-testsuite --with-realtime-testsuite
find testcases | gzip --fast > TC_INDEX.gz

make all %{?jobs:-j%jobs}
make -C testcases/open_posix_testsuite all

%install

# install our manual page
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_mandir}/man8/qa_test_ltp.8

# install LTP
make DESTDIR=$RPM_BUILD_ROOT install

# Now subpackage ltp-ctcs2-glue
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/config/ltp
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/bin/
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_ltp
cp -v TC_INDEX.gz $RPM_BUILD_ROOT/usr/share/qa/qa_test_ltp/

# Deal with openposix test binaries and create runtest file
mkdir -p $RPM_BUILD_ROOT/opt/ltp/testcases/bin/openposix

cd testcases/open_posix_testsuite
# Exclude tests which are "build only"
for i in `find conformance/interfaces/ -name '*.run-test' -a ! -name '*-buildonly*'` ; do
	# create runtest openposix file
	echo `basename "$i" .run-test | sed s/-/_/` '${LTPROOT}/testcases/bin/openposix/'$i >> ../../runtest/openposix;
	# install binaries
	mkdir -p $RPM_BUILD_ROOT/opt/ltp/testcases/bin/openposix/`dirname $i`;
	cp $i $RPM_BUILD_ROOT/opt/ltp/testcases/bin/openposix/`dirname $i`;
done
cp ../../runtest/openposix $RPM_BUILD_ROOT/opt/ltp/runtest/
cd ../..

# Install ctcstools with excutable bit
install -m 755 ctcstools/* $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
ln -s ../../../../../opt/ltp/runtest $RPM_BUILD_ROOT/usr/lib/ctcs2/config/ltp/runtest

# Generate ctcs2 tcf files from runtest files
$RPM_BUILD_ROOT/usr/lib/ctcs2/tools/ltp-generator 720 %{_libdir} $RPM_BUILD_ROOT

#Exclude tst_brk
HARDLINKS="tst_brkm tst_res tst_resm tst_exit tst_flush tst_brkloop tst_brkloopm tst_kvercmp"
cd $RPM_BUILD_ROOT/opt/ltp/testcases/bin
for n in $HARDLINKS; do
	ln -s -f tst_brk $n
done

%files
%defattr(-,root,root)
%doc %{_mandir}/man8/qa_test_ltp.8.*
%doc README INSTALL COPYING
/opt/ltp/
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_bindir}/ltp-bump
%{_bindir}/ltp-pan
%{_bindir}/ltp-scanner
%{_bindir}/execltp
%{_bindir}/ffsb

%defattr(-,root,root)
/usr/lib/ctcs2
%{_datadir}/qa

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Jan 21 2015 Cyril Hrubis chrubis@suse.cz
  Update to ltp-full-20150119

* Mon Sep 01 2014 Cyril Hrubis chrubis@suse.cz
  Update to ltp-full-20140828

* Mon Apr 28 2014 Cyril Hrubis chrubis@suse.cz
  Update to ltp-full-20140422

* Tue Mar 25 2014 Cyril Hrubis chrubis@suse.cz
  Backport fix for shm_open, shm_unlink ENAMETOOLONG testcases.

* Mon Mar 10 2014 Cyril Hrubis chrubis@suse.cz
  Backport fixes for link() failures due to enabled protected_hardlinks
  Backport fixes for swapon() and swapoff() testcases on Btrfs

* Wed Jan 15 2014 Cyril Hrubis chrubis@suse.cz
  Update to ltp-full-20140115

  Add build dependency on numa devel library.

  Add two more tcf files (controllers, numa) into default run.

* Mon Sep  9 2013 Cyril Hrubis chrubis@suse.cz
  Update to ltp-full-20130904

  Fixed bug #729880

* Mon Jun  3 2013 Cyril Hrubis chrubis@suse.cz
  Update to ltp-full-20130503

* Thu May  2 2013 Cyril Hrubis chrubis@suse.cz

  Backported fixes for following testcases:

  * accept4 - Return TCONF on ENOSYS

  * ksm05 - Fix Segfault on ENOSYS

  * thp03: Return TCONF on ENOSYS

  * pthread_key_create_5-1: Fix.

  * pthread_mutexattr_gettype: Return UNTESTED on unimplemented.

* Mon Apr 29 2013 Cyril Hrubis chrubis@suse.cz

  Backport fixes for aio_fsync_2-1 and aio_fsync_3-1
  (the testcases Segfaulted randomly due to race
   condition)

* Wed Apr 24 2013 Cyril Hrubis chrubis@suse.cz

  Backport patch for proc01 for false possitive on
  xen proc files.

* Wed Apr 17 2013 Cyril Hrubis chrubis@suse.cz

  Backport several patches and fix openposix wrapper.

  * Remove lio_listio_11-1 as the test was wrong

  * Fixup several testcases to return UNTESTED
    instead of UNRESOLVED when the test for
    optional behavior (and not implemented by Linux).

  * Fixup the openposix wrapper to interpret the
    UNTESTED as skipped under CTCS2 which is closer
    to the openposix interpretation.

* Thu Mar 21 2013 Cyril Hrubis chrubis@suse.cz

  Silenced process_stress output (bug #810495).

  Turned off debug for FSX tests

  Fixed tests bellow flush stdout before fork:

  pthread_cond_broadcast/1-2.c
  pthread_create/3-2.c
  pthread_exit/6-1.c
  pthread_cond_timedwait/4-2.c

  All in order not to generate several megabytes
  of useless logs.

* Wed Mar 20 2013 Cyril Hrubis chrubis@suse.cz
  Backported fix for sysctl03.

* Tue Mar  5 2013 Cyril Hrubis chrubis@suse.cz
  Backported patches to remove stubs from
  openposix testsuite.

* Mon Mar  4 2013 Cyril Hrubis chrubis@suse.cz
  Backported fixes for:

  getrusage04
  pthread_cond_timedwait/{2-2,2-3}
  readlink04

* Wed Feb 13 2013 Cyril Hrubis chrubis@suse.cz
  Update to ltp-full-20130109

* Thu Oct 18 2012 Cyril Hrubis chrubis@suse.cz
  Update to ltp-full-20120903

* Wed Jun 20 2012 Cyril Hrubis chrubis@suse.cz
  Fixed realtime build.

* Wed Jun 06 2012 Cyril Hrubis chrubis@suse.cz
  Update to ltp-full-20120401

* Thu Feb 02 2012 Cyril Hrubis chrubis@suse.cz
  Update to ltp-full-20120104

* Mon Aug 22 2011 - llipavsky@suse.cz
- Package rename: ltp -> qa_test_ltp

* Fri Aug 19 2011 Cyril Hrubis chrubis@suse.cz
  Updated ltp package to newest released version.
