# ****************************************************************************
#
# Copyright (c) 2013 Novell, Inc.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.   See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact Novell, Inc.
#
# To contact Novell about this file by physical or electronic mail,
# you may find current contact information at www.novell.com
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
# 
# ****************************************************************************
#
# spec file for package qa_test_lynis
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_lynis
License:        GPL v3
Group:          SuSE internal
Summary:        lynis 
Version:	1.3.0
Release:	1
Requires:	qa_lib_ctcs2
Source0:        %{name}-%{version}.tar.bz2
Source1:        default.prf 
Source2:        tests_binary_rpath
Source3:        tests_file_permissionsDB
Source4:        tests_file_permissions_ww
Source5:        tests_network_allowed_ports
Source6:        tests_system_dbus
Source7:        tests_system_proc
Source8:        tests_tmp_symlinks
Source9:        tests_users_wo_password
Source10:       prepare_for_suse.sh
Source11:       dbus-whitelist.db.openSUSE_12.2_x86_64
Source12:       fileperms.db.openSUSE_12.2_x86_64
Source21:       %{name}.8
Source22:       test_lynis-run
Source23:       qa_lynis.tcf
Source24:       runtest.sh
# PATCH-OPENSUSE-FIX -- thomas@novell.com - modifying for openSUSE  
Patch0:         lynis_%{version}_lynis.diff
# PATCH-OPENSUSE-FIX -- thomas@novell.com - modifying for openSUSE
Patch2:         lynis_%{version}_include_consts.diff
# PATCH-OPENSUSE-FIX -- thomas@novell.com - modifying for openSUSE
Patch3:         lynis_%{version}_include_binaries.diff
# PATCH-OPENSUSE-FIX -- thomas@novell.com - modifying for openSUSE
Patch4:         lynis_%{version}_include-test-databases.diff
Patch5:         lynis_%{version}_include-osdetection.diff
Patch6:         lynis_%{version}_include-test-filesystem.diff
Patch7:         lynis_%{version}_include-test-kernel.diff
Patch8:         lynis_%{version}_include-test-storage.diff
Patch9:         lynis_%{version}_include-test-homedirs.diff

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Lynis is a security and system auditing tool. It scans a system on the
most interesting parts useful for audits, like:
     - Security enhancements
     - Logging and auditing options
     - Banner identification
     - Software availability
Lynis is released as a GPL licensed project and free for everyone to use.

See http://www.rootkit.nl for a full description and documentation.


%prep
%setup -q 
%patch0
%patch2
%patch3
%patch4
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:21} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -d $RPM_BUILD_ROOT/usr/share/qa/%{name}/{include,plugins,db}
install -m 755 lynis $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 644 default.prf $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 %{S:10} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 644 include/* $RPM_BUILD_ROOT/usr/share/qa/%{name}/include/
install -m 644 {%{S:2},%{S:3},%{S:4},%{S:5},%{S:6},%{S:7},%{S:8},%{S:9}} $RPM_BUILD_ROOT/usr/share/qa/%{name}/include/
install -m 644 plugins/*  $RPM_BUILD_ROOT/usr/share/qa/%{name}/plugins/
install -m 644 db/*  $RPM_BUILD_ROOT/usr/share/qa/%{name}/db/
install -m 644 {%{S:11},%{S:12}}  $RPM_BUILD_ROOT/usr/share/qa/%{name}/db/
install -m 755 %{S:22} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %{S:23} $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 %{S:24} $RPM_BUILD_ROOT/usr/share/qa/%{name}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%dir /usr/share/qa
%dir /usr/share/qa/tools
%dir /usr/share/qa/tcf
%dir /usr/share/qa/%{name}
%dir /usr/share/qa/%{name}/include
%dir /usr/share/qa/%{name}/plugins
%dir /usr/share/qa/%{name}/db
/usr/share/qa/%{name}/lynis
/usr/share/qa/%{name}/runtest.sh
/usr/share/qa/%{name}/default.prf
/usr/share/qa/%{name}/prepare_for_suse.sh
/usr/share/qa/%{name}/include/*
/usr/share/qa/%{name}/plugins/*
/usr/share/qa/%{name}/db/*
/usr/share/qa/tools/test_lynis-run
/usr/share/qa/tcf/qa_lynis.tcf
/usr/share/man/man8/%{name}.8.gz

%changelog 
* Thu Mar 07 2013 - llipavsky@suse.com
- moved to use ctcs2 -> thus submit to QADB
* Wed Dec 12 2012 - yxu@suse.de
- package created

