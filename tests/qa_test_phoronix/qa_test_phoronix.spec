#!BuildIgnore: post-build-checks
# spec file for package phoronix test suite (Version 2.2.0)
#
# Copyright (c) 2009 SUSE LINUX Products GmbH,Nuernberg,Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners,unless otherwise agreed
# upon.The license for this file,and modifications and additions to the
# file,is the same license as for the pristine package itself(unless the 
# license for the pristine package is not an Open Source License,in which
# case the license is the MIT License).An "Open Source License" is a 
# license that conforms to the Open Source Definition(Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.novell.com/
#

# norootforbuild
Name:   qa_test_phoronix
License: GPL v3 or later
Summary: The most comprehensive testing and benchmarking platform for the Linux
URL: http://www.phoronix-test-suite.com/
Version: 2.2.0
Release: 1
Autoreqprov: on
Source0: phoronix-test-suite-%{version}.tar.bz2
Source1: ctcstools-%version.tar.bz2	
Source2:	qa_test_phoronix.8
Patch0:   run-PTS-automaticly.patch
Patch1:   build-imagemagick.patch
Patch2:   encode-ape.patch
Patch3:   non-interactive.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Provides:	qa_phoronix
Obsoletes:	qa_phoronix
Requires: php5 php5-gd
Group: SUSE internal

%description
This software is designed to effectively carry out both qualitative and quantitative benchmarks is a clean,reproducible,and easy-to-use manner.
The Phoronix Test Suite consists of a lightweight processing core(pts-core) with each benchmark consisting of an XML-based profile with related resource scripts.The process from the benchmark installation,to the actual benchmarking,to the parsing of important hardware and software components is heavily automated and completely repeatable,asking usrs only for confirmation of actions.

%prep
%setup -q -n phoronix-test-suite -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
export DESTDIR=${RPM_BUILD_ROOT}
./install-sh 
rm -f $RPM_BUILD_ROOT/usr/share/applications/phoronix-test-suite.desktop
 
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
cp ctcstools/test_phoronix-run $RPM_BUILD_ROOT/usr/share/qa/tools
cp ctcstools/*.tcf $RPM_BUILD_ROOT/usr/share/qa/%name/tcf

ln -s ../%name/tcf/pts_aio-stress.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_apache.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_blogbench.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_bork.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_build-apache.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_build-imagemagick.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_build-linux-kernel.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_build-mplayer.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_byte.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_cachebench.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_compliance-acpi.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_compliance-sensors.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_compress-7zip.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_compress-lzma.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_compress-pbzip2.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_crafty.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_c-ray.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_dcraw.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_encode-ape.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_encode-flac.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_encode-mp3.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_encode-ogg.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_encode-wavpack.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/pts_iozone.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/


# now fix file permissions
# no suid root
# no world writable
#find $RPM_BUILD_ROOT -type f -print0 |xargs -0 chmod -c o-w,u-s


%files
%defattr(-,root,root)
/usr/share/man/man8/qa_test_phoronix.8.gz
/usr/bin/phoronix-test-suite
/usr/share/doc/phoronix-test-suite
/usr/share/phoronix-test-suite
/usr/share/qa/%name
/usr/share/qa/tcf/
/usr/share/qa/tools/test_phoronix-run
%config /etc/bash_completion.d/phoronix-test-suite
#/usr/share/applications/phoronix-test-suite.desktop
/usr/share/icons/phoronix-test-suite.png
/usr/share/man/man1/phoronix-test-suite.1.gz

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Aug 15 2011 - llipavsky@suse.cz
- Package rename: qa_phoronix -> qa_test_phoronix


