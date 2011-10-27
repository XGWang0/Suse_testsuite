#
# spec file for package qa_mozmill (Version 0.1)
#
# Copyright (c) 2010 Novell, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugzilla.novell.com/
#

# norootforbuild

Name:           qa_test_mozmill
BuildRequires:  python
License:        MPL 1.1; GPL v2 or later; LGPL v2.1 or later
Group:          SuSE internal
AutoReqProv:	on
Version:	0.2
Release:	1
Summary:	An automation test framework for firefox.
Url:		http://hg.mozilla.org/qa/mozmill-tests
Source0:	%{name}-%{version}.tar.bz2
Source1:	test_mozmill-run
Source2:	prepare.sh
Source3:	ManifestDestiny-0.2.3.tar.gz
Source4:	mozrunner-2.5.3.tar.gz
Source5:	jsbridge-2.4.2.tar.gz
Source6:	mozmill-1.5.2.tar.gz
Source7:	qa_test_mozmill.8.gz
Source8:	test_mozmill-ctcs2-run
Source9:	chkmozmillresult
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Provides:	qa_mozmill
Obsoletes:	qa_mozmill
Requires:	python >= 2.6 python-setuptools firefox ctcs2
BuildArch:	noarch

%description
MozMill is a test tool and framework for writing automated tests for Gecko based applications (Firefox etc). 
It is built as a command line client tools to help users write, run, and debug tests.

Authors:
--------
	Arthur Guo <aguo@novell.com>
%prep
%setup -q -n %{name}

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8/
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/%name
cp %{S:3} $RPM_BUILD_ROOT/usr/share/qa/%name
cp %{S:4} $RPM_BUILD_ROOT/usr/share/qa/%name
cp %{S:5} $RPM_BUILD_ROOT/usr/share/qa/%name
cp %{S:6} $RPM_BUILD_ROOT/usr/share/qa/%name
cp %{S:7} $RPM_BUILD_ROOT/usr/share/man/man8/
cp %{S:8} $RPM_BUILD_ROOT/usr/share/qa/%name
cp %{S:9} $RPM_BUILD_ROOT/usr/share/qa/%name
cp -ap * $RPM_BUILD_ROOT/usr/share/qa/%name
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name CVS -exec rm -rf {} \;

%post
echo
echo "NOTICE: \n implement \"/usr/share/qa/qa_test_mozmill/prepare.sh\" \nbefore running MozMill test."

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)   
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/%name/tcf
/usr/share/man/man8/qa_test_mozmill.8.gz

%changelog
* Thu Mar 25 2011 - aguo@novell.com
- Integrate MozMill with ctcs2
- Provide two options for test: ctcs2/non-ctcs2, add parser for non-ctcs2 mode.
* Thu Mar 04 2011 - aguo@novell.com
- Add python egg of mozmill and dependent eggs.
* Thu Mar 03 2011 - aguo@novell.com
- Update test cases.
* Wed Mar 02 2011 - aguo@novell.com
- Initiate this package.
