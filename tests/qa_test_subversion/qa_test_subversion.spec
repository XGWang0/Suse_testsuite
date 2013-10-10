# ****************************************************************************
# Copyright © 2013 Unpublished Work of SUSE, Inc. All Rights Reserved.
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
# norootforbuild

Name:           qa_test_subversion
BuildRequires:  ctcs2
License:        SUSE Proprietary
Group:          SuSE internal
Summary:        Simple subversion tests for ctcs framework
Requires:       subversion subversion-server ctcs2 grep apache2
%if 0%{suse_version} >= 1100
Requires:       vim-base
%else
Requires:       vim
%endif
Version:        0.1.2
Release:        1
Source0:        %name-%version.tar.bz2
Source1:        qa_subversion.tcf
Source2:        test_subversion-run
Source3:        qa_test_subversion.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Test cases for subversion


Authors:
--------
    QAM team <qa-maintenance@suse.de>

%prep
%setup -q -n %{name}

%build

%install
# TODO: make this work from the makefile
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8/
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
ln -s ../%name/tcf/qa_subversion.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
chmod 755 $RPM_BUILD_ROOT/usr/share/qa/%name/svn.sh
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d \( -name CVS -or\
 -name .svn \) -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%dir /usr/share/qa
/usr/share/qa/%name
%dir /usr/share/qa/tools
/usr/share/qa/tools/test_subversion-run
%dir /usr/share/qa/tcf
/usr/share/qa/tcf/qa_subversion.tcf
/usr/share/man/man8/qa_test_subversion.8.gz
%doc LICENSE

%changelog
* Mon Jul 15 2013 - jmatejka@suse.cz
- initial release 0.1.0
