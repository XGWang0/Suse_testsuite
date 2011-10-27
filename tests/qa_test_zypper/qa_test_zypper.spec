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

Name:           qa_test_zypper
License:        SUSE Proprietary
Group:          System/Packages
Summary:        Basic light zypper tests for ctcs2 framework
Provides:	qa_zypper
Obsoletes:	qa_zypper
Requires:       zypper >= 1.0 ctcs2
AutoReqProv:    on
Version:        1.0
Release:        1
Source0:        %name-%version.tar.bz2
Source1:        qa_zypper.tcf
Source2:        test_zypper-run	
Source3:	qa_test_zypper.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
%define qa_location /usr/share/qa/%{name}

%description
Testcases for zypper package. This is a light test suite, which focus on
options and commands test.
There is another API level test suite libzypp-testsuite-tools, but this
one is much bigger, slower and have too many dependences.

%prep
%setup -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}
cp -rv * $RPM_BUILD_ROOT/%{qa_location}
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tools
cp %{SOURCE1} $RPM_BUILD_ROOT/%{qa_location}/tcf
ln -s ../%name/tcf/qa_zypper.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/qa/tools

%clean
rm -rvf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_zypper.8.gz
%{qa_location}
/usr/share/qa

%changelog
* Wed Aug 10 2011 - llipavsky@suse.cz
- Package rename: qa_zypper -> qa_test_zypper
* Thu Apr 7 2011 llwang@novell.com
- Initial test packages

