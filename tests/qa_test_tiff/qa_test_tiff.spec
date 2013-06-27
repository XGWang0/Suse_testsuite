#
# spec file for package qa_test_tiff (Version 0.1)
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild
%define qa_location /usr/share/qa/qa_test_tiff

Name:           qa_test_tiff
License:        as-is; GPL v3 or later
Group:          SuSE internal
Summary:        Unittests for tiff
Provides:	qa_tiff
Obsoletes:	qa_tiff
Requires:       bash tiff qa_lib_ctcs2
BuildRequires:  bash tiff
Version:        4.0.0beta7
Release:        21
Source0:        %name-%version.tar.bz2
Source1:        test_tiff-run
Source2:        qa_test_tiff.8
Source3:        qa_test_tiff-repack.sh
Patch0:         qa_test_tiff-skipexe.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Test cases for tiff package.


%prep
%setup -q -n %{name}-%{version}

%patch0 -p1

# tiffcp-logluv.sh: uses args that are not availible on binaries from tiff 3.
find ./ -name \*.sh | \
	grep -v tiffcp-logluv.sh | \
	sed -e 's:./::' | sort | uniq  > ./ctcs2_test_list

echo -en "#!/bin/bash\ncd %{qa_location}\nbash \$1\nexit \$?\n" > ./ctcs2_run_test.sh
chmod +x ./ctcs2_run_test.sh


%build


%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/%{qa_location}
install -m 755 -d $RPM_BUILD_ROOT/%{qa_location}/tcf
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/%{qa_location}

cat $RPM_BUILD_ROOT/%{qa_location}/ctcs2_test_list | while read test; do
	echo "timer 300"
	echo -en "fg 1 "
	echo -en "$test %{qa_location}/ctcs2_run_test.sh $test\n"
	echo -en "wait\n\n"
done > $RPM_BUILD_ROOT/usr/share/qa/tcf/qa_tiff.tcf


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
/usr/share/qa/
/usr/share/man/man8/qa_test_tiff.8.gz


%changelog
