#
# spec file for package qa_test_openldap2
#
# Copyright (c) 2015 SUSE LINUX GmbH, Nuernberg, Germany.
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


%define __os_install_post %{nil}
%if 0%{?suse_version} >= 1315
%define ver 2.Xgit_a18d4c97638e
%define system sle12
%endif
%if 0%{?suse_version} == 1110
%define ver 2.4.20
%define system sle11
%endif
%if 0%{?suse_version} == 1010
%define ver 2.3.32
%define system sle10sp3
%endif
%if 0%{?suse_version} == 910
%define ver 2.2.24
%define system sle9sp4
%endif
Name:           qa_test_openldap2
Version:        %{ver}
Release:        0
Summary:        openldap2 tests for ctcs framework
License:        OpenLDAP Public License
Group:          SuSE internal
Source0:        %{name}-%{version}.tar.bz2
Source1:        qa_openldap2-%{system}.tcf
Source2:        test_openldap2-run
Source3:        qa_test_openldap2.8
BuildRequires:  ctcs2
Requires:       ctcs2
Requires:       grep
Requires:       openldap2
Requires:       openldap2-client
Provides:       qa_openldap2
Obsoletes:      qa_openldap2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Test cases for openldap2 server testing

%prep
%setup -q -n qa_openldap2

%build
%if 0%{?suse_version} >= 1315
# Since we are using parts of build enviroment which was configured for
# x86_64, we need to replace x86_64 specific things with appropriate ones
# for other architectures.
%ifarch ppc64le
find ./ -type f -exec sed -i "s|x86_64|powerpc64le|g" {} +
find ./ -type f -exec sed -i "s|stubs-64.h|stubs-64-v2.h|g" {} +
%else
find ./ -type f -exec sed -i "s|x86_64|%{_arch}|g" {} +
%endif
make %{?_smp_mflags} V=1 -C '%{_builddir}/qa_openldap2/libraries'
make %{?_smp_mflags} V=1 -C '%{_builddir}/qa_openldap2/tests/progs'
%endif


%install
install -m 755 -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE3} %{buildroot}%{_mandir}/man8
gzip %{buildroot}%{_mandir}/man8/%{name}.8
install -m 755 -d %{buildroot}%{_datadir}/qa/%{name}/tcf
install -m 755 -d %{buildroot}%{_datadir}/qa/tcf
install -m 755 -d %{buildroot}%{_datadir}/qa/tools
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/qa/%{name}/tcf/qa_openldap2.tcf
ln -s ../%{name}/tcf/qa_openldap2.tcf %{buildroot}%{_datadir}/qa/tcf/
install -m 755 %{SOURCE2} %{buildroot}%{_datadir}/qa/tools
%if 0%{?suse_version} >= 1315
make install-tests DESTDIR=%{buildroot}%{_datadir}/qa/%{name}
%else cp -a * %{buildroot}%{_datadir}/qa/%{name}
%endif

%files
%defattr(-, root, root)
%{_mandir}/man8/qa_test_openldap2.8.gz
%dir %{_datadir}/qa
%{_datadir}/qa/%{name}
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_openldap2-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_openldap2.tcf

%changelog
