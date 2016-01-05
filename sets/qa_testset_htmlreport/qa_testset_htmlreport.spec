#!BuildIgnore: post-build-checks

# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
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

Name:           qa_testset_htmlreport
License:        GPL v2 or later
Group:          testset
Requires:       java >= 1.7
AutoReqProv:    on
Version:        1.0
Release:        0
Summary:        A test test tool for generating html report for testset automation framework
Source0:        testset_htmlreport-%{version}.tar.bz2
Source1:        qa_testset_htmlreport.8
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
qa_testset_htmlreport is a tools for generating cucumber report.

Authors:
--------
    John Wang <xgwang@suse.com>

%prep
%setup -n testset_htmlreport

%install
export NO_BRP_CHECK_BYTECODE_VERSION=true
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 755 -d %{buildroot}%{_datadir}/qa/qaset/report
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
cp -a * %{buildroot}%{_datadir}/qa/qaset/report

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{_datadir}/qa
/usr/share/man/man8/*

%changelog
* Tue Aug 18 2015 xgwang@suse.de
- initial package
