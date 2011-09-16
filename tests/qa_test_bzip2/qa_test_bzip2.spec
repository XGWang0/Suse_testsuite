#
# spec file for package qa_bzip2 (Version 0.1)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_bzip2
License:        GPL v2 or later
Group:          SuSE internal
AutoReqProv:    on
Version:        0.2
Release:        1
Summary:        (rd-)qa internal package for testing bzip2
Url:            http://w3.suse.de/~fseidel/
Source0:        %name-%version.tar.bz2
Source1:        qa_bzip2.tcf
Source2:        test_bzip2-run
Source3:	    qa_test_bzip2.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	qa_bzip2
Obsoletes:	qa_bzip2
Requires:       bzip2 gcc ctcs2 libbz2-devel

%description
this is the first rd-qa internal package following the new rd-qa
internal policies and may be taken as a template for other similar ones

Authors:
--------
    Frank Seidel <fseidel@suse.de>

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
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/qa_bzip2.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name CVS -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)   
/usr/share/man/man8/qa_test_bzip2.8.gz
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/qa_bzip2.tcf
/usr/share/qa/tools/test_bzip2-run

%changelog
* Wed Aug 10 2011 - llipavsky@suse.cz
- Package rename: qa_bzip2 -> qa_test_bzip2
* Thu Jan 17 2008 mmrazik@suse.cz
- libbz2-devel added to Requires (needed by compile test)
* Wed Jan 09 2008 mmrazik@suse.cz
- tests failing due to incorrect path [#245775]
* Tue Jan 23 2007 llipavsky@suse.cz
- converted to new qa package standard
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Nov 07 2005 fseidel@suse.de
- specfile changed according to new ctcs2
* Fri Oct 14 2005 fseidel@suse.de
- minor specfile bugfix
* Thu Oct 13 2005 fseidel@suse.de
- bugfix for ctcs2 runfile and docu-update
* Wed Oct 12 2005 ro@suse.de
- minor specfile cleanup
* Thu Oct 06 2005 fseidel@suse.de
- initial release
