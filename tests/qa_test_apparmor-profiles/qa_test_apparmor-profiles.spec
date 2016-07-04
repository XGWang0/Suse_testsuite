#!BuildIgnore: post-build-checks

# spec file for package qa_apparmor-profiles (Version 1)
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
Name:           qa_test_apparmor-profiles
Version:        1
Release:        1
Summary:        apparmor profile tests
License:        GPL v2
Provides:	qa_apparmor-profiles
Obsoletes:	qa_apparmor-profiles
Group:          System/Packages
Requires:       apparmor-parser apparmor-profiles qa_lib_ctcs2 qa_test_ltp apache2
BuildRequires:  apparmor-parser bzip2 gcc libapparmor-devel swig flex bison automake autoconf libtool
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         %{name}-%{version}.tar.bz2
Source1:        qa_apparmor_profiles.tcf
Source2:        qa_test_apparmor-profiles.8
Source3:        test_apparmor_profiles-run


%description
This package contains tcf files for apparmor profile testing.

Currently the following profiles are tested:
- tcp commands:ping
- tcp commands:traceroute
- apache


%prep
%setup


%install
%define qa_dir usr/share/qa
%define man_dir usr/share/man/
# test scripts
install -m 755 -d $RPM_BUILD_ROOT/%{qa_dir}
install -m 755 -d $RPM_BUILD_ROOT/%{qa_dir}/%{name}
cp -ar * $RPM_BUILD_ROOT/%{qa_dir}/%{name}
# man page
install -m 755 -d $RPM_BUILD_ROOT/%{man_dir}/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/%{man_dir}/man8
gzip $RPM_BUILD_ROOT/%{man_dir}/man8/%{name}.8
# tcf file
install -d -m 0755 $RPM_BUILD_ROOT/%{qa_dir}/tcf
install -d -m 0755 $RPM_BUILD_ROOT/%{qa_dir}/%{name}/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/%{qa_dir}/%{name}/tcf/
ln -s ../%{name}/tcf/qa_apparmor_profiles.tcf $RPM_BUILD_ROOT/%{qa_dir}/tcf/qa_apparmor_profiles.tcf
# run file
install -d -m 0755 $RPM_BUILD_ROOT/%{qa_dir}/tools
install -m 0755 %{S:3} $RPM_BUILD_ROOT/usr/share/qa/tools


%clean
rm -rvf $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
%dir /%{qa_dir}
/%{qa_dir}/%{name}
%dir /%{qa_dir}/tcf
/%{qa_dir}/tcf/qa_apparmor_profiles.tcf
%dir /%{qa_dir}/tools
/%{qa_dir}/tools/test_apparmor_profiles-run
%dir /%{man_dir}/man8
/%{man_dir}/man8/%{name}.8.gz


%changelog
* Mon Jul 04 2016 - jtzhao@suse.com
- Add apache2 to dependencies
* Tue Dec 29 2015 - jtzhao@suse.com
- Separate qa_test_apparmor-profiles from qa_test_apparmor
