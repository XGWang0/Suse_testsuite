# ****************************************************************************
# Copyright (c) 2012 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************
#

#
# spec file for package qa_test_nmon
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_nmon
License:        SUSE Proprietary
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

