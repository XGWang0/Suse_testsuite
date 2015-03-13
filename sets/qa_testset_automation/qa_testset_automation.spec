#
# spec file for package qa_testset_performance (Version 1.0)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_testset_automation
License:        GPL v2 or later
Group:          testset
AutoReqProv:    on
Version:        1.0
Release:        0
Summary:        A test Framework for QA ACAPII
Source0:        automation-%{version}.tar.bz2
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
qa_testset_automation is a collection of tools.

Authors:
--------
    Lance Wang <lzwang@suse.com>

%prep
%setup -n automation

%build

%install
%if %suse_version == 1110
SLE_RELEASE=SLE11
%elseif %suse_version == 1315
SLE_RELEASE=SLE12
%endif
pushd qaset
make TARGET_RELEASE=${SLE_RELEASE} DEST=$RPM_BUILD_ROOT install
popd qaset
#tar xf stat.tar.xz

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%if %suse_version == 1110
/etc/init.d/qaset
%elseif %suse_version == 1315
/usr/lib/systemd/system/multi-user.target.wants
/usr/lib/systemd/system/qaperf.service
%endif
/usr/share/qa
/usr/share/qa/qaset

%changelog
* Fri Jan 17 2014 cachen@suse.de
- initial package
