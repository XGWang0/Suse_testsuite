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


Name:           qa_jenkins_rttest
License:        SUSE-NonFree
Summary:        Qa package for regressiont and kotd automation integration test on jenkins
Group:          SUSE internal
Requires:       python >= 2.6
Provides:       rtautotool
Obsoletes:      rtautotool
Version:        1.0
Release:        0
Source:         %{name}-%{version}.tar.bz2
Source1:        qa_jenkins_rttest.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
QA tool for regression and kotd automation test on Jenkins

%prep
%setup -n %{name}

%build

%install
install -m 755 -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man8
gzip %{buildroot}%{_mandir}/man8/%{name}.8
install -m 755 -d %{buildroot}%{_datadir}/qa/jenkins_rt_run
cp -a * %{buildroot}%{_datadir}/qa/jenkins_rt_run
find %{buildroot}%{_datadir}/qa/jenkins_rt_run -type d -name .pyc -exec rm -rf {} \;

%post

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{_mandir}/man8/qa_jenkins_rttest.8.gz
%{_datadir}/qa
#%doc COPYING

%changelog
