#
# spec file for package bonnie (Version 1.4)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_bonnie++
Url:            http://www.garloff.de/kurt/linux/bonnie
License:        Artistic
Group:          System/Benchmark
AutoReqProv:    on
Summary:        File System Benchmark
Version:        1.03e
Release:        1
Source0:        bonnie++-%{version}.tgz
Source1:	qa_test_bonnie++.8
Source2:	test_bonnie++-run
Source3:	do_bonnie++
Source4:	bonnie++-default.tcf
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires: gcc-c++

%description
Bonnie++ is a popular performance benchmark that targets various aspects
of Unix file systems.

This subpackage also provides scripts and TCF files to the QA CTCS2 framework.


Authors:
--------
    QA-APACII team

%prep
%setup -n bonnie++-1.03e 

%build
%configure
make CC=gcc CFLAGS="$RPM_OPT_FLAGS"

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
#make install DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}
install -D -m 755 bonnie++ $RPM_BUILD_ROOT/usr/sbin/bonnie++
install -D -m 755 bon_csv2html $RPM_BUILD_ROOT/usr/bin/bon_csv2html
install -D -m 755 bon_csv2txt $RPM_BUILD_ROOT/usr/bin/bon_csv2txt
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_bonnie++
install -m 744 %{S:3} $RPM_BUILD_ROOT/usr/share/qa/qa_test_bonnie++/
install -m 744 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools/
install -m 755 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/tcf/

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_bonnie++.8.gz
/usr/share/qa/qa_test_bonnie++
/usr/share/qa/tools/test_bonnie++-run
/usr/share/qa/tcf
/usr/share/qa
/usr/sbin/bonnie++
/usr/bin/bon_csv2html
/usr/bin/bon_csv2txt

%changelog -n qa_test_bonnie++
* Tue Jun 17 2014 cachen@suse.com
- Initial Bonnie++.
