#
# spec file for package ltp (Version 20081031)
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

Url:            http://ltp.sf.net
License:        GPL v2 or later
Group:          System/Benchmark
Provides:       runalltests.sh diskio.sh networktests.sh 
Provides:	ltp ltp-ctcs2-glue
Obsoletes:	ltp ltp-ctcs2-glue
Requires:       bash
Requires:       perl
Requires:       python
AutoReqProv:    on
Summary:        The Linux Test Project
Packager:	Cyril Hrubis chrubis@suse.cz
Version:        20110606
Release:        1
Source:         ltp-full-%{version}.bz2
# For subpackage creation
Source1:        ctcstools-%{version}.tar.bz2
Source2:	qa_test_ltp.8
# Fixes for internal tools
Patch001:	fix_ctcs2_glue.patch
Patch002:	reorder_run-ltp_testcases.patch
Patch003:	fix_ltp_wrapper.patch
Patch004:	add_testcases_to_ltp-run.patch
# Compiler warnings and workarounds
Patch100:	sles9-workarounds.patch
Patch101:	workaround-sles11-capability-headers.patch
# Patches 2xx Build Environment Patches
# Waiting for upstream approval
Patch200:	fix_clone_include.patch
# Patches 3xx RPMLinit Warning Fixes
# Patches 4xx Real Bug Fixes (from internal)
Patch404:       increase-stack-size.diff
Patch408:       fix-sched_stress.patch
# Patches 5xx Workarounds
Patch501:	change_ltp_prog_install_dir.patch
# Patches 6xx Realtime related changes
Patch601:       fix-sched_setparam_10_1.patch
Patch602:       bug-307752_sched_setparam-2-1.patch
# Patches 7xx Real Bug Fixes from Upstream (e.g. backported patches)
# Patches 8xx CTCS2 related changes
Patch802:       pan-pass-returnvalue.diff
Patch803:	ctcs2-glue-fixups.patch
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

# %package devel 
#License:        GPL v2 or later
#Summary:        The Linux Test Project
#Group:          System/Benchmark
#AutoReqProv:    on
#Requires:       ltp = %{version}
#
#%description devel
#A collection of test suites to validate the reliability, robustness and
#stability of Linux. It provides tools for testing the kernel and
#related features.
#
#
#
#Authors:
#--------
#    LTP authors.


%prep
%setup -q -n ltp-full-%{version} -a1
# Fixes for internal tools
%patch001 -p1
%patch002 -p1
%patch003 -p1
%patch004 -p1
# Compiler warnings and workarounds
%if 0%{?sles_version} == 9
%patch100 -p1
%endif
%patch101 -p1
# Patches 2xx Build Environment Patches
%patch200 -p1
# Patches 3xx RPMLinit Warning Fixes
# Patches 4xx Real Bug Fixes
#%patch404 -p1
%patch408 -p1
# Patches 5xx Workarounds
%patch501 -p1
# Patches 6xx Realtime related changes
#%patch601 -p1
#%patch602 -p1
# Patches 7xx Real Bug Fixes from Upstream (e.g. backported patches)
# Patches 8xx CTCS2 related changes
%patch802 -p1
%patch803 -p1
# Patches 9xx LTP runtest control file modifications 
%patch900 -p1
%patch901 -p0
%patch903 -p1
%patch904 -p1
# runltp script fixes
%patch1002 -p1
%patch1004 -p1

%build
#%ifarch %ix86 x86_64 ppc ppc64
#%if 0%{?sles_version} != 9

#%endif
#%endif

%configure --prefix=/opt/ltp --with-openposix-testsuite
find testcases | gzip --fast > TC_INDEX.gz

make all %{?jobs:-j%jobs}
make -C testcases/open_posix_testsuite all %{?jobs:-j%jobs}

%install

# install our manual page
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_mandir}/man8/qa_test_ltp.8

# install LTP
make DESTDIR=$RPM_BUILD_ROOT install

# Realtime tests build only on  i386, x86_64, ppc, ppc64
#%ifarch %ix86 x86_64 ppc ppc64
#%if 0%{?sles_version} != 9
#make -C testcases/realtime DESTDIR=$RPM_BUILD_ROOT install
#%endif
#%endif

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
%doc README INSTALL COPYING CREDITS ChangeLog
/opt/ltp/
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_bindir}/ltp-bump
%{_bindir}/ltp-pan
%{_bindir}/ltp-scanner
%{_bindir}/execltp
# It is back, reminder to fix testcases/mem/ correclty
%{_libdir}/libmem.a

#%files devel
#%defattr(-,root,root)
#%{_includedir}/qa_test_ltp/
#%{_libdir}/libltp.a
#%{_datadir}/pkgconfig/ltp.pc
#/usr/share/aclocal/*

%defattr(-,root,root)
/usr/lib/ctcs2
%{_datadir}/qa
%{_datadir}/qa/qa_test_ltp

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Aug 22 2011 - llipavsky@suse.cz
- Package rename: ltp -> qa_test_ltp

* Fri Aug 19 2011 Cyril Hrubis chrubis@suse.cz
  Updated ltp package to newest released version.
