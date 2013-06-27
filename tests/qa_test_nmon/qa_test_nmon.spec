# ****************************************************************************
#
# Copyright (c) 2012 Novell, Inc.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 2 of the GNU General Public License as
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

# ****************************************************************************
#
#
# spec file for package qa_test_nmon

# norootforbuild

Name:           qa_test_nmon
License:        GPL v2 or later
Group:          SuSE internal
Summary:        nmom 
Version:	1
Release:	1
Source0:        nmon_linux_14g.tar.gz
Source1:        %{name}.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
nmon tool is used to monitor and analyze performance data, including:
    CPU utilization
    Memory use
    Kernel statistics and run queue information
    Disks I/O rates, transfers, and read/write ratios
    Free space on file systems
    Disk adapters
    Network I/O rates, transfers, and read/write ratios
    Paging space and paging rates
    CPU and AIX specification
    Top processors
    IBM HTTP Web cache
    User-defined disk groups
    Machine details and resources
    Asynchronous I/O -- AIX only
    Workload Manager (WLM) -- AIX only
    IBM TotalStorage® Enterprise Storage Server® (ESS) disks -- AIX only
    Network File System (NFS)
    Dynamic LPAR (DLPAR) changes 


%prep
%setup -q 

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d $RPM_BUILD_ROOT/usr/share/qa/%{name}/bin/
install -m 755 {nmon_ia64_sles10,nmon_power_32_sles11,nmon_power_64_sles11,nmon_x86_64_sles11,nmon_x86_sles11} $RPM_BUILD_ROOT/usr/share/qa/%{name}/bin/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%dir /usr/share/qa
%dir /usr/share/qa/%{name}
%dir /usr/share/qa/%{name}/bin
/usr/share/qa/%{name}/bin/nmon_ia64_sles10
/usr/share/qa/%{name}/bin/nmon_power_32_sles11
/usr/share/qa/%{name}/bin/nmon_power_64_sles11
/usr/share/qa/%{name}/bin/nmon_x86_64_sles11
/usr/share/qa/%{name}/bin/nmon_x86_sles11
/usr/share/man/man8/%{name}.8.gz

%changelog 
* Mon Dec 03 2012 - yxu@suse.de
- package created

