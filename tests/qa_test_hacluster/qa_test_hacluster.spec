#
# spec file for package qa_sample (Version 0.1)
#
# Copyright (c) 2010 Novell, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugzilla.novell.com/
#

# norootforbuild

Name:           qa_test_hacluster
#BuildRequires:  ctcs2
License:        SUSE Proprietary
Group:          SuSE internal
AutoReqProv:    on
Version:        0.4.1
Release:        1
Summary:        (rd-)qa internal package for HA setup
Url:            http://qa.suse.de/
Source0:        %name-%version.tar.bz2
Source1:        qa_hacluster.tcf
Source2:        test_hacluster-run
Source3:        qa_test_hacluster.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Provides:	qa_hacluster
Obsoletes:	qa_hacluster
Requires:       ctcs2

%description
This is a package that contains scripts for HA cluster setup.

Authors:
--------
    Vit Pelcak <vpelcak@novell.com>

%prep
%setup -q -n %{name}

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/qa_hacluster.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_hacluster.8.gz
/usr/share/qa
/usr/share/qa/tcf
/usr/share/qa/tools
/usr/share/qa/%name
/usr/share/qa/tcf/qa_hacluster.tcf
/usr/share/qa/tools/test_hacluster-run

%changelog
* Fri Jan 13 2012 - vpelcak@suse.com
- Added Apache + MySQL deployment

* Fri Dec 03 2010 - vpelcak@novell.com
- Finished cLVM, initial work on CTDB

* Tue Nov 30 2010 - vpelcak@novell.com
- Initial cLVM test support

* Wed Nov 10 2010 - vpelcak@novell.com
- Initial CTS setup integration

* Thu Nov 04 2010 - vpelcak@novell.com
- added automation of testplan 2841

* Tue Nov 02 2010 - vpelcak@novell.com
- improved and debugged node and ocfs2 configuration

* Tue Oct 25 2010 - vpelcak@novell.com
- support for ocfs2 automated configuration and multimachine support fixes

* Mon Oct 25 2010 - vpelcak@novell.com
- start of adaptation to multimachine support

* Tue Oct 19 2010 - vpelcak@novell.com
- SBD primitive configuration added

* Tue Oct 12 2010 - vpelcak@novell.com
- Created initial package for setup of HA cluster
