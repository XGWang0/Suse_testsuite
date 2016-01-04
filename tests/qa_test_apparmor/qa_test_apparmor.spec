#!BuildIgnore: post-build-checks

# spec file for package qa_apparmor (Version 1325)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
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
Name:           qa_test_apparmor
%if 0%{?suse_version} >= 1315
Version:        2.8.2
%else
Version:        2.5.1
%endif
Release:        1
Summary:        apparmor tests
License:        GPL v2
Group:          System/Packages
AutoReqProv:    on
Source0:        apparmor-%{version}.tar.bz2
Source1:        qa_apparmor-%{version}.tcf
Source2:        test_apparmor-run
Source3:        qa_test_apparmor.8
Source4:        wrapper.sh
Patch0:         bin_include-path-%{version}.patch
%if "%{version}" == "2.8.2"
Patch1:         mount-2.8.2.patch
Patch2:         exec_ptrace_regex-2.8.2.patch
%else %if "%{version}" == "2.5.1"
Patch1:         backport-2.5.1.patch
%endif
Url:            http://www.novell.com/products/apparmor/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	qa_apparmor
Obsoletes:	qa_apparmor
Requires:       apparmor-parser apparmor-profiles libapparmor perl bison swig flex ruby qa_lib_ctcs2
BuildRequires:  apparmor-parser bzip2 gcc libapparmor-devel swig flex bison automake autoconf libtool


%description
This package contains different types of tests:
- regression tests for apparmor_parser
- regression tests for the kernel module
- stress tests
- parser tests

%prep
%define qa_dir usr/share/qa
%setup -q -n apparmor-%{version}
%patch0 -p1
%if "%{version}" == "2.8.2"
%patch1 -p1
%patch2 -p1
%else %if "%{version}" == "2.5.1"
%patch1 -p1
%endif


%build
# regression
%if 0%{?suse_version} >= 1315
make -C tests/regression/apparmor
%else
make -C tests/regression/subdomain
%endif
# stress
# TODO: subdomain testing scripts need patching
make -C tests/stress/subdomain
# Remove source code files
find -name '*.c' -exec rm {} \; -o -name '*.h' -exec rm {} \;


%install
find -type f -name '*.sh' -exec chmod +x {} \;
# scripts
install -d -m 0755 $RPM_BUILD_ROOT/%{qa_dir}/tools
install -d -m 0755 $RPM_BUILD_ROOT/%{qa_dir}/%{name}
cp -ar * $RPM_BUILD_ROOT/%{qa_dir}/%{name}/
install -m 0755 %{SOURCE4} $RPM_BUILD_ROOT/%{qa_dir}/%{name}/
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/%{qa_dir}/tools/
# man page
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
# tcf files
install -d -m 0755 $RPM_BUILD_ROOT/%{qa_dir}/tcf
install -d -m 0755 $RPM_BUILD_ROOT/%{qa_dir}/%{name}/tcf
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{qa_dir}/%{name}/tcf
mv $RPM_BUILD_ROOT/%{qa_dir}/%{name}/tcf/qa_apparmor-%{version}.tcf $RPM_BUILD_ROOT/%{qa_dir}/%{name}/tcf/qa_apparmor.tcf
ln -s ../%{name}/tcf/qa_apparmor.tcf $RPM_BUILD_ROOT/%{qa_dir}/tcf/qa_apparmor.tcf


%clean
rm -rvf $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
# man page
/usr/share/man/man8/qa_test_apparmor.8.gz
# scripts
%dir /usr/share/qa
/usr/share/qa/%{name}
%dir /usr/share/qa/tools
/usr/share/qa/tools/test_apparmor-run
# tcf file
%dir /usr/share/qa/tcf
/usr/share/qa/tcf/qa_apparmor.tcf


%changelog
* Wed Aug 10 2011 - llipavsky@suse.cz
- Package rename: qa_apparmor -> qa_test_apparmor
