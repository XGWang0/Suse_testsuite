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
# spec file for package qa_iosched_test (Version 0.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_iosched
BuildRequires:  ctcs2
License:        SUSE Proprietary
Group:          SuSE internal
Autoreqprov:    on
Version:        0.1
Release:        1
Summary:        rd-qa-kernel internal package to test behaviour of available ioschedulers
Url:            None
Source:         %{name}-%{version}.tar.bz2
Source1:	qa_test_iosched.8
Source2:	test_iosched-run
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	qa_iosched_test
Obsoletes:	qa_iosched_test
Requires:       ctcs2 tiobench
BuildArchitectures: noarch
#ExclusiveArch: %ix86

%description
Tries small benchmark on all available ioschedulers for the device.



Authors:
--------
    Frank Seidel <fseidel@suse.de>

%prep
%setup -n %{name}

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d -v $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
install -m 755 -d -v $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/tcf
cp -v iosched_testing.sh $RPM_BUILD_ROOT/usr/share/qa/%{name}/
cp -v qa_iosched_test.tcf $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf/
ln -sf ../%{name}/tcf/qa_iosched_test.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/qa_iosched_test.tcf
ln -sf ../../../share/qa/%{name}/tcf/qa_iosched_test.tcf  $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf/qa_iosched_test.tcf
cp -v %{S:2} $RPM_BUILD_ROOT/usr/lib/ctcs2/tools/

%clean
rm -rvf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_iosched.8.gz
/usr/lib/ctcs2/tools/test_iosched-run
/usr/lib/ctcs2/tcf/qa_iosched_test.tcf
/usr/share/qa
/usr/share/qa/qa_test_iosched
/usr/share/qa/tcf/qa_iosched_test.tcf

%changelog -n qa_test_iosched
* Wed Feb 15 2006 - fseidel@suse.de
- initial release

