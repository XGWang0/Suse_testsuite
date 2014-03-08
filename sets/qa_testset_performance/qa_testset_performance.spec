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

Name:           qa_testset_performance
License:        GPL v2 or later
Group:          testset
AutoReqProv:    on
Version:        1.0
Release:        0
Summary:        Setup for performance tests running
Source0:        testset_performance-run
Source1:        sq-set.sh
Source2:        sq-mach.sh
Source3:        sq-control.sh
Source4:        sq-execute.sh
Source5:        sq-util.sh
Source6:        sq-global.sh
Source7:        sq-fake.sh
Source8:        performance.set
Source9:        README.md
Source1101:     SLE11SP3.conf
Source1102:     SLE11SP3.list
Source1201:     SLE12.conf
Source1202:     SLE12.list
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
testset_performance-run is a script to launch a serials of tests related perforamnce benchmarks testing.


Authors:
--------
    Lance Wang <lzwang@suse.com>

%prep

%build

%install
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 744 %{S:0} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 744 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 744 %{S:7} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 644 %{S:5} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 644 %{S:6} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 644 %{S:7} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 644 %{S:8} $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 644 %{S:9} $RPM_BUILD_ROOT/usr/share/qa/%{name}
%if %suse_version < 1315
    sed -i '/^TARGET_RELEASE=$/s/TARGET_RELEASE=/TARGET_RELEASE=SLE11SP3/' $RPM_BUILD_ROOT/usr/share/qa/%{name}/testset_performance-run
    install -m 644 %{S:1101} $RPM_BUILD_ROOT/usr/share/qa/%{name}
    install -m 644 %{S:1102} $RPM_BUILD_ROOT/usr/share/qa/%{name}
%endif
%if %suse_version == 1315
    sed -i '/^TARGET_RELEASE=$/s/TARGET_RELEASE=/TARGET_RELEASE=SLE12/' $RPM_BUILD_ROOT/usr/share/qa/%{name}/testset_performance-run
    install -m 644 %{S:1201} $RPM_BUILD_ROOT/usr/share/qa/%{name}
    install -m 644 %{S:1202} $RPM_BUILD_ROOT/usr/share/qa/%{name}
    mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system
    mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system/multi-user.target.wants
cat <<EOF > $RPM_BUILD_ROOT/usr/lib/systemd/system/sqperf.service
[Unit]
Description=testset_performance-run
ConditionFileIsExecutable=/usr/share/qa/tools/testset_performance-run
After=getty.target

[Service]
Type=idle
ExecStart=/usr/share/qa/tools/testset_performance-run
TimeoutSec=0
RemainAfterExit=yes

[Install]
Alias=sqperf

EOF
   chmod 644 $RPM_BUILD_ROOT/usr/lib/systemd/system/sqperf.service
   ln -sf ../sqperf.service $RPM_BUILD_ROOT/usr/lib/systemd/system/multi-user.target.wants/sqperf.service
%endif
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
ln -s ../%{name}/testset_performance-run $RPM_BUILD_ROOT/usr/share/qa/tools/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/qa
/usr/share/qa/%{name}
/usr/share/qa/tools
%if %suse_version == 1315
/usr/lib/systemd/system
/usr/lib/systemd/system/sqperf.service
/usr/lib/systemd/system/multi-user.target.wants/sqperf.service
%endif

%changelog
* Fri Jan 17 2014 cachen@suse.de
- initial package
