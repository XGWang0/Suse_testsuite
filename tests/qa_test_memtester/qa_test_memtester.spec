#
# spec file for package memtester (Version 4.0.5)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


Name:           qa_test_memtester
Url:            http://pyropus.ca/software/memtester
#BuildRequires:  ctcs2
License:        GPL v2
Group:          SUSE internal
AutoReqProv:    on
Version:        4.0.5
Release:        225
Summary:        tiny but very intensive memory tester
Source0:        memtester-%{version}.tar.gz
Source1:        ctcstools-%version.tar.bz2
Source2:	qa_test_memtester.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	memtester
Obsoletes:	memtester
Requires:       ctcs2
#BuildArchitectures: noarch
#ExclusiveArch: %ix86

%description
RD-QA-Kernel internal tool for intensive memorytests



Authors:
--------
    Charles Cazabon <memtest@discworld.dyndns.org>

%prep
%setup -a1 -n memtester-%{version}

%build
%{__make} clean
%{__make} CFLAGS="$RPM_OPT_FLAGS" all

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
%{__install} -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/qa_test_memtester
%{__install} -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/qa_test_memtester/tcf
%{__install} -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/qa_test_memtester/tools
%{__install} -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/tcf
%{__install} -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/tools
%{__install} -m 755 -d -v $RPM_BUILD_ROOT/usr/bin
cp -v memtester $RPM_BUILD_ROOT/usr/bin/
ln -sf ../../../bin/memtester  $RPM_BUILD_ROOT/usr/share/qa/qa_test_memtester/memtester
cp -v ctcstools/memtester.sh $RPM_BUILD_ROOT/usr/share/qa/qa_test_memtester/memtester.sh
chmod +x $RPM_BUILD_ROOT/usr/share/qa/qa_test_memtester/memtester.sh
ln -sf ../share/qa/qa_test_memtester/memtester.sh $RPM_BUILD_ROOT/usr/bin/memtester.sh
cp -v ctcstools/memtester.tcf $RPM_BUILD_ROOT/usr/share/qa/qa_test_memtester/tcf/
cp -v ctcstools/test_memtester-run $RPM_BUILD_ROOT/usr/share/qa/qa_test_memtester/tools/
chmod +x  $RPM_BUILD_ROOT/usr/share/qa/qa_test_memtester/tools/test_memtester-run
ln -s ../qa_test_memtester/tcf/memtester.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/memtester.tcf
ln -s ../qa_test_memtester/tools/test_memtester-run $RPM_BUILD_ROOT/usr/share/qa/tools/test_memtester-run

%clean
rm -rvf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_memtester.8.gz
/usr/share/qa
/usr/share/qa/tcf
/usr/share/qa/tools
/usr/share/qa/qa_test_memtester
/usr/share/qa/tcf/memtester.tcf
/usr/share/qa/tools/test_memtester-run
/usr/bin/memtester
/usr/bin/memtester.sh

%changelog
* Wed Oct 15 2008 mmrazik@suse.cz
- Fallback to MemFree if LowFree is not available (bnc#398426)
* Mon Mar 10 2008 ro@suse.de
- added directories to filelist
* Thu May 31 2007 yxu@suse.de
- integrated ehamera's patch into tcf file, extended timeout to 18 hours,(bug 278196)
- created a folder ctcs-tools to seperate ctcs2-related files from memtester files
* Thu Mar 15 2007 ehamera@suse.cz
- longer timeout in tcf file (needed for PPC with 8GB RAM)
* Tue Jan 31 2006 fseidel@suse.de
- initial version of qa_test_memtester
