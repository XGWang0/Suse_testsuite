# ****************************************************************************
# Copyright (c) 2013, 2014 Unpublished Work of SUSE. All Rights Reserved.
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
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Summary:     virt-test wrapper for QA Automation
Name:        qa_test_virt-test
Version:     1.0
Release:     1
License:     GPL-2.0+
Url:         https://github.com/autotest/virt-test
Group:       Applications/System
Source0:     %{name}-run
Source1:     %{name}.8
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:    virt-test


%description
This is a wrapper for the upstream virt-test testsuite. This wrapper
integrates the testsuite with the QA Automation tool Hamsta.

Read the virt-test package description for more information about the
test itself.

Note that in order to install this testsuite you need to add the
virtualization team's package repository, the SLES SDK and Updates
repository (e.g. register your SLES product).

%prep

%build

%install
install -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man8
gzip %{buildroot}%{_mandir}/man8/%{name}.8
install -d %{buildroot}%{_datadir}/qa/%{name}/bin/
install -m 755 %{SOURCE0} %{buildroot}%{_datadir}/qa/%{name}/bin/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_datadir}/qa/%{name}
%dir %{_datadir}/qa/%{name}/bin
%{_datadir}/qa/tools/bin/%{name}-run
%{_mandir}/man8/%{name}.8.gz
%doc

%changelog
