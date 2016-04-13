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

#
# spec file for package qa_samba (Version 0.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_virtualization
License:		SUSE Proprietary
Group:          SuSE internal
Summary:        (rd-)qa virtualization automated tests
Provides:	qa_virtualization
Obsoletes:	qa_virtualization
Requires:       bridge-utils tftp dhcp-server syslinux bind apache2 awk ctcs2 qa_tools libqainternal wget
Requires:       virtautolib >= 2.7.0
BuildRequires:  ctcs2 virtautolib-data
AutoReqProv:    on
Version:        0.1.5
Release:        1
Source0:        %name.tar.bz2
Source1:        generate.tar.bz2
Source2:        tools.tar.bz2
Source3:	qa_test_virtualization.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch  

%description
Test cases for virtualization

Authors:
--------
    Lukas Lipavsky <llipavsky@suse.cz>

%prep
%setup -n %{name} -a1 -a2

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}

chmod +x generate/*.sh
# 1. generate testcases
generate/_generate_install.sh -d /usr/share/qa/virtautolib/data/autoinstallation -m standalone >$RPM_BUILD_ROOT/usr/share/qa/%name/tcf/qa_virtualization-standalone.tcf
generate/_generate_install.sh -d /usr/share/qa/virtautolib/data/autoinstallation -m network > $RPM_BUILD_ROOT/usr/share/qa/%name/tcf/qa_virtualization-network.tcf
generate/_generate_virt-install.sh -d /usr/share/qa/virtautolib/data/autoinstallation >$RPM_BUILD_ROOT/usr/share/qa/%name/tcf/qa_virtualization-virt_install.tcf

#./_generate_install.sh -d /usr/share/qa/virtautolib/data/autoinstallation -m standalone -t "tap:aio"
#./_generate_install.sh -d /usr/share/qa/virtautolib/data/autoinstallation -m network -t "tap:qcow2"


cp tools/test_virtualization-virt_install* $RPM_BUILD_ROOT/usr/share/qa/tools
cp generate/_generate_vh-update* $RPM_BUILD_ROOT/usr/share/qa/tools
cp tools/test_virtualization-standalone-run $RPM_BUILD_ROOT/usr/share/qa/tools
cp tools/test_virtualization-guest-migrate-run $RPM_BUILD_ROOT/usr/share/qa/tools
cp tools/test_virtualization-guest-upgrade-run $RPM_BUILD_ROOT/usr/share/qa/tools

rm -fr tools generate _install.template

chmod +x $RPM_BUILD_ROOT/usr/share/qa/tools/test_virtualization*-run
chmod +x $RPM_BUILD_ROOT/usr/share/qa/tools/test_virtualization-standalone-run
chmod +x $RPM_BUILD_ROOT/usr/share/qa/tools/_generate_vh-update_tests.sh
chmod +x $RPM_BUILD_ROOT/usr/share/qa/tools/test_virtualization-guest-migrate-run
chmod +x $RPM_BUILD_ROOT/usr/share/qa/tools/test_virtualization-guest-upgrade-run

cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name

for tcf in `cd $RPM_BUILD_ROOT/usr/share/qa/%name/tcf  ; ls` ; do
	ln -s ../%name/tcf/$tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_virtualization.8.gz
/usr/share/qa
%doc COPYING
%attr(0755,root,root) /usr/share/qa/%name/netinfo/*
%attr(0755,root,root) /usr/share/qa/%name/loc/cleanup.*
%attr(0755,root,root) /usr/share/qa/%name/loc/prepare.*
%attr(0755,root,root) /usr/share/qa/%name/installos
%attr(0755,root,root) /usr/share/qa/%name/cleanup
%attr(0755,root,root) /usr/share/qa/%name/virt_installos

%changelog

