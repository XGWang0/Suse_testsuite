# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE. All Rights Reserved.
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
# spec file for package qa_postfix (Version 0.2)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_postfix
#BuildRequires:  libqainternal
License:		SUSE Proprietary
Group:          System/Packages
Summary:        Basic postfix tests for ctcs framework
Provides:	qa_postfix
Obsoletes:	qa_postfix
Requires:       postfix libqainternal ctcs2
AutoReqProv:    on
Version:        0.2
Release:        192
Source0:        %name-%version.tar.bz2
Source1:        qa_postfix.tcf
Source2:        test_postfix-run	
Source3:        README
Source4:	qa_test_postfix.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
%define qa_location /usr/share/qa/%{name}

%description
Testcases for postfix package. Tests start, restart and stop of the
service (so far)



%prep
%setup -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}
cp -rv * $RPM_BUILD_ROOT/%{qa_location}
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/tcf
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/doc
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tools
cp %{SOURCE1} $RPM_BUILD_ROOT/%{qa_location}/tcf
ln -s ../%name/tcf/qa_postfix.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp %{SOURCE3} $RPM_BUILD_ROOT%{qa_location}/doc

%clean
rm -rvf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)   
/usr/share/man/man8/qa_test_postfix.8.gz
%{qa_location}
/usr/share/qa
#/usr/share/qa/tcf/qa_postfix.tcf
#/usr/share/qa/tools/test_postfix-run

%changelog
* Thu Jun 18 2009 llwang@novell.com
- fix 0006_send_attachment.sh
* Fri Sep 26 2008 mmrazik@suse.cz
- test_postfix-run made executable
* Fri Sep 19 2008 mmrazik@suse.cz
- "Message file too big" changed to lowercase in latest postfix.
  Test checking for this message fixed.
* Fri Jan 11 2008 mmrazik@suse.cz
- use custom aliases for send_to_nonexistent test to make sure mail
  is really bounced to root
* Thu Jan 03 2008 mmrazik@suse.cz
- look for error logs both in /var/log/mail and /var/log/mail.err
  because syslog-ng logs everything in /var/log/mail by default
* Wed Aug 23 2006 mmrazik@suse.cz
- new tests added (mailq, postalias, postcat, defer transport, virtual domains)
* Thu Aug 10 2006 mmrazik@suse.cz
- existing tests rewritten to use new shell testscript API
- new tests added (send e-mail, send e-mail to alias,
  newaliases command, send e-mail to bad address)
- changed to noarch
* Wed Apr 19 2006 kmachalkova@suse.cz
- package created

