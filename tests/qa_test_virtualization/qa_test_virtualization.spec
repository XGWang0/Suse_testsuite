#
# spec file for package qa_samba (Version 0.1)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_virtualization
License:        GPL v2 or later
Group:          SuSE internal
Summary:        (rd-)qa virtualization automated tests
Provides:	qa_virtualization
Obsoletes:	qa_virtualization
Requires:       virtautolib bridge-utils tftp dhcp-server syslinux bind apache2 awk ctcs2 qa_tools libqainternal wget
BuildRequires:  ctcs2 virtautolib-data
AutoReqProv:    on
Version:        0.1.5
Release:        1
Source0:        %name.tar.bz2
Source1:        generate.tar.bz2
Source2:        tools.tar.bz2
Source3:	qa_test_virtualization.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch  

%description
Test cases for virtualization

Authors:
--------
    Lukas Lipavsky <llipavsky@suse.cz>

%prep
%setup -n %{name} -a1 -a2

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}

# 1. generate testcases
generate/_generate_install.sh -d /usr/share/qa/virtautolib/data/autoinstallation
#./_generate_install.sh -d /usr/share/qa/virtautolib/data/autoinstallation -t "tap:aio"
#./_generate_install.sh -d /usr/share/qa/virtautolib/data/autoinstallation -t "tap:qcow2"

# 2. generate tcfs
generate/_generate_tcf.sh standalone > $RPM_BUILD_ROOT/usr/share/qa/%name/tcf/qa_virtualization-standalone.tcf
generate/_generate_tcf.sh network > $RPM_BUILD_ROOT/usr/share/qa/%name/tcf/qa_virtualization-network.tcf

generate/_generate_sles10sp4supported_tcf.sh standalone > $RPM_BUILD_ROOT/usr/share/qa/%name/tcf/qa_virtualization-sles10sp4supported-standalone.tcf
generate/_generate_sles10sp4supported_tcf.sh network > $RPM_BUILD_ROOT/usr/share/qa/%name/tcf/qa_virtualization-sles10sp4supported-network.tcf

generate/_generate_sles11sp1supported_tcf.sh standalone > $RPM_BUILD_ROOT/usr/share/qa/%name/tcf/qa_virtualization-sles11sp1supported-standalone.tcf
generate/_generate_sles11sp1supported_tcf.sh network > $RPM_BUILD_ROOT/usr/share/qa/%name/tcf/qa_virtualization-sles11sp1supported-network.tcf

cp tools/* $RPM_BUILD_ROOT/usr/share/qa/tools
rm -fr tools generate _install.template

cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name

for tcf in `cd $RPM_BUILD_ROOT/usr/share/qa/%name/tcf  ; ls` ; do
	ln -s ../%name/tcf/$tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_virtualization.8.gz
/usr/share/qa

%changelog
