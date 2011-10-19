# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE. All Rights Reserved.
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
# spec file for package qa_pcmk (Version 0.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_pcmk
BuildRequires:  ctcs2
License:		SUSE Proprietary
Group:          SuSE internal
Summary:	Pacemaker internal test suite
Provides:	qa_pcmk
Obsoletes:	qa_pcmk
Requires:	pacemaker
Version:	1.0
Release:	1
Source0:	%name-%version.tar.bz2
Source1:	test_pcmk-run
Source2:        qa_test_pcmk.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch: noarch

%description
Pacemaker internal testsuite.

Uses crm_simulate to emulate different scenarios

Authors:
--------
    Dinar Valeev <dvaleev@novell.com>

%prep
%setup -q -n %name

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools

ln -s ../%name/tcf/qa_pcmk.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools

cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_pcmk.8.gz
%dir %{_datadir}/qa
%{_datadir}/qa/%name
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_pcmk-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_pcmk.tcf

%changelog


