#
# spec file for package qa_test_java-1_4_2-ibm (Version 1.0.2)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/

##### WARNING #####
# Generated by qa-test-generator.sh so please consider fix it and regenerate
# those packages, instead of changing this one directly
#
# http://git.suse.de/ibmjava/ibmjava/blobs/master/qa/qa-test-generator.sh
#
##### WARNING #####

# tested package name
%define tpname  java-1_4_2-ibm

# QA automation dirs
%define destdir %{_datadir}/qa
%define tcfdir %{destdir}/tcf
%define ptcfdir %{destdir}/%{name}/tcf
%define toolsdir %{destdir}/tools
%define confdir /etc/qa

Name:           qa_test_%{tpname}
License:	GPL v2 or later
Group:          SuSE internal
Version:        1.0.2
Release:        1
Summary:        QA test for %{tpname}
Url:            http://qit.suse.de/ibmjava/ibmjava/blobs/master/qa/
Source0:        qa_%{tpname}.tcf
Source1:        test_%{tpname}-run
Source2:        check-modified-files.sh
Source3:        %{name}.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
BuildRequires:  qa_lib_ibmjava
Requires:       qa_lib_ibmjava

%description
QA test for %{tpname} - check if package matches the original tarball
content. Use the qa_lib_ibmjava script.

%prep
#nothing to do

%build
#nothing to do

%install
install -m 0755 -d %{buildroot}%{_mandir}/man8
install -m 0644 %{SOURCE3} %{buildroot}%{_mandir}/man8

install -m 755 -d %{buildroot}%{tcfdir}
install -m 755 -d %{buildroot}%{toolsdir}
install -m 755 -d %{buildroot}%{ptcfdir}
install -m 755 -d %{buildroot}%{destdir}/%{name}

install -m 644 %{SOURCE0} %{buildroot}%{ptcfdir}
ln -s ../%{name}/tcf/qa_%{tpname}.tcf %{buildroot}%{tcfdir}

install -m 755 %{SOURCE1} %{buildroot}%{toolsdir}

install -m 755 %{SOURCE2} %{buildroot}%{destdir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root,0755)
%dir %{destdir}/%{name}
%dir %{ptcfdir}
%dir %{tcfdir}
%dir %{toolsdir}
%{ptcfdir}/qa_%{tpname}.tcf
%{tcfdir}/qa_%{tpname}.tcf
%{toolsdir}/test_%{tpname}-run
%{_mandir}/man8/%{name}.8.gz
%{destdir}/%{name}/check-modified-files.sh

%changelog
