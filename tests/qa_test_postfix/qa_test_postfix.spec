#
# spec file for package qa_postfix (Version 0.2)
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_postfix
#BuildRequires:  libqainternal
License:        GPL v2 or later
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
