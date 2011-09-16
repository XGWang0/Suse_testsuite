#
# spec file for package qa-aim7 (Version 1 )
#
# Copyright (c) 2004 SuSE Linux AG, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://www.suse.de/feedback/
#

# norootforbuild
# usedforbuild    aaa_base acl attr bash bind-utils bison bzip2 coreutils cpio cpp cvs cyrus-sasl db devs diffutils e2fsprogs file filesystem fillup findutils flex gawk gdbm-devel glibc glibc-devel glibc-locale gpm grep groff gzip info insserv kbd less libacl libattr libgcc libstdc++ libxcrypt m4 make man mktemp modutils ncurses ncurses-devel net-tools netcfg openldap2-client openssl pam pam-devel pam-modules patch permissions popt ps rcs readline sed sendmail shadow strace syslogd sysvinit tar texinfo timezone unzip util-linux vim zlib zlib-devel autoconf automake binutils cracklib gcc gdbm gettext libtool perl rpm

Name:         qa_test_aim7
License:      GPL
Group:        System/Benchmark
Autoreqprov:  on
Version:      1 
Release:      140
Source0:       %{name}-%{version}.tar.bz2
Source1:	qa_test_aim7.8
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Summary:      AIM7 test and benchmarking suite
Provides:       qa-aim7
Obsoletes:      qa-aim7


%description
The AIM Multiuser Benchmark - Suite VII tests and measures the
performance of Open System multiuser computers. Multiuser computer
environments typically have the following general characteristics in
common:

- A large number of tasks are run concurrently

- Disk storage increases dramatically as the number of users
   increase.

- Complex numerically intense applications are performed
   infrequently

- An important amount of time is spent sorting and searching through
   large amounts of data.

- After data is used it is placed back on disk because it is a
   shared resource.

- A large amount of time is spent in common runtime libraries.

Multiuser systems are commonly used to support the following types of
user environments:

- Multiuser/shared system environment performing office automation,
   word processing, spreadsheet, email, database, payroll, and data
   processing.

- Compute server environment that uses an extremely large quantity
   of data, performs large quantities of floating point
   calculations, and large amounts of Interprocess Communications
   (IPC) for graphics.

- Large database environment with a lot of disk I/O, data in memory,
   and IPC via shared memory.

- File server environment with a heavy concentration of integer compute
file system operations.



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
install -d $DESTDIR/opt/testing/aim7
install -m 755 aim_1.sh $DESTDIR/opt/testing/aim7
install -m 755 aim_2.sh $DESTDIR/opt/testing/aim7
install -m 755 aim_3.sh $DESTDIR/opt/testing/aim7
install -m 755 slay $DESTDIR/opt/testing/aim7
install -m 755 aim_3.sh $DESTDIR/opt/testing/aim7
install -m 755 multitask $DESTDIR/opt/testing/aim7
install -m 755 rpt $DESTDIR/opt/testing/aim7
install -m 755 slay.sysv $DESTDIR/opt/testing/aim7
install -m 755 true $DESTDIR/opt/testing/aim7
install -m 644 config $DESTDIR/opt/testing/aim7
install -m 644 workfile* $DESTDIR/opt/testing/aim7
install -m 644 fakeh.tar $DESTDIR/opt/testing/aim7

%clean
#rm -rf $RPM_BUILD_ROOT

%post

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_aim7.8.gz
%doc COPYING CREDITS HISTORY MANIFEST README
%doc doc/*
%dir /opt/testing
%dir /opt/testing/aim7
/opt/testing/aim7/rpt
/opt/testing/aim7/slay
/opt/testing/aim7/true
/opt/testing/aim7/workfile.shared
/opt/testing/aim7/fakeh.tar
/opt/testing/aim7/workfile.fserver
/opt/testing/aim7/aim_1.sh
/opt/testing/aim7/aim_2.sh
/opt/testing/aim7/aim_3.sh
/opt/testing/aim7/config
/opt/testing/aim7/multitask
/opt/testing/aim7/workfile
/opt/testing/aim7/workfile.dbase
/opt/testing/aim7/workfile.compute
/opt/testing/aim7/slay.sysv

%changelog -n qa_test_aim7
* Wed Aug 10 2011 - llipavsky@suse.cz
- Package rename: qa-aim7 -> qa_test_aim7
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Sat Jan 10 2004 - adrian@suse.de
- build as user
* Wed Jun 18 2003 - ro@suse.de
- added directories to filelist
* Wed Dec 11 2002 - mistinie@suse.de
- Initial version
