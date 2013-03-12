# ****************************************************************************
# Copyright (c) 2012 Unpublished Work of SUSE. All Rights Reserved.
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
# spec file for package qa_test_iozone (Version 3_300)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_iozone
License:        Freeware
Group:          SuSE internal
Summary:        iozone test
Requires:       ctcs2
BuildRequires:  ctcs2
Version:        3_300
Release:	1
Source0:        %name-%version.tar.bz2
Source1:        qa_iozone.tcf
Source2:        test_iozone-run
Source3:	qa_test_iozone.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

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
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/bin
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
* Thu Nov 15 2012 - yxu@suse.de
- package created, version 3_300

