#
# spec file for package qa_libibmjava (Version 1.0)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

# QA automation dirs
%define destdir /usr/share/qa
%define libdir %{destdir}/lib/ibmjava

Name:		qa_lib_ibmjava
License:	GPL v2 or later
Group:		SUSE internal
AutoReqProv:	on
Version:	1.1
Release:	1
Summary:	Shared QA IBM Java functions
Url:            http://qit.suse.de/ibmjava/ibmjava/blobs/master/qa/
Source0:        http://qit.suse.de/ibmjava/ibmjava/blobs/master/qa/qa_lib_ibmjava.8
Source1:	http://qit.suse.de/ibmjava/ibmjava/blobs/master/qa/check-modified-files.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:	noarch

Requires:       bash
Requires:       coreutils
Requires:       grep
Requires:       sed

%description
IBM Java QA scripts

%prep
#nothing to do

%build
#nothing to do

%install
install -m 0755 -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE0} %{buildroot}%{_mandir}/man8

install -m 755 -d %{buildroot}%{libdir}

install -m 0755 %{SOURCE1} %{buildroot}%{libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%dir %{destdir}
%dir %{destdir}/lib
%dir %{libdir}
%{_mandir}/man8/%{name}.8.gz
%{libdir}/check-modified-files.sh

%changelog
