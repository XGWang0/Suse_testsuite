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
# spec file for package qa_test_lynis
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_lynis
License:        SUSE Proprietary
Group:          SuSE internal
Summary:        lynis 
Version:	1.3.0
Release:	1
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}.8
Source2:        test_lynis-run
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Lynis is a security and system auditing tool. It scans a system on the
most interesting parts useful for audits, like:
     - Security enhancements
     - Logging and auditing options
     - Banner identification
     - Software availability
Lynis is released as a GPL licensed project and free for everyone to use.

See http://www.rootkit.nl for a full description and documentation.


%prep
%setup -q 

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -d $RPM_BUILD_ROOT/usr/share/qa/%{name}/{include,plugins,db}
install -m 755 lynis $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 644 default.prf $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 644 include/* $RPM_BUILD_ROOT/usr/share/qa/%{name}/include/
install -m 644 plugins/*  $RPM_BUILD_ROOT/usr/share/qa/%{name}/plugins/
install -m 644 db/*  $RPM_BUILD_ROOT/usr/share/qa/%{name}/db/
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%dir /usr/share/qa
%dir /usr/share/qa/tools
%dir /usr/share/qa/%{name}
%dir /usr/share/qa/%{name}/include
%dir /usr/share/qa/%{name}/plugins
%dir /usr/share/qa/%{name}/db
/usr/share/qa/%{name}/lynis
/usr/share/qa/%{name}/default.prf
/usr/share/qa/%{name}/include/*
/usr/share/qa/%{name}/plugins/*
/usr/share/qa/%{name}/db/*
/usr/share/qa/tools/test_lynis-run
/usr/share/man/man8/%{name}.8.gz

%changelog 
* Wed Dec 12 2012 - yxu@suse.de
- package created

