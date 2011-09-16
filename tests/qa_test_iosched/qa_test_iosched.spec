#
# spec file for package qa_iosched_test (Version 0.1)
#
# Copyright (c) 2006 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_iosched
BuildRequires:  ctcs2
License:        Unknown
Group:          SuSE internal
Autoreqprov:    on
Version:        0.1
Release:        1
Summary:        rd-qa-kernel internal package to test behaviour of available ioschedulers
Url:            http://w3.suse.de/~fseidel/
Source:         %{name}-%{version}.tar.bz2
Source1:	qa_test_iosched.8
Source2:	test_iosched-run
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	qa_iosched_test
Obsoletes:	qa_iosched_test
Requires:       ctcs2 tiobench
BuildArchitectures: noarch
#ExclusiveArch: %ix86

%description
Tries small benchmark on all available ioschedulers for the device.



Authors:
--------
    Frank Seidel <fseidel@suse.de>

%prep
%setup -n %{name}

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d -v $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
install -m 755 -d -v $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/tcf
cp -v iosched_testing.sh $RPM_BUILD_ROOT/usr/share/qa/%{name}/
cp -v qa_iosched_test.tcf $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf/
ln -sf ../%{name}/tcf/qa_iosched_test.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/qa_iosched_test.tcf
ln -sf ../../../share/qa/%{name}/tcf/qa_iosched_test.tcf  $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf/qa_iosched_test.tcf
cp -v %{S:2} $RPM_BUILD_ROOT/usr/lib/ctcs2/tools/

%clean
rm -rvf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_iosched.8.gz
/usr/lib/ctcs2/tools/test_iosched-run
/usr/lib/ctcs2/tcf/qa_iosched_test.tcf
/usr/share/qa
/usr/share/qa/qa_test_iosched
/usr/share/qa/tcf/qa_iosched_test.tcf

%changelog -n qa_test_iosched
* Wed Feb 15 2006 - fseidel@suse.de
- initial release
