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

Source1:	qa_test_slepos.8
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

# norootforbuild

Name:           qa_test_slepos
Version:	0.5
Release:	1
Summary:	SLEPOS (semi)automation bash scripts
Group:		System/Benchmark
License:		SUSE Proprietary
Url:		http://qa.suse.de
BuildArch:      noarch
Source0:		%{name}-%{version}.tar.bz2
Source1:		qa_test_slepos.8
Provides:	qa_slepos
Obsoletes:	qa_slepos
Requires:	bash qa_keys
%if 0%{?suse_version} >= 1000
Recommends:	ctcs2
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description

Authors:
--------
    Tomas Cech <tcech@suse.cz>
    Erik Hamera <ehamera@suse.cz> 

%prep
%setup -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 qa_slepos-admin.tcf $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
ln -s ../%name/tcf/qa_slepos-admin.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/qa_slepos-admin.tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 slepos-run $RPM_BUILD_ROOT/usr/share/qa/tools/
install -m 755 -d $RPM_BUILD_ROOT/usr/share/doc/packages/%name
install -m 644 README $RPM_BUILD_ROOT/usr/share/doc/packages/%name
cp -a usr $RPM_BUILD_ROOT/

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ -f "/root/slepos_lib.sh" ] || ln -s /usr/share/qa/qa_test_slepos/slepos_lib.sh /root/slepos_lib.sh 
[ -f "/root/qa_slepos-local_config.sh" ] || ln -s /usr/share/qa/qa_test_slepos/local_config.sh /root/qa_slepos-local_config.sh 
%postun

%files
%defattr(-,root,root)
/usr/share/man/man8/qa_test_slepos.8.gz
/usr/share/qa
%config /usr/share/qa/%name/local_config.sh
%{_docdir}/%{name}
%doc %{_docdir}/%{name}/README

%changelog

