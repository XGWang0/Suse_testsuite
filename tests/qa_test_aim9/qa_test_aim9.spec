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
License:      GPL
Group:        System/Benchmark
Autoreqprov:  on
Version:      1 
Release:      141
Source0:       %{name}-%{version}.tar.bz2
Source1:	qa_test_aim9.8
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
#

%build
make 

%install
DESTDIR=$RPM_BUILD_ROOT
rm -rf $DESTDIR
mkdir $DESTDIR
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d $DESTDIR/opt/testing/aim9
install -m 755 aim_1.sh $DESTDIR/opt/testing/aim9
install -m 755 aim_2.sh $DESTDIR/opt/testing/aim9
install -m 755 aim_3.sh $DESTDIR/opt/testing/aim9
install -m 755 aim_3.sh $DESTDIR/opt/testing/aim9
install -m 755 singleuser $DESTDIR/opt/testing/aim9
install -m 755 rpt9 $DESTDIR/opt/testing/aim9
install -m 755 true $DESTDIR/opt/testing/aim9
install -m 644 s9workfile $DESTDIR/opt/testing/aim9
install -m 644 fakeh.tar $DESTDIR/opt/testing/aim9

%clean
#rm -rf $RPM_BUILD_ROOT

%post

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_aim9.8.gz
%doc COPYING CREDITS HISTORY MANIFEST README
%doc doc/*
%dir /opt/testing
%dir /opt/testing/aim9
/opt/testing/aim9/rpt9
/opt/testing/aim9/true
/opt/testing/aim9/s9workfile
/opt/testing/aim9/fakeh.tar
/opt/testing/aim9/aim_1.sh
/opt/testing/aim9/aim_2.sh
/opt/testing/aim9/aim_3.sh
/opt/testing/aim9/singleuser

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
