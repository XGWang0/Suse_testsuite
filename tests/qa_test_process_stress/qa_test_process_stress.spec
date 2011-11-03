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

Source1:	qa_test_process_stress.8
#
# spec file for package qa_process_stress (Version 0.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_process_stress
#BuildRequires:  ctcs2
License:        SUSE Proprietary
Group:          SUSE internal
Summary:        process stress test from LTP
Provides:	qa_process_stress
Obsoletes:	qa_process_stress
Requires:       ctcs2 ltp
Version:        0.1
Release:        2
Source0:        %{name}-%{version}.tar.bz2
Source1:        qa_test_process_stress.8
Source2:        test_process_stress-run
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
process stress test from LTP

%prep
%setup -n %{name} 

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
cp do_process_stress $RPM_BUILD_ROOT/usr/share/qa/tools
cp process_stress.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf 
cp %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
chmod 755 $RPM_BUILD_ROOT/usr/share/qa/tools/test_process_stress-run
ln -s ../../../share/qa/tcf/process_stress.tcf $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_process_stress.8.gz
/usr/share/qa
/usr/lib/ctcs2
%changelog
* Tue Mar 01 2011 llwang@novell.com
- modify loop condition
* Wed Apr 01 2009 yxu@suse.de
- initial release

