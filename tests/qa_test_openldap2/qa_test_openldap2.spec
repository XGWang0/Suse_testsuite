# Copyright (c) 2010 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild
#!BuildIgnore: post-build-checks

%if %{suse_version} >= 1110
%define ver 2.4.20
%define system sle11
%endif

%if %{suse_version} == 1010
%define ver 2.3.32
%define system sle10sp3
%endif

%if %{suse_version} == 910
%define ver 2.2.24
%define system sle9sp4
%endif

Name:           qa_test_openldap2
BuildRequires:  ctcs2
License:        OpenLDAP Public License
Group:          SuSE internal
Summary:        openldap2 tests for ctcs framework
Provides:	qa_openldap2
Obsoletes:	qa_openldap2
Requires:       openldap2 openldap2-client ctcs2 grep
Version:        %{ver}
Release:        1
Source0:        %name-%version.tar.bz2
Source1:        qa_openldap2-%{system}.tcf
Source2:        test_openldap2-run
Source3:        qa_test_openldap2.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch: 	noarch

%define __os_install_post %{nil}
%description
Test cases for openldap2 server testing

Authors:
--------
    The OpenLDAP Project <project@openldap.org>

%prep
%setup -q -n qa_openldap2

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf/qa_openldap2.tcf
ln -s ../%name/tcf/qa_openldap2.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_openldap2.8.gz
%dir /usr/share/qa
/usr/share/qa/%name
%dir /usr/share/qa/tools
/usr/share/qa/tools/test_openldap2-run
%dir /usr/share/qa/tcf
/usr/share/qa/tcf/qa_openldap2.tcf

%changelog
* Wed Aug 17 2011 - llipavsky@suse.cz
- Remove qa_dummy dependency
* Fri Aug 12 2011 - llipavsky@suse.cz
- Package rename: qa_openldap2 -> qa_test_openldap2
* Thu Aug 12 2010 - nfriedrich@suse.cz
- package created, version 1.1
