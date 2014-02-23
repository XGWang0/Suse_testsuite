#
# spec file for package dbench (Version 4.0)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_dbench-4_0
License:        GPL v2 or later
Group:          System/Benchmark
AutoReqProv:    on
Version:        4.0
Release:        1
Summary:        File System Benchmark Similar to Netbench
Url:            http://samba.org/ftp/tridge/dbench
Source0:        dbench-%{version}.tar.bz2
Source1:        ctcstools-%{version}.tar.bz2
Source2:        qa_test_dbench-4_0.8
Source3:        test_dbench-4_0-nfs-run
Source4:        test_dbench-4_0-nfs4-run
Source5:        test_dbench-4_0-run
Source6:        test_dbench-4_0-syncIO-run
Patch0:		fileio_leak_repair.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	dbench dbench-ctcs2-glue
Obsoletes:	dbench gbench-ctcs2-glue
Requires:       ctcs2 >= 0.1.1 nfs-utils
BuildRequires:  popt-devel autoconf automake libtool

%description
Dbench is a file system benchmark that generates load patterns similar
to those of the commercial Netbench benchmark, but without requiring a
lab of Windows load generators to run. It is now considered a de facto
standard for generating load on the Linux VFS.



Authors:
--------
    Andrew Tridgell <tridge@samba.org>

#%package ctcs2-glue 
#Summary:        File System Benchmark similar to Netbench
#Group:          System/Benchmark
#Requires:       ctcs2 >= 0.1.1 dbench nfs-utils
##BuildArchitectures: 	noarch
#
#%description ctcs2-glue
#Dbench is a file system benchmark that generates load patterns similar
#to those of the commercial Netbench benchmark, but without requiring a
#lab of Windows load generators to run. It is now considered a de-facto
#standard for generating load on the Linux VFS.
#
#This subpackage provides scripts and TCF files to the QA CTCS2 framework.
#
#
#
#Authors:
#--------
#    Andrew Tridgell <tridge@samba.org>

%prep
%setup -q -n dbench-%{version} -a1
%patch0 -p1

%build
./autogen.sh
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr --program-suffix=-4_0 --datadir=/usr/share/dbench-4_0
make

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
# install qa_test_dbench-4_0
make install prefix=$RPM_BUILD_ROOT/usr datadir=$RPM_BUILD_ROOT/usr/share/dbench-4_0 mandir=$RPM_BUILD_ROOT/usr/share/man/man1
mv $RPM_BUILD_ROOT/usr/bin/dbench $RPM_BUILD_ROOT/usr/bin/dbench-4_0 
mv $RPM_BUILD_ROOT/usr/bin/tbench $RPM_BUILD_ROOT/usr/bin/tbench-4_0
mv $RPM_BUILD_ROOT/usr/bin/tbench_srv $RPM_BUILD_ROOT/usr/bin/tbench_srv-4_0
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/qa_test_dbench-4_0
install -m 644 README $RPM_BUILD_ROOT/usr/share/doc/qa_test_dbench-4_0/README
# create directories
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_dbench-4_0/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
# install ctcs2 related files in the ctcs2-glue sub packages
install -m 744 ctcstools/do_dbench $RPM_BUILD_ROOT/usr/share/qa/qa_test_dbench-4_0/
install -m 744 ctcstools/do_dbench_nfs $RPM_BUILD_ROOT/usr/share/qa/qa_test_dbench-4_0/
install -m 744 ctcstools/dbenchnewparser $RPM_BUILD_ROOT/usr/share/qa/qa_test_dbench-4_0/
install -m 744 ctcstools/dbenchnfsparser $RPM_BUILD_ROOT/usr/share/qa/qa_test_dbench-4_0/

install -m 644 ctcstools/dbench-*.tcf $RPM_BUILD_ROOT/usr/share/qa/qa_test_dbench-4_0/tcf/
for A in ctcstools/dbench-*.tcf
do
	B=`basename $A`
	ln -s ../qa_test_dbench-4_0/tcf/$B $RPM_BUILD_ROOT/usr/share/qa/tcf/
done




install -m 744 %{S:3} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 %{S:5} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 %{S:6} $RPM_BUILD_ROOT/usr/share/qa/tools
find $RPM_BUILD_ROOT/usr/share/dbench-4_0 -name "*.txt" -type f -print0 | xargs -r -0 chmod a-x

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_dbench-4_0.8.gz
/usr/bin/dbench-4_0
/usr/bin/tbench-4_0
/usr/bin/tbench_srv-4_0
/usr/share/man/man1/dbench.1.gz
/usr/share/man/man1/tbench.1.gz
/usr/share/man/man1/tbench_srv.1.gz
/usr/share/dbench-4_0
/usr/share/qa/%name/dbenchnewparser
/usr/share/qa/%name/dbenchnfsparser
%doc /usr/share/doc/qa_test_dbench-4_0

#%files ctcs2-glue
#%defattr(-, root, root)
/usr/share/qa

%changelog
