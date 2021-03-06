#
# spec file for package qa_test_numbench
# Copyright (c) 2013 Novell, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugzilla.novell.com/
#

# norootforbuild

Name:           qa_test_numbench
License:        SUSE Proprietary
Group:          SuSE internal
AutoReqProv:    on
Version:        0.1
Release:        1
Summary:        simple benchmark for CPU test.
Url:            http://www.novell.com/
Source0:        %name-%version.tar.bz2
Source1:        qa_numbench.tcf
Source2:        test_numbench-run
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       qa_lib_ctcs2 >= 2.4.0
Requires:	qa_lib_perl
BuildRequires:  qa_lib_ctcs2 >= 2.4.0 

%description
    Author : Junwei Hao (jhao@suse.com)
run 5 iterative algorithms(like fibonacci sequence)
calculate every CPU cost measured by seconds:


%prep
%setup -q -n %{name}

%install
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
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
/usr/share/qa
%attr(0755,root,root) /usr/share/qa/%name/*.py
%attr(0755,root,root) /usr/share/qa/%name/numbenchparser

%changelog
* Mon May 21 2012 - nobody@novell.com
- Package (v.0.1) created automatically using spec_generator

