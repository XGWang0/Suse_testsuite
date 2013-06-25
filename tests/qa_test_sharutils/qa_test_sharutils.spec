#
# spec file for package qa_sharutils (Version 4.6.2)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_sharutils
License:        GPL v2 or later
Group:          SuSE internal
#This is ugly hack, to make build satisfied 
#It complains about missing libc, since there are some binary data in test directory
Autoreqprov:    off
Summary:        Simple sharutils test for ctcs framework
Provides:	qa_sharutils
Obsoletes:	qa_sharutils
Requires:       sharutils ctcs2
Version:        4.6.2
Release:        1
Source0:        sharutils-%version.tar.bz2
Source1:        qa_sharutils.tcf
Source2:        test_sharutils-run
Source3:        upstream_wrapper.sh
Source4:        qa_test_sharutils.8
Patch0:         %name-%version-paths.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Test case for sharutils package.

Tests from sharutils package (source code) included as well as one
custom testcase for uuencode/decode.



%prep
%setup -q -n sharutils
%patch0 
%define qa_location /usr/share/qa/%name

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/%{qa_location}
cp -a * $RPM_BUILD_ROOT/%{qa_location}
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tools
#
#copy the helper script
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 0755 %{SOURCE3} $RPM_BUILD_ROOT/%{qa_location}
#
#
cp %{SOURCE1} $RPM_BUILD_ROOT/%{qa_location}/tcf
ln -s ../%name/tcf/qa_sharutils.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_sharutils.8.gz
%{qa_location}
/usr/share/qa
/usr/share/qa/tcf/qa_sharutils.tcf
/usr/share/qa/tools/test_sharutils-run

%changelog -n qa_test_sharutils
* Tue Jul 25 2006 - mmrazik@suse.cz
- added tests from the upstram source-code package
- fixed the package to conform QA Packaging Guidelines
- minor fix of the custom test included previously
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Sep 01 2005 - kmachalkova@suse.cz
- Package created, version 1.1
