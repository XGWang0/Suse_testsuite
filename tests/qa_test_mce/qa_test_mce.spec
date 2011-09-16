#
# spec file for package qa_test_mce
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


Name:           qa_test_mce

Url:            git://git.kernel.org/pub/scm/utils/cpu/mce/mce-test.git
License:        GPL v2 or later
Group:          System/Benchmark
AutoReqProv:    on
Provides:	mce-test
Obsoletes:	mce-test
Requires:	mce-inject mcelog ctcs2
Summary:        MCE testing scripts with ctcs2 integration
Version:        git_04_02_2010
Release:        1
Source0:        mce-test-%{version}.tar.bz2
Source1:	mce-test.tcf
Source2:	test_mce-run
Source3:	qa-mce-wrapper.sh
Source4:        qa_test_mce.8
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description

Machine Check Exception test scripts and data. Needs kernel 2.6.31+ kernel with
CONFIG_X86_MCE_INJECT enabled. 

Authors:
--------
	Andi Kleen
	Ying Huang

%prep
%setup -q -n mce-test-%{version}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 644 %{S:1} -v $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf
install -m 755 %{S:2} -v $RPM_BUILD_ROOT/usr/share/qa/tools
cp -rv * $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 775 %{S:3} -v $RPM_BUILD_ROOT/usr/share/qa/qa_test_mce/tools
ln -s ../%{name}/tcf/mce-test.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_mce.8.gz
/usr/share/qa
/usr/share/qa/%{name}/
/usr/share/qa/%{name}/*
/usr/share/qa/%{name}/tcf/mce-test.tcf
/usr/share/qa/tcf/mce-test.tcf
/usr/share/qa/tools/test_mce-run

%clean
%{__rm} -rvf $RPM_BUILD_ROOT/usr/share/qa/%{name}

%changelog
* Wed Aug 17 2011 - llipavsky@suse.cz
- Remove qa_dummy dependency
* Thu Aug 11 2011 - llipavsky@suse.cz
- Package rename: mce-test -> qa_test_mce-
* Thu Mar 11 2010 chrubis@suse.cz
 Added wrapper for simple tests in
 order to propagate test result as return
 number.

* Tue Feb 25 2010 chrubis@suse.cz
 Created initial package version.
