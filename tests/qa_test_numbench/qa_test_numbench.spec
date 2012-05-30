#
# spec file for package qa_test_numbench
# Copyright (c) 2010 Novell, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugzilla.novell.com/
#

# norootforbuild

Name:           qa_test_numbench
License:        GPL v2 or later
Group:          OpenSUSE
AutoReqProv:    on
Version:        0.1
Release:        1
Summary:        qa_test_numbench
Url:            http://www.novell.com/
Source0:        %name-%version.tar.gz
Source1:        qa_numbench.tcf
Source2:        test_numbench-run
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       ctcs2 
BuildRequires:  qa_lib_ctcs2 >= 2.4.0 ctcs2 

%description
    Author : Put your name here
No description

%prep
cd $RPM_SOURCE_DIR
tar -zxvf %name-%version.tar.gz
%setup -q -n %{name}

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/qa_numbench.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name CVS -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)   
/usr/share/qa/%name
/usr/share/qa/tcf/qa_numbench.tcf
/usr/share/qa/tools/test_numbench-run

%changelog
* Mon May 21 2012 - nobody@novell.com
- Package (v.0.1) created automatically using spec_generator

