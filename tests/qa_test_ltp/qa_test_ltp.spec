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
%if 0%{?suse_version} >= 1220
Requires:	rpmbuild
%endif
AutoReqProv:    on
Summary:        The Linux Test Project
Packager:	Cyril Hrubis chrubis@suse.cz
Version:        20160920
Release:        1
Source:         ltp-full-%{version}.tar.bz2
# CTCS2 Glue
Source1:        ctcstools-%{version}.tar.bz2
Source2:	qa_test_ltp.8
Source3:	leapsec.tcf

# Compiler warnings and workarounds
Patch101:	disable-min_free_kbytes.patch
# Patches 2xx Build Environment Patches
# Waiting for upstream approval
# Patches 3xx RPMLinit Warning Fixes
# Patches 4xx Real Bug Fixes (from internal)
# Patches 5xx Workarounds
# Patches 6xx Realtime related changes
# Patches 7xx Real Bug Fixes from Upstream (e.g. backported patches)
Patch700:	0001-du01.sh-Fix-failures-on-Btrfs-on-ppc32le.patch
# Patches 8xx CTCS2 related changes
# Patches 9xx LTP runtest control file modifications
Patch900:       add-fsstress.patch
Patch901:       enables_lvm_part_xfs.patch
Patch903:       aiodio-runtest-modification-ctcs2.diff
Patch904:	disable_aio_system_crushers.patch
#Patch1001:      bnc458987_utimensat_tests.sh.diff
# For runltp to be usable on installed system
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
%if 0%{?suse_version} < 1220
%patch101 -p1
%endif
# Patches 2xx Build Environment Patches
# Patches 3xx RPMLinit Warning Fixes
# Patches 4xx Real Bug Fixes
# Patches 5xx Workarounds
# Patches 6xx Realtime related changes
# Patches 7xx Real Bug Fixes from Upstream (e.g. backported patches)
%patch700 -p1
# Patches 8xx CTCS2 related changes
# Patches 9xx LTP runtest control file modifications
%patch900 -p1
%patch901 -p0
%patch903 -p1
%patch904 -p1
# runltp script fixes
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

# Install leap second tcf file
install %{SOURCE3} $RPM_BUILD_ROOT/usr/share/qa/qa_test_ltp/tcf/

# Exclude tst_brkm
HARDLINKS1="tst_exit tst_flush tst_fs_has_free tst_get_unused_port tst_kvercmp tst_brk"
HARDLINKS2="tst_res tst_kvercmp2 tst_ncpus tst_ncpus_conf tst_ncpus_max tst_resm"
cd $RPM_BUILD_ROOT/opt/ltp/testcases/bin
for n in $HARDLINKS1 $HARDLINKS2; do
	ln -s -f tst_brkm $n
done

%files
%defattr(-,root,root)
%doc %{_mandir}/man8/qa_test_ltp.8.*
%doc README INSTALL COPYING
/opt/ltp/
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_bindir}/execltp
%{_bindir}/ffsb

%defattr(-,root,root)
/usr/lib/ctcs2
%{_datadir}/qa

%clean
rm -rf $RPM_BUILD_ROOT
