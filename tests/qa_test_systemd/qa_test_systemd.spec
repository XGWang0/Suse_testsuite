#
#****************************************************************************
# spec file for package systemd
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
# norootforbuild
#
#***************************************************************************
#

Name:           qa_test_systemd
License:        GPL v2
Group:          SuSE internal
Summary:        systemd test
Requires:       ctcs2, apache2, apparmor-parser, at, audit, bluez, brltty, cups, cron, cyrus-sasl-saslauthd, device-mapper, dovecot, dnsmasq, gpm, haveged, kexec-tools, libvirt, lvm2, mariadb, mdadm, multipath-tools, nfs-client, nfsidmap, nfs-kernel-server, nscd, openslp-server, PackageKit, pcsc-lite, postfix, postgresql-server, quota, radvd, rpcbind, rsync, rsyslog, samba, samba-winbind, spice-vdagent, SuSEfirewall2, systemd, upower, usbmuxd, vsftpd, yast2-nfs-server, xinetd
Version:        1
Release:        1
Source:         qa_test_systemd-1.tar.bz2
Source1:        test_systemd-run
Source2:        qa_test_systemd.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
During Beta7 and Beta8 regression testing, we noticed that systemd upgrade easier to cause system service regression issue(specially relate to sysvinit), such as kdump in bnc882395 and bnc869608, postfix in bnc879960, nfs in bnc860246. So do a basic service activity testing is necessarily. 
We designed 2 test points for systemd service as first step, the automation is implemented.

%prep
%setup

%build
while read -r line; do
    cat <<END >> tcf/qa_systemd.tcf

timer 1800
fg 1 check-${line} %{_datadir}/qa/%{name}/check-service.sh "${line}"
wait
END
done < services
chmod +x *.sh

%install
install -m 755 -d %{buildroot}/%{_datadir}/qa
install -m 755 -d %{buildroot}/%{_datadir}/qa/%name
cp -r * %{buildroot}/%{_datadir}/qa/%name
install -m 755 -d %{buildroot}/%{_datadir}/qa/%name/tcf
install -m 755 -d %{buildroot}/%{_datadir}/qa/tcf
install -m 755 -d %{buildroot}/%{_datadir}/qa/tools
install -m 755 %{S:1} %{buildroot}/%{_datadir}/qa/tools
ln -s %{_datadir}/qa/%name/tcf/qa_systemd.tcf %{buildroot}/%{_datadir}/qa/tcf/
# man page
install -m 755 -d %{buildroot}/%{_datadir}/man/man8
install -m 644 %{S:2} %{buildroot}/%{_datadir}/man/man8
gzip %{buildroot}/%{_datadir}/man/man8/%{name}.8

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{_datadir}/man/man8/%{name}.8.gz
%dir %{_datadir}/qa
%{_datadir}/qa/%name
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_systemd.tcf
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_systemd-run

%changelog 
* Mon Nov 30 2015 - jtzhao@suse.com
- Only test pre-defined services(bsc#955543)
* Fri Jul 25 2014 - bwliu@suse.com
- package created, version 0.1
