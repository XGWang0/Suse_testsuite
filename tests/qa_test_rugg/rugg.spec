# ****************************************************************************
#
# Copyright (c) 2013 Novell, Inc.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.   See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact Novell, Inc.
#
# To contact Novell about this file by physical or electronic mail,
# you may find current contact information at www.novell.com

# ****************************************************************************
#
# spec file for package rugg (Version 0.2.3)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_rugg
License:        GPL V2
Group:          Filesystem test
Summary:        rugg test
Requires:  	python >= 2.4, findutils-locate, pychecker, epydoc, ctags, sudo
BuildRequires: 	python >= 2.4, python-devel, findutils-locate, pychecker, epydoc, ctags, sudo
BuildRequires:	-post-build-checks 
Version:        0.2.3
Release:	1
Source0:        %name-%version.tar.bz2
Source1:        qa_rugg.tcf
Source2:        test_rugg-run
Source3:        %name.8
Source4:	input
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Rugg is a hard drive and filesystem harness tool that allows you to test and 
benchmark drives and filesystems, by writing simple to complex scenarios that 
can mimic the behaviour of real-world applications.


%prep
%setup

%build
python setup.py build

%install
python setup.py install --root=$RPM_BUILD_ROOT 

install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/%name/
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/bin
ln -s ../%name/tcf/qa_rugg.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%dir /usr/local/%_lib/python2.6/site-packages
/usr/local/%_lib/python2.6/site-packages/*
/usr/local/bin/rugg
%dir /usr/share/qa/%name
/usr/share/qa/%name/input
/usr/share/qa/tcf/qa_rugg.tcf
/usr/share/qa/%name/tcf/qa_rugg.tcf
/usr/share/qa/tools/test_rugg-run
/usr/share/man/man8/%name.8.gz

%changelog 
* Wed Mar 06 2013 - yxu@suse.de
- package created, version 0.2.3

