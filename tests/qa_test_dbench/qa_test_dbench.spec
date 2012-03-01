#
# spec file for package dbench (Version 3.04)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_dbench
License:        GPL v2 or later
Group:          System/Benchmark
AutoReqProv:    on
Version:        3.04
Release:        112
Summary:        File System Benchmark Similar to Netbench
Url:            http://samba.org/ftp/tridge/qa_test_dbench/
Source0:        dbench-%{version}.tar.bz2
Source1:        ctcstools-%{version}.tar.bz2
Source2:        qa_test_dbench.8
Source3:        qa_test_dbench-nfs-run
Source4:        qa_test_dbench-nfs4-run
Source5:        qa_test_dbench-run
Source6:        qa_test_dbench-run-old
Patch0:         verbose.diff
Patch1:		fileio_leak_repair.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	dbench dbench-ctcs2-glue
Obsoletes:	dbench gbench-ctcs2-glue
Requires:       ctcs2 >= 0.1.1 nfs-utils

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
%patch1 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr --datadir=/usr/share/dbench
make

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
# install qa_test_dbench
make install prefix=$RPM_BUILD_ROOT/usr datadir=$RPM_BUILD_ROOT/usr/share/dbench mandir=$RPM_BUILD_ROOT/usr/share/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/qa_test_dbench
install -m 644 README $RPM_BUILD_ROOT/usr/share/doc/qa_test_dbench/README
# create directories
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_dbench/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
# install ctcs2 related files in the ctcs2-glue sub packages
install -m 744 ctcstools/do_dbench $RPM_BUILD_ROOT/usr/share/qa/qa_test_dbench/
install -m 744 ctcstools/do_dbench_nfs $RPM_BUILD_ROOT/usr/share/qa/qa_test_dbench/

install -m 644 ctcstools/dbench-*.tcf $RPM_BUILD_ROOT/usr/share/qa/qa_test_dbench/tcf/
for A in ctcstools/dbench-*.tcf
do
	B=`basename $A`
	ln -s ../qa_test_dbench/tcf/$B $RPM_BUILD_ROOT/usr/share/qa/tcf/
done




install -m 744 %{S:3} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 %{S:5} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 %{S:6} $RPM_BUILD_ROOT/usr/share/qa/tools

find $RPM_BUILD_ROOT/usr/share/dbench -name "*.txt" -type f -print0 | xargs -r -0 chmod a-x

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_dbench.8.gz
/usr/bin/dbench
/usr/bin/tbench
/usr/bin/tbench_srv
/usr/share/man/man1/dbench.1.gz
/usr/share/man/man1/tbench.1.gz
/usr/share/man/man1/tbench_srv.1.gz
/usr/share/dbench
%doc /usr/share/doc/qa_test_dbench

#%files ctcs2-glue
#%defattr(-, root, root)
/usr/share/qa

%changelog
* Wed Mar 19 2008 yxu@suse.de
- adjust the wait time in tcf file (much longer than 750s in real test)
* Wed Mar 12 2008 yxu@suse.de
- removed do_dbench,v in ctcstool source (it is not built anywhere)
- retrieving content from the old missing patch fixing_suse_cert_dependency, and integrated into source
* Fri Mar 07 2008 yxu@suse.de
- submit the package to all distributions
* Mon Mar 03 2008 vmarsik@suse.cz
- subpkg dbench-ctcs2-glue: now uses /tmp when /abuild not available
- subpkg dbench-ctcs2-glue: starts a series of 1,2,4,8,12,16,20,24,32,40,48,56,64,96,128,192,256,384,500 processes
- subpkg dbench-ctcs2-glue: every run now takes only the standard time of 120+600 seconds
- subpkg dbench-ctcs2-glue: old version still available under test_dbench-run-old
* Fri Jul 27 2007 pkirsch@suse.de
- dodbench_spare_file fixes the awk command for searching the size
  of the choosen dir. Now it can run on a spare file.
* Wed Feb 21 2007 yxu@suse.de
- merge several fixing_suse_cert_dependency patches into one file
* Thu Feb 08 2007 yxu@suse.de
- finished removing dependency on pkg suse_cert
* Mon Jan 29 2007 yxu@suse.de
- continued removing dependency on pkg suse_cert
- fixed typo
* Fri Nov 10 2006 ro@suse.de
- fix docu permissions
* Mon Feb 06 2006 fseidel@suse.de
- removed dpendency on pkg suse_cert
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Dec 07 2005 kgw@suse.de
- subpkg dbench-ctcs2-glue: Added wrapper script do_qa_test_dbench
  for some pre-test error checking
- subpkg dbench-ctcs2-glue: adapted the *.tcf accordingly
- subpkg dbench-ctcs2-glue: new: dependency on pkg suse-cert
* Tue Nov 15 2005 ories@suse.de
- major update to 3.04
- moved clients.txt to /usr/share/qa_test_dbench/
- added subpackage dbench-ctcs2-glue
* Thu Jun 30 2005 meissner@suse.de
- use RPM_OPT_FLAGS.
* Wed Jun 18 2003 - ro@suse.de
- added directory to filelist
* Wed Sep 18 2002 ro@suse.de
- removed bogus self-provides
* Tue Dec 18 2001 ories@suse.de
- initial package
