#
# spec file for package sysbench (Version 0.4.8)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_sysbench
%define _unpackaged_files_terminate_build 0 
BuildRequires:  mysql-devel
Summary:        A MySQL benchmarking tool
Version:        0.4.8
Release:        64
License:        GPL v2 or later
Group:          System/Benchmark
Url:            http://sourceforge.net/projects/sysbench
AutoReqProv:    on
PreReq:         %insserv_prereq %fillup_prereq
Provides:	sysbench sysbench-ctcs2-glue
Obsoletes:	sysbench sysbench-ctcs2-glue
Requires:       mysql mysql-client openssl ctcs2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        sysbench-%{version}.tar.bz2
Source1:        sysbench-example-tests.tar.bz2
Source2:        ctcstools-%{version}.tar.bz2
Source3:        qa_test_sysbench.8
Patch0:         sysbench-%{version}.dif
Patch1:         sysbench-check_return_value.diff
Patch2:         rdrw_mutex.patch
Patch3: 		sysbench-wrong-option-mysql_table.diff
Patch4: 		modify_thread-num_all-tests.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#BuildArchitectures: noarch

%description
This benchmark was designed for identifying basic system parameters, as
they are important for systems using MySQL (w Innodb) under intensive
load.



Authors:
--------
    Alexey Kopytov (alexeyk@mysql.com)
    Konstantin Osipov (rabidtransit@users.sourceforge.net)

#%package ctcs2-glue
#License:        GPL v2 or later
#Summary:        The let-sysbench-be-run-via-ctcs glue
#Group:          Development/Tools/Other
#AutoReqProv:    on
#Requires:       ctcs2 >= 0.1.6
#Requires:       sysbench = %{version}
#
#%description ctcs2-glue
#This package contains the glue for integrating sysbench test-suite into
#the ctcs testing framework.
#
#
#
#Authors:
#--------
#    Patrick Kirsch <pkirsch@suse.de>

%prep
%setup -n sysbench-%version -a 2
%patch0 -p 0
%patch1 -p 0
%patch2 -p 0
%setup -n sysbench-%version -T -D -a 1
%patch3 -p 1
%patch4 -p 1

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{buildroot}/usr  --libdir=%_libdir --mandir=%_mandir --infodir=%{buildroot}/usr
make -e CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS -fno-exceptions" 'VERSION_NO="\"%version\""'

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
# Version will be used for link to library: .so.%version, see below in %files
make install
#pushd %{name}-example-tests
install -D -m 755 sysbench-example-tests/sysbench-example-test %{buildroot}/usr/bin/sysbench-example-test 
install -D -m 755 sysbench-example-tests/sysbench-example-all-tests  %{buildroot}/usr/bin/sysbench-example-all-tests
#popd
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
cp ctcstools/test_sysbench-run $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
cp ctcstools/sysbench-full.tcf $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
cp ctcstools/test_sysbench-bench-run $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
cp ctcstools/sysbench-bench.tcf $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
cp ctcstools/sysbench.tcf $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf

%post 
if [ -x /etc/init.d/mysql ] ; then
    grep max_connections /etc/init.d/mysql || sed -i 's/--skip-networking/--max_connections=1000 \\\n\t\t\t\t--skip-networking/g' /etc/init.d/mysql
    /etc/init.d/mysql restart
fi

%preun

%postun

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_sysbench.8.gz
%_bindir/*
%dir /usr/share/doc/sysbench
/usr/share/doc/sysbench/manual.html

#%files ctcs2-glue
#%defattr(-, root, root)
/usr/lib/ctcs2

%changelog
* Thu Jul 31 2008 yxu@suse.de
- modified the test_sysbench-run file so that
  all test_file* are removed automatically after test finished
* Thu Jun 26 2008 pkirsch@suse.de
- added sub package ctcstools for ctcs2 integration
- included several definied testcase and workload
* Mon Oct 29 2007 pkirsch@suse.de
- fixed thread-concurency in sb_fileio.c, so that --validate=on
  works without throwing FATAL messages
* Thu Oct 11 2007 pkirsch@suse.de
- added sysbench-example-all-tests, which should make use of
  sysbench's available variations
* Fri Oct 05 2007 pkirsch@suse.de
- update to version 0.4.8
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue May 17 2005 trenn@suse.de
- fixed gcc 4.0 warnings -> posix_memalign return value needs to
  be checked
* Mon Apr 11 2005 trenn@suse.de
- fixed gcc 4.0 warnings -> struct not initialised
* Mon Mar 07 2005 ro@suse.de
- fix example-tests tarball
* Wed Mar 02 2005 trenn@suse.de
- corrected the sysbench-example-tests script
* Tue Feb 22 2005 trenn@suse.de
- initiale checkin
