#
# spec file for package qa-aim9 (Version 1 )
#
# Copyright (c) 2004 SuSE Linux AG, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://www.suse.de/feedback/
#

# norootforbuild
# usedforbuild    aaa_base acl attr bash bind-utils bison bzip2 coreutils cpio cpp cvs cyrus-sasl db devs diffutils e2fsprogs file filesystem fillup findutils flex gawk gdbm-devel glibc glibc-devel glibc-locale gpm grep groff gzip info insserv kbd less libacl libattr libgcc libstdc++ libxcrypt m4 make man mktemp modutils ncurses ncurses-devel net-tools netcfg openldap2-client openssl pam pam-devel pam-modules patch permissions popt ps rcs readline sed sendmail shadow strace syslogd sysvinit tar texinfo timezone unzip util-linux vim zlib zlib-devel autoconf automake binutils cracklib gcc gdbm gettext libtool perl rpm

Name:         qa_test_aim9
License:      GPL v2 or later
Group:        System/Benchmark
Autoreqprov:  on
Version:      1 
Release:      141
Source0:      %{name}-%{version}.tar.bz2
Source1:      qa_test_aim9.8
Source2:      do_aim9_singleuser
Source3:      qa_aim9.tcf
Source4:      test_aim9-run
Patch0:       fix-RUN-command.patch
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Summary:      AIM Independent Resource Benchmark - Suite IX
Provides:     qa-aim9
Obsoletes:    qa-aim9


%description
The AIM Independent Resource Benchmark exercises and times each
component of a UNIX computer system, independently. The benchmark uses
58 subtests to generate absolute processing rates, in operations per
second, for subsystems, I/O transfers, function calls, and UNIX system
calls.

Test results can be used to compare different machines on a
test-by-test basis or to measure the success or failure of system
tuning and configuration changes on a single system. This benchmark
yields specific results on a per-test basis.



SuSE series: suse

%prep
%setup -n %{name}
#%patch
%patch0 -p0

%build
make 

%install
DESTDIR=$RPM_BUILD_ROOT
rm -rf $DESTDIR
mkdir $DESTDIR
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d $RPM_BUILD_ROOT/usr/share/qa/qa_test_aim9
install -m 755 {aim_1.sh,aim_2.sh,aim_3.sh,singleuser,rpt9,true,RUN,%{S:2}} $DESTDIR/usr/share/qa/qa_test_aim9
install -m 644 {s9workfile,fakeh.tar,input,%{S:3}} $DESTDIR/usr/share/qa/qa_test_aim9
ln -s ../qa_test_aim9/qa_aim9.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf

%clean
#rm -rf $RPM_BUILD_ROOT

%post

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_aim9.8.gz
%doc COPYING CREDITS HISTORY MANIFEST README
%doc doc/*
%dir /usr/share/qa/qa_test_aim9
%dir /usr/share/qa
%dir /usr/share/qa/tools
%dir /usr/share/qa/tcf
/usr/share/qa/qa_test_aim9/*
/usr/share/qa/tcf/qa_aim9.tcf
/usr/share/qa/tools/test_aim9-run


%changelog -n qa_test_aim9
* Wed Aug 10 2011 - llipavsky@suse.cz
- Package rename: qa-aim9 -> qa_test_aim9
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Sun Jan 11 2004 - adrian@suse.de
- build as user
* Wed Jun 18 2003 - ro@suse.de
- added directories to filelist
* Thu Dec 12 2002 - mistinie@suse.de
- Initial version
