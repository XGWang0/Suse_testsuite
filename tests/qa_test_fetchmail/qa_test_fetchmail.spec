#
# spec file for package qa_fetchmail (Version 0.2.1)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


Name:           qa_test_fetchmail
Url:            http://httpd.apache.org/test/
Version:        0.2.1
Release:        2
License:        Other uncritical OpenSource License
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
