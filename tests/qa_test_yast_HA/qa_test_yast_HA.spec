# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE. All Rights Reserved.
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
# spec file for package qa_test_yast_HA (Version 0.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/

Name:           qa_test_yast_HA
License:	SUSE Proprietary
Group:          SuSE internal
Summary:        HA Yast tools UI Automation tests
Provides:	qa_yast_HA
Obsoletes:	qa_yast_HA
Requires:       strongwind ctcs2 python-pexpect yast2-cluster yast2-iplb yast2-drbd yast2-gtk
Version:        0.1
Release:        1
Source0:        %{name}-%{version}.tar.bz2
Source1:        qa_HA_yast-cluster.tcf
Source2:        test_HA_yast-cluster-run
Source3:	qa_test_yast_HA.8
Source4:        test_HA_yast-iplb-run
Source5:        qa_HA_yast-iplb.tcf
Source6:        test_HA_yast-drbd-run
Source7:        qa_HA_yast-drbd.tcf
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
UI Automation test cases for HA Yast tools package, include yast2-cluster yast2-iplb yast2-drbd

%prep
%setup -q -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %{S:5} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:6} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %{S:7} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/qa_HA_yast-cluster.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/qa_HA_yast-iplb.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/qa_HA_yast-drbd.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_yast_HA.8.gz
/usr/share/qa
/usr/share/qa/tcf
/usr/share/qa/tools
%doc COPYING

%changelog
* Tue Feb 28 2012 - cachen@suse.com
- package created, version 0.1

