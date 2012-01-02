#!BuildIgnore: post-build-checks
#
# spec file for package qa_hazard (Version 0.1)
#
# Please submit bugfixes or comments via http://bugzilla.novell.com/
#

# norootforbuild

Name: qa_test_kiwi
License:        GPL v2
Group:          SuSE internal
Version: 0.1
Release:        1
Summary:        (rd-)qa internal package for training
Provides:	qa_kiwi
Obsoletes:	qa_kiwi
Requires:	perl perl-Config-IniFiles perl-IO-stringy ctcs2 squashfs qemu
Url:            http://qa.suse.de/
Source0:        %name-%version.tar.bz2
Source1:        test_kiwi-run
Source2:        qa_kiwi_dict.conf
Source3:	qa_test_kiwi.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
AutoReqProv:    off

%description
automation for kiwi
automatic generate kinds type of iso



Authors:
--------
    ms

%prep
%setup -q -n %{name}

%build
make

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8

install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tools
install -m 755 %{SOURCE1}  $RPM_BUILD_ROOT/usr/share/qa/%name/tools
install -m 644 %{SOURCE2}  $RPM_BUILD_ROOT/usr/share/qa/%name
prefix=$RPM_BUILD_ROOT make install
gzip $RPM_BUILD_ROOT/usr/share/man/man1/*


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)   
/usr/share/qa
/usr/share/qa/%name
/srv/tftpboot/
/usr/bin/dcounter
/usr/bin/driveready
/usr/bin/startshell
/usr/bin/utimer
/usr/sbin/kiwi
/usr/share/man/man1/kiwi.1.gz
/usr/share/man/man1/KIWI::config.sh.1.gz
/usr/share/man/man1/KIWI::kiwirc.1.gz
/usr/share/man/man1/KIWI::images.sh.1.gz
/usr/share/doc/packages/kiwi
/usr/share/kiwi
/usr/share/man/man8/qa_test_kiwi.8.gz


%changelog
* Wed Aug 17 2011 - llipavsky@suse.cz
- Remove qa_dummy dependency
* Thu Aug 11 2011 - llipavsky@suse.cz
- Package rename: qa_kiwi -> qa_test_kiwi
* Thu Mar 23 2011 - jtang@novell.com
- initial 0.1


