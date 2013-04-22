#
# spec file for package qa_test_ltp
#
# Copyright (c) 2009-2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

#
# libcap-devel is not present on sles 9
#
%if 0%{?sles_version} == 9
BuildRequires: flex gcc-c++ libaio-devel zip
%else
BuildRequires: flex gcc-c++ libaio-devel libcap-devel zip
%endif

#
# Attr library name is different on RedHat derivatives
#
%if 0%{?suse_version} >= 1000
BuildRequires: attr-devel
%endif

%if 0%{?rhel_version} || 0%{?centos_version} || 0%{?fedora}
BuildRequires: libattr-devel
%endif

Url:            http://ltp.sf.net
License:        GPL v2 or later
Group:          System/Benchmark
Provides:       runalltests.sh diskio.sh networktests.sh 
Provides:	ltp ltp-ctcs2-glue
Obsoletes:	ltp ltp-ctcs2-glue
Requires:       bash
Requires:       perl
Requires:      	qa_lib_ctcs2 
Requires:       python
AutoReqProv:    on
Summary:        The Linux Test Project
Packager:	Cyril Hrubis chrubis@suse.cz
Version:        20130109
Release:        1
Source:         ltp-full-%{version}.bz2
# CTCS2 Glue
Source1:        ctcstools-%{version}.tar.bz2
Source2:	qa_test_ltp.8
# Compiler warnings and workarounds
Patch100:	sles9-workarounds.patch
Patch102:	disable-min_free_kbytes.patch
# Patches 2xx Build Environment Patches
# Waiting for upstream approval
Patch300:	0001-Fix-realtime-build.patch
Patch301:	0001-syscalls-mremap05-Fix-build.patch
# Patches 3xx RPMLinit Warning Fixes
# Patches 4xx Real Bug Fixes (from internal)
Patch408:       fix-sched_stress.patch
# Patches 5xx Workarounds
Patch501:	change_ltp_prog_install_dir.patch
# Patches 6xx Realtime related changes
#Patch601:       fix-sched_setparam_10_1.patch
# Patches 7xx Real Bug Fixes from Upstream (e.g. backported patches)
Patch700:	0001-syscalls-getrusage04-Try-guess-timer-granularity.patch
Patch701:	0001-openposix-.-pthread_cond_timedwait-2-2-2-3.patch
Patch702:	0001-syscalls-readlink04-Cleanup.patch
Patch703:	0001-syscalls-readlink04-Simplify-the-code.patch
Patch704:	0001-openposix-Remove-stubs.patch
Patch705:	0001-syscalls-sysctl03-Change-TWARN-to-TINFO.patch
Patch706:	0001-testcases-.-process_stress-Silence-the-output.patch
Patch707:	0001-runtest-ltp-aiodio.part3-fsx-linux-turn-off-debug.patch
Patch708:	0001-openposix-Fix-several-return-values.patch
Patch709:	remove_lio_listio_11-1.patch
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
%if 0%{?sles_version} == 9
%patch100 -p1
%endif
%patch102 -p1
# Patches 2xx Build Environment Patches
# Patches 3xx RPMLinit Warning Fixes
%patch300 -p1
%patch301 -p1
# Patches 4xx Real Bug Fixes
%patch408 -p1
# Patches 5xx Workarounds
%patch501 -p1
# Patches 6xx Realtime related changes
# Patches 7xx Real Bug Fixes from Upstream (e.g. backported patches)
%patch700 -p1
%patch701 -p1
%patch702 -p1
%patch703 -p1
%patch704 -p1
%patch705 -p1
%patch706 -p1
%patch707 -p1
%patch708 -p1
%patch709 -p1
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
	echo `echo $i|cut -d '/' -f 3- | sed -e 's/-/_/g' -e 's#/#_#g'` '${LTPROOT}/testcases/bin/openposix/'$i >> ../../runtest/openposix;
	mkdir -p $RPM_BUILD_ROOT/opt/ltp/testcases/bin/openposix/`dirname $i`;
	cp $i $RPM_BUILD_ROOT/opt/ltp/testcases/bin/openposix/`dirname $i`;
done
cp ../../runtest/openposix $RPM_BUILD_ROOT/opt/ltp/runtest/
cd ../..


# Install ctcstools with excutable bit
install -m 755 ctcstools/* $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
ln -s ../../../../usr/lib/ctcs2/tools/ltp_wrapper.sh $RPM_BUILD_ROOT/usr/lib/ctcs2/tools/openposix_wrapper.sh
ln -s ../../../../../opt/ltp/runtest $RPM_BUILD_ROOT/usr/lib/ctcs2/config/ltp/runtest
ln -s ../../../../opt/ltp/testcases/bin $RPM_BUILD_ROOT/usr/lib/ctcs2/bin/ltp

# Generate ctcs2 tcf files from runtest files
$RPM_BUILD_ROOT/usr/lib/ctcs2/tools/ltp-generator 300 %{_libdir} $RPM_BUILD_ROOT

#Exclude tst_brk
HARDLINKS="tst_brkm tst_res tst_resm tst_exit tst_flush tst_brkloop tst_brkloopm tst_kvercmp"
cd $RPM_BUILD_ROOT/opt/ltp/testcases/bin
for n in $HARDLINKS; do
	ln -s -f tst_brk $n
done

%files
%defattr(-,root,root)
%doc %{_mandir}/man8/qa_test_ltp.8.*
%doc README INSTALL COPYING CREDITS
/opt/ltp/
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_bindir}/ltp-bump
%{_bindir}/ltp-pan
%{_bindir}/ltp-scanner
%{_bindir}/execltp

%defattr(-,root,root)
/usr/lib/ctcs2
%{_datadir}/qa
#%{_datadir}/qa/qa_test_ltp

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
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

* Fri Feb 02 2012 Cyril Hrubis chrubis@suse.cz
  Update to ltp-full-20120104

* Mon Aug 22 2011 - llipavsky@suse.cz
- Package rename: ltp -> qa_test_ltp

* Fri Aug 19 2011 Cyril Hrubis chrubis@suse.cz
  Updated ltp package to newest released version.
