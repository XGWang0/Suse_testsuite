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
License:        Freeware
Group:          SuSE internal
Summary:        systemd test
Requires:       ctcs2
BuildRequires:  ctcs2
Version:        1
Release:	1
Source:         qa_test_systemd-1.tar.bz2
Source1:        test_systemd-run
Source2:        qa_test_systemd.8

%description
During Beta7 and Beta8 regression testing, we noticed that systemd upgrade easier to cause system service regression issue(specially relate to sysvinit), such as kdump in bnc882395 and bnc869608, postfix in bnc879960, nfs in bnc860246. So do a basic service activity testing is necessarily. 
We designed 2 test points for systemd service as first step, the automation is implemented.

%prep
%setup

%build
while read -r line; do
    cat <<END >> qa_systemd.tcf

timer 1800
fg 1 check-${line} /usr/share/qa/qa_test_systemd/check-service.sh "${line}"
wait
END
done < services
chmod +x *.sh

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
cp -r * $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
mv qa_systemd.tcf $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools
#ln -s ../%name/tcf/qa_systemd.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s /usr/share/qa/%name/tcf/qa_systemd.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
# man page
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/%{name}.8.gz
%dir /usr/share/qa
/usr/share/qa/%name
%dir /usr/share/qa/tcf
/usr/share/qa/tcf/qa_systemd.tcf
%dir /usr/share/qa/tools
/usr/share/qa/tools/test_systemd-run

%changelog 
* Mon Nov 30 2015 - jtzhao@suse.com
- Only test pre-defined services(bsc#955543)
* Fri Jul 25 2014 - bwliu@suse.com
- package created, version 0.1
