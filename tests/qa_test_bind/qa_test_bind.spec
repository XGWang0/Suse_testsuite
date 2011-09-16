#
# spec file for package qa_bind (Version 0.221)
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_bind
BuildRequires:  ctcs2
License:        GPL v2 or later
Group:          SuSE internal
Summary:        Simple bind tests for ctcs framework
Provides:	qa_bind
Obsoletes:	qa_bind
Requires:       bind bind-utils ctcs2 grep
Version:        0.222
Release:        1
Source0:        %name-%version.tar.bz2
Source1:        qa_bind.tcf
Source2:        test_bind-run
Source3:        qa_test_bind.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Test cases for bind DNS server testing

* start and restart of the service

* primary DNS function

* secondary DNS function

* DNS forwarding



Authors:
--------
    QA team <qa@suse.de>

%prep
%setup -q -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8/
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
ln -s ../%name/tcf/qa_bind.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d \( -name CVS -or -name .svn \) -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%dir /usr/share/qa
/usr/share/qa/%name
%dir /usr/share/qa/tools
/usr/share/qa/tools/test_bind-run
%dir /usr/share/qa/tcf
/usr/share/qa/tcf/qa_bind.tcf
/usr/share/man/man8/qa_test_bind.8.gz

%changelog
* Wed Aug 17 2011 - llipavsky@suse.cz
- Remove qa_dummy dependency
* Wed Aug 10 2011 - llipavsky@suse.cz
- Package rename: qa_bind -> qa_test_bind
* Fri Jul 27 2007 - rommel@suse.de
- updated to minor version 221 (renamed directories, reworked test scripts)
* Wed Apr 19 2006 - mmrazik@suse.cz
- "QA Packaging Guidelines" conformation added
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Dec 21 2005 - kmachalkova@suse.cz
- added ctcs2 support (tcf files, test_bind-run script etc.)
* Tue Aug 16 2005 - kmachalkova@suse.cz
- package created, version 1.1
