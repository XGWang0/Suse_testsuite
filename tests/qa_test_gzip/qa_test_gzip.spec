#
# spec file for package qa_gzip (Version 0.1)
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_gzip
License:        GNU General Public License (GPL)
Group:          SuSE internal
Summary:        Simple gzip tests for ctcs framework
Provides:	qa_gzip
Obsoletes:	qa_gzip
Requires:       gzip ctcs2
BuildRequires:  ctcs2
Version:        0.1
Release:        48
Source0:        %name-%version.tar.bz2
Source1:        qa_gzip.tcf
Source2:        test_gzip-run
Source3:        qa_test_gzip.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Test cases for gzip package. Test archive creation and uncompression



%prep
%setup -q -n %{name}

%build

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
ln -s ../%name/tcf/qa_gzip.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name CVS -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/qa_gzip.tcf
/usr/share/qa/tools/test_gzip-run
/usr/share/man/man8/qa_test_gzip.8.gz

%changelog -n qa_test_gzip
* Tue Aug  9 13:24:36 GMT 2011 - llipavsky@suse.cz
- Package rename: qa_gzip -> qa_test_gzip
* Tue Mar 15 2011 - aguo@novell.com
- add man page document
* Tue Jan 23 2007 - llipavsky@suse.cz
- fix in spec file
* Tue Jan 23 2007 - llipavsky@suse.cz
- submitting to other products (not only stable)
* Fri Sep 29 2006 - llipavsky@suse.cz
- fized Bug 208191 - /usr/share/qa/tools/test_gzip-run does not work
* Thu Jul 13 2006 - llipavsky@suse.cz
- added correct BuildRequires tag
* Wed Jul 12 2006 - llipavsky@suse.cz
- fixed to comply QA Packaging Guidelines
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Jan 20 2006 - kmachalkova@suse.cz
- package created, version 0.1
