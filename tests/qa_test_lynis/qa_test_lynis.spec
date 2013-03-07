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
# spec file for package qa_test_lynis
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_lynis
License:        SUSE Proprietary
Group:          SuSE internal
Summary:        lynis 
Version:	1.3.0
Release:	1
Requires:	qa_lib_ctcs2
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}.8
Source2:        test_lynis-run
Source3:        qa_lynis.tcf
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
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -d $RPM_BUILD_ROOT/usr/share/qa/%{name}/{include,plugins,db}
install -m 755 lynis $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 644 default.prf $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 644 include/* $RPM_BUILD_ROOT/usr/share/qa/%{name}/include/
install -m 644 plugins/*  $RPM_BUILD_ROOT/usr/share/qa/%{name}/plugins/
install -m 644 db/*  $RPM_BUILD_ROOT/usr/share/qa/%{name}/db/
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:3} $RPM_BUILD_ROOT/usr/share/qa/tcf


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
/usr/share/qa/%{name}/default.prf
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

