#
# spec file for package qa_testset_kernel (Version 1.0)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_testset_kernel
License:        GPL v2 or later
Group:          testset
AutoReqProv:    on
Version:        1.0
Release:        0
Summary:        Setup for Kernel tests running
Source0:        testset_kernel-run
Source1:	install.sh
Source2:	test_run.sh
Source3:	kernel_test_packages
Source4:	regression_test_packages
Source5:	run.sh
Source6:	validation.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
testset_kernel-run is a script to launch a serials of tests related kernel testing.


Authors:
--------
    Liang Zheng <lzheng@suse.com>

%prep
#%setup -q


%build

%install
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/%{name}
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 %{S:0} $RPM_BUILD_ROOT/usr/share/qa/tools/
install -m 744 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 744 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 744 %{S:5} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 744 %{S:6} $RPM_BUILD_ROOT/usr/share/qa/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/qa
/usr/share/qa/tools

%changelog
* Fri Jan 17 2014 cachen@suse.de
- initial package
