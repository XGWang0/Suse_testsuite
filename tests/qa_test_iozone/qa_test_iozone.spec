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
Source1:        ctcstools-%{version}.tar.bz2
Source2:        qa_test_iozone.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
IOzone is a filesystem benchmark tool. The benchmark generates and measures a variety 
of file operations. Iozone has been ported to many machines and runs under many
operating systems. 


%prep
%setup -q -n %{name} -a1

%build
cd src/current
make linux

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/bin
install -m 744 src/current/iozone $RPM_BUILD_ROOT/usr/bin
install -m 744 src/current/fileop $RPM_BUILD_ROOT/usr/bin
install -m 744 src/current/Generate_Graphs $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 744 src/current/gengnuplot.sh $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 744 src/current/gnu3d.dem $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 744 src/current/iozone_visualizer.pl $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 744 src/current/report.pl $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 644 src/current/Gnuplot.txt $RPM_BUILD_ROOT/usr/share/qa/%name
#ctcstools files
install -m 644 ctcstools/qa_iozone.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 ctcstools/test_iozone-run $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 ctcstools/iozoneparser $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 ctcstools/test_iozone_doublemem-run $RPM_BUILD_ROOT/usr/share/qa/tools

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

