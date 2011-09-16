#
# spec file for package qa_cabextract (Version 0.1)
#
# Copyright (c) 2006 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_cabextract
License:        GPL
Group:          SuSE internal
Summary:        Simple cabextract tests for ctcs framework
Provides:	qa_cabextract
Obsoletes:	qa_cabextract
Requires:       cabextract ctcs2
BuildRequires:  ctcs2 
Version:        0.1
Release:        1
Source0:        %name-%version.tar.bz2
Source1:        qa_cabextract.tcf
Source2:        test_cabextract-run
Source3:	qa_test_cabextract.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Test cases for cabextract package. Test archive uncompression.



Authors:
--------
    Lukas Lipavsky <llipavsky@suse.cz>

%prep
%setup -q -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/qa_cabextract.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_cabextract.8.gz
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/qa_cabextract.tcf
/usr/share/qa/tools/test_cabextract-run

%changelog -n qa_test_cabextract
* Wed Aug 10 2011 - llipavsky@suse.cz
- Package rename: qa_cabextract -> qa_test_cabextract
* Mon Sep 11 2006 - lukas@suse.cz
- Initial import
