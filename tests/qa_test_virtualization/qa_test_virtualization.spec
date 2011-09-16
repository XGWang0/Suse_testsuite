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
BuildRequires:  ctcs2
AutoReqProv:    on
Version:        0.1.4
Release:        1
Source0:        %name-%version.tar.bz2
Source1:        qa_virtualization-standalone.tcf
Source2:        test_virtualization-standalone-run
Source3:        qa_virtualization-network.tcf
Source4:        test_virtualization-network-run
Source5:        qa_virtualization-sles10sp4supported-standalone.tcf
Source6:        test_virtualization-sles10sp4supported-standalone-run
Source7:        qa_virtualization-sles10sp4supported-network.tcf
Source8:        test_virtualization-sles10sp4supported-network-run
Source9:        qa_virtualization-sles11sp1supported-standalone.tcf
Source10:        test_virtualization-sles11sp1supported-standalone-run
Source11:        qa_virtualization-sles11sp1supported-network.tcf
Source12:        test_virtualization-sles11sp1supported-network-run
Source13:	qa_test_virtualization.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch  

%description
Test cases for virtualization

Authors:
--------
    Lukas Lipavsky <llipavsky@suse.cz>

%prep
%setup -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:13} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %{S:5} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:6} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %{S:7} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:8} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %{S:9} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:10} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %{S:11} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:12} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/qa_virtualization-standalone.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/qa_virtualization-network.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/qa_virtualization-sles10sp4supported-standalone.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/qa_virtualization-sles10sp4supported-network.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/qa_virtualization-sles11sp1supported-standalone.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/qa_virtualization-sles11sp1supported-network.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name .svn -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_virtualization.8.gz
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/qa_virtualization-standalone.tcf
/usr/share/qa/tcf/qa_virtualization-network.tcf
/usr/share/qa/tcf/qa_virtualization-sles10sp4supported-standalone.tcf
/usr/share/qa/tcf/qa_virtualization-sles10sp4supported-network.tcf
/usr/share/qa/tcf/qa_virtualization-sles11sp1supported-standalone.tcf
/usr/share/qa/tcf/qa_virtualization-sles11sp1supported-network.tcf
/usr/share/qa/tools/test_virtualization-standalone-run
/usr/share/qa/tools/test_virtualization-network-run
/usr/share/qa/tools/test_virtualization-sles10sp4supported-standalone-run
/usr/share/qa/tools/test_virtualization-sles10sp4supported-network-run
/usr/share/qa/tools/test_virtualization-sles11sp1supported-standalone-run
/usr/share/qa/tools/test_virtualization-sles11sp1supported-network-run
#%config /usr/share/qa/%name/config
#%{_docdir}/%{name}
#%doc %{_docdir}/%{name}/README

%changelog
