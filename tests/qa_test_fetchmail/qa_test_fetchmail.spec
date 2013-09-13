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
# spec file for package qa_fetchmail (Version 0.2.1)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_fetchmail
Url:            None
Version:        0.2.1
Release:        2
License:        SUSE Proprietary
Group:          System/Packages
AutoReqProv:    on
Source0:        %{name}-%{version}.tar.bz2
Source1:        qa_fetchmail.tcf
Source2:        test_fetchmail-run
Source3:	qa_test_fetchmail.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Summary:        (rd-)qa internal package for fetchmail testing
BuildArch:      noarch
Provides:	qa_fetchmail
Obsoletes:	qa_fetchmail
Requires:       fetchmail xinetd cyrus-imapd postfix
Provides:	qa_fetchmail
Obsoletes:	qa_fetchmail
Requires:       ctcs2
Requires:       libqainternal

%description
fetchmail tests:

- fetching via imap(s)

- fetching via pop3(s)



%prep
%setup -n %{name}
%define qa_location /usr/share/qa/qa_test_fetchmail

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}
#
cp -rv * $RPM_BUILD_ROOT/%{qa_location}
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tools
cp %{SOURCE1} $RPM_BUILD_ROOT/%{qa_location}/tcf
ln -s ../%{name}/tcf/qa_fetchmail.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/qa/tools

%clean
rm -rvf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_fetchmail.8.gz
/usr/share/qa
/usr/share/qa/tcf/qa_fetchmail.tcf
%{qa_location}
%doc COPYING
%attr(0755,root,root) /usr/share/qa/%name/bin/*.sh
%attr(0755,root,root) /usr/share/qa/%name/*
%attr(0644,root,root) /usr/share/qa/%name/COPYING

%changelog
* Wed Dec 30 2009 puzel@suse.cz
- update to 0.2.1
  - main.cf: use default myhostname
* Wed Nov 19 2008 mmrazik@suse.cz
- make test_fetchmail-run executable
* Thu Oct 23 2008 puzel@suse.cz
- update to 0.2
  - use cyrus-imapd
  - use libqainternal for some tasks
* Thu Jan 10 2008 mmrazik@suse.cz
- enable required xinetd services (imap, pop3) automatically
* Fri Jun 23 2006 mmrazik@suse.cz
- initial release

