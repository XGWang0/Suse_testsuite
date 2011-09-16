#
# spec file for package qa_test_yast2 (Version 0.1)
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_yast2
BuildRequires:  ctcs2 gcc-c++ xorg-x11-devel
License:        GPL v2 or later
Group:          SuSE internal
AutoReqProv:    on
Version:        0.1
Release:        130
Summary:        RD-QA internal yast2-gui-testingset
Url:            http://w3.suse.de/~fseidel
Source0:        %name-%version.tar.bz2
Source1:        qa_yast2.tcf
Source2:        test_yast2-run	
Source3:        qa_test_yast2.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	qa_yast2
Obsoletes:	qa_yast2
Requires:       yast2 yast2-qt yast2-packagemanager yast2-online-update

%description
Test of YaST online update (so far)



Authors:
--------
    fseidel@suse.de

%prep
rm -rvf $RPM_BUILD_DIR/%{name}-%{version}
tar -xjvf %SOURCE0 -C $RPM_BUILD_DIR

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CCFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
export LIBDIR=%{_lib}
cd qa_test_yast2/xmacro
%{__make} clean
%{__make} xmacroplay

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
ln -s ../%name/tcf/qa_yast2.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cd $RPM_BUILD_DIR
cp -rv %{name} $RPM_BUILD_ROOT/usr/share/qa/

%clean
%{__rm} -rvf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_yast2.8.gz
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf
/usr/share/qa/tools

%changelog
* Thu Aug 11 2011 - llipavsky@suse.cz
- Package rename: qa_yast2 -> qa_test_yast2
* Mon Dec 03 2007 - llipavsky@suse.cz
- fixed to work with gcc 4.3
* Mon Jul 17 2006 - llipavsky@suse.cz
- fixed to comply with QA Packaging Guidelines
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Jan 19 2006 - kmachalkova@suse.cz
- fixed tcf location (updated Packaging Guidelines)
- fixed run-script location (updated Packaging Guidelines)
* Thu Jan 05 2006 - kmachalkova@suse.cz
- added support for ctcs2
* Wed Sep 07 2005 - fseidel@suse.de
- initial release
