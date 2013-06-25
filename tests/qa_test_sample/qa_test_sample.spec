# ****************************************************************************
# Copyright © 2013 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
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
# spec file for package qa_sample (Version 0.1)
#
# Please submit bugfixes or comments via http://bugzilla.novell.com/
#

# norootforbuild

Name:           qa_test_sample
BuildRequires:  ctcs2
License:        SUSE Proprietary
Group:          SuSE internal
AutoReqProv:    on
Version:        0.11
Release:        1
Summary:        (rd-)qa internal package for training
Url:            http://qa.suse.de/
Source0:        %name-%version.tar.bz2
Source1:        qa_sample.tcf
Source2:        test_sample-run
Source3:        qa_test_sample.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	qa_sample
Obsoletes:	qa_sample
Requires:       ctcs2

%description
This is a sample qa_ test package that can be used as a template to 
create other packages or just for training purposes.

Authors:
--------
    Dan Collingridge <dcollingridge@novell.com>

%prep
%setup -q -n %{name}

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/qa_sample.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name CVS -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)   
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/qa_sample.tcf
/usr/share/qa/tools/test_sample-run
/usr/share/man/man8/*
%doc COPYING

%changelog
* Thu Sep 02 2010 - aguo@novell.com
- Add perl and python sample
* Wed Aug 25 2010 - dcollingridge@novell.com
- Added this as a new package for training/templating purposes
