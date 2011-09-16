#
# spec file for package qa_gnutls (Version 0.1)
#
# Copyright (c) 2010 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_gnutls
License:        GNU General Public License (GPL)
Group:          SuSE internal
Summary:        Tests for the gnutls package, prepared to run under the ctcs framework
Provides:	qa_gnutls
Obsoletes:	qa_gnutls
Requires:       gnutls ctcs2
BuildRequires:  ctcs2
Version:        0.2
Release:        1.1
Source0:        %name-%version.tar.bz2
Source1:        qa_gnutls.tcf
Source2:        test_gnutls-run
Source3:        qa_test_gnutls.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Test cases for the gnutls package.

The following command line utilities are tested:
gnutls-cli, gnutls-cli-debug, gnutls-serv, certtool, srptool

Implements TESTOPIA testcases 233364 - 233369 (as of 2010)


%prep
%setup -q -n qa_test_gnutls

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
ln -s ../%name/tcf/qa_gnutls.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_gnutls.8.gz
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/qa_gnutls.tcf
/usr/share/qa/tools/test_gnutls-run

%changelog
* Wed Aug 17 2011 - llipavsky@suse.cz
- Remove qa_dummy dependency
* Thu Aug 11 2011 - llipavsky@suse.cz
- Package rename: qa_gnutls -> qa_test_gnutls
* Thu Oct  7 2010 kgw@suse.de
- package created, version 0.2
