#
# spec file for package qa_cracklib (Version 1.1)
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_cracklib
License:        GNU General Public License (GPL)
Group:          SuSE internal
Summary:        Simple cracklib tests for ctcs framework
Provides:	qa_cracklib
Obsoletes:	qa_cracklib
Requires:       cracklib expect ctcs2
Version:        1.1.1
Release:        49
Source0:        %name-%version.tar.bz2
Source1:        qa_cracklib.tcf
Source2:        test_cracklib-run
Source3:        qa_test_cracklib.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Test cases for cracklib package. Tests short and trivial passwords.

%prep
%setup -q -n %{name}

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8/
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/qa_cracklib.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name CVS -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_cracklib.8.gz
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/qa_cracklib.tcf
/usr/share/qa/tools/test_cracklib-run

%changelog -n qa_test_cracklib
* Tue Feb 06 2007 - ro@suse.de
- added qa_dummy as buildreq
* Mon Feb 05 2007 - mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Feb 05 2007 - llipavsky@suse.cz
- fixed build requirenments
* Thu Feb 01 2007 - llipavsky@suse.cz
- fixed incorrect path in one sorce
* Tue Jan 23 2007 - llipavsky@suse.cz
- submit for more dists.
* Thu Jul 13 2006 - llipavsky@suse.cz
- added correct BuildRequires tag
* Wed Jul 12 2006 - llipavsky@suse.cz
- fixed to comply QA Packaging Guidelines
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Aug 19 2005 - kmachalkova@suse.cz
- package created, version 1.1
