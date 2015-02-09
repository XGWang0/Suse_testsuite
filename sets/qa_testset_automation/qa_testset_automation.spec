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
Summary:        A test Framework for QCAPII
Source0:        qaset-%{version}.tar.bz2
#Source501:      stat.tar.xz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
qa_testset_automation is a framework to launch a serial of tests.
All of the tests run in the same system.


Authors:
--------
    Lance Wang <lzwang@suse.com>

%prep
%setup -n qaset-%{version}

%build

%install
%if %suse_version == 1110
SLE_RELEASE=SLE11
%elseif %suse_version == 1315
SLE_RELEASE=SLE12
%endif
make TARGET_RELEASE=${SLE_RELEASE} DEST=$RPM_BUILD_ROOT install

#%post
#%if %suse_version < 1315
#ln -s ../qaset /etc/init.d/rc5.d/S99qaset
#%endif

#cd /usr/share/qa/%{name}
#tar xf stat.tar.xz

#%preun
#cd /usr/share/qa/%{name}
#rm -rf stat

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
