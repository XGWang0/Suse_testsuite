#
# spec file for package qa_clamav (Version 0.6)
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


Name:           qa_test_clamav
#BuildRequires:  ctcs2 
License:        SUSE Proprietary
Group:          SUSE internal
AutoReqProv:    on
Version:        0.6
Release:        1
Summary:        (rd-)qa internal package for testing clamav
Url:            http://www.clamav.net/
Source0:        %name-%version.tar.bz2
Source1:        qa_clamav.tcf
Source2:        test_clamav-run
Source3:        README
Source4:	qa_test_clamav.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	qa_clamav
Obsoletes:	qa_clamav
Requires:       ctcs2 clamav
BuildArch:      noarch
#ExclusiveArch: %ix86

%description
test suite for clamav and freshclam testing



Authors:
--------
    Andrej Semen asemen@suse.de

%prep
%setup -q -n %{name}

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:3} $RPM_BUILD_ROOT/usr/share/qa/%name/
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/qa_clamav.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755,root,root)
/usr/share/man/man8/qa_test_clamav.8.gz
/usr/share/qa/
/usr/share/qa/%name
/usr/share/qa/%name/README
/usr/share/qa/tcf/qa_clamav.tcf
/usr/share/qa/tools/test_clamav-run

%changelog
* Wed Aug 10 2011 - llipavsky@suse.cz
- Package rename: qa_clamav -> qa_test_clamav
* Thu Apr 23 2009 asemen@suse.de
- correction in tcf file of output script name to qa_clamdscan_file_scan_eicarcom2.zip.sh
* Fri Dec 12 2008 asemen@suse.de
- fix fail of initial installed clamav if no clamav db is present
* Fri Nov 21 2008 asemen@suse.de
- fix restart and start problem of clamd and freshclam
* Fri Nov 21 2008 asemen@suse.de
- fix #447091 clamd_start
- fix #447087 changing to noarch
- Add of README
* Thu Nov 20 2008 asemen@suse.de
- building fail on sles9 fixed
- filescan tests for clamscan and clamdsacn in seperate files
- add environment checks of start and stop of clamd and freshclam
- add 2nd freshclam update test (no db files)
* Fri Nov 14 2008 asemen@suse.de
- package created, version 0.1
