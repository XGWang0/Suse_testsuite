#
#****************************************************************************
# spec file for package iozone
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

Name:           qa_test_iozone
License:        Freeware
Group:          SuSE internal
Summary:        iozone test
Requires:       ctcs2 qa_lib_perl
BuildRequires:  ctcs2
Version:        3_300
Release:	1
Source0:        %name-%version.tar.bz2
Source1:        qa_iozone.tcf
Source2:        test_iozone-run
Source3:	qa_test_iozone.8
Source4:	iozoneparser
Source7:        test_iozone_new_run
Source10:       qa_iozone_4-32G.tcf
Source11:   	test_iozone_bigmem-run
Source12:       qa_iozone_bigmem_basic.tcf.tpl
Source13:       test_iozone_bigmem_basic-run
Source20:   	abuildinfo
Source21: 	iozoneparser_4-32G
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
IOzone is a filesystem benchmark tool. The benchmark generates and measures a variety 
of file operations. Iozone has been ported to many machines and runs under many
operating systems. 


%prep
%setup -q -n %{name}

%build
cd src/current
make linux

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/bin
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:7} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:11} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:13} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 %{S:21} $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 %{S:20} $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 644 %{S:10} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:12} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
ln -s ../%name/tcf/qa_iozone_4-32G.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/qa_iozone_4-32G.tcf
install -m 744 src/current/iozone $RPM_BUILD_ROOT/usr/bin
install -m 744 src/current/fileop $RPM_BUILD_ROOT/usr/bin
install -m 744 src/current/Generate_Graphs $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 744 src/current/gengnuplot.sh $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 744 src/current/gnu3d.dem $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 744 src/current/iozone_visualizer.pl $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 744 src/current/report.pl $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 644 src/current/Gnuplot.txt $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/qa_iozone.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/%{name}.8.gz
/usr/bin/iozone
/usr/bin/fileop
/usr/share/qa
/usr/share/qa/%name/*

%changelog
* Wed July 09 2014 - bwliu@suse.com
- add new parser 'iozoneparser_4-32G' for tcf 'qa_iozone_4-32G.tcf'
* Thu Mar 05 2014 - bwliu@suse.com
- just change the name of /usr/bin/eatmem to /usr/bin/eatmem_iozone to avoid conflict with qa_test_tiobench.
- just change the name of /usr/share/qa/%name/eatmen.sh to /usr/share/qa/%name/eatmen_iozone.sh to avoid conflict with qa_test_tiobench.
* Thu Feb 25 2014 - bwliu@suse.com
- add iozoneparser
- eatmem to 512M
* Thu Nov 15 2012 - yxu@suse.de
- package created, version 3_300

