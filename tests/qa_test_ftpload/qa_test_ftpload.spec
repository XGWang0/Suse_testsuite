# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
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
# spec file for package ftpload (Version 0.8.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#



Name:           qa_test_ftpload
BuildRequires:  ctcs2
Summary:        ftp download test
Version:        0.1
Release:        1
Provides:	qa_ftpload
Obsoletes:	qa_ftpload
Requires:       wget pure-ftpd ctcs2
Group:          Development/Tools/Other
License:        SUSE Proprietary
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        ftpload
Source1:        test_ftpload-run
Source2:        ftpload.tcf
Source3:        ftpload.sh
Source4:	cert_tests.lib
Source5:	qa_test_ftpload.8
Source6:	qa_test_ftpload-config
BuildArchitectures: noarch

%description
Download ftp source for times.

Authors:
--------
    Arthur Guo <aguo@novell.com>

%prep

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/bin/
install -m 755 -d $RPM_BUILD_ROOT/usr/lib/
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8/
cp %{S:0} $RPM_BUILD_ROOT/usr/bin/
cp %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools
cp %{S:2} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
cp %{S:3} $RPM_BUILD_ROOT/usr/share/qa/%name/
cp %{S:4} $RPM_BUILD_ROOT/usr/lib/
cp %{S:5} $RPM_BUILD_ROOT/usr/share/man/man8/
cp %{S:6} $RPM_BUILD_ROOT/usr/share/qa/%name/
gzip $RPM_BUILD_ROOT/usr/share/man/man8/qa_test_ftpload.8
ln -s ../%name/tcf/ftpload.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(755,root,root)
/usr/bin/*
/usr/lib/*
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/ftpload.tcf
/usr/share/qa/tools/test_ftpload-run
/usr/share/man/man8/*

%changelog
* Mon Oct 24 2011 - cachen@suse.com
- Add configuration file to set ftp source
* Wed Aug 17 2011 - llipavsky@suse.cz
- Remove qa_dummy dependency
* Thu Aug 11 2011 - llipavsky@suse.cz
- Package rename: qa_ftpload -> qa_test_ftpload
* Fri Feb 25 2011 - aguo@novell.com
- add man page of qa_test_ftpload
* Wed Feb 15 2011 - aguo@novell.com
- create ftpload package.

