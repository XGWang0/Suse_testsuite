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
# spec file for package rugg (Version 0.2.3)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_rugg
License:        SUSE Proprietary
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

