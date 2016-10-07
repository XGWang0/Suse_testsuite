#
# spec file for package qa_test_tiff
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
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


%define qa_location %{_datadir}/qa/%{name}
Name:           qa_test_tiff
Version:        4.0.0beta7
Release:        0
Summary:        Unittests for tiff
License:        as-is and GPL v3 or later
Group:          SUSE internal
Source0:        %{name}-%{version}.tar.bz2
Source1:        test_tiff-run
Source2:        qa_test_tiff.8
Source3:        qa_test_tiff-repack.sh
Patch0:         qa_test_tiff-skipexe.patch
BuildRequires:  bash
BuildRequires:  tiff
Requires:       bash
Requires:       qa_lib_ctcs2
Requires:       tiff
Provides:       qa_tiff
Obsoletes:      qa_tiff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
Test cases for tiff package.

%prep
%setup -q
%patch0

# tiffcp-logluv.sh: uses args that are not availible on binaries from tiff 3.
find ./ -name \*.sh | \
	grep -v tiffcp-logluv.sh | \
	sed -e 's:./::' | sort | uniq  > ./ctcs2_test_list

echo -en "#!/bin/bash\ncd %{qa_location}\nbash \$1\nexit \$?\n" > ./ctcs2_run_test.sh
chmod +x ./ctcs2_run_test.sh

%build

%install
install -m 755 -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8
install -m 755 -d %{buildroot}%{_datadir}/qa/tcf
install -m 755 -d %{buildroot}%{_datadir}/qa/tools
install -m 755 -d %{buildroot}/%{qa_location}
install -m 755 -d %{buildroot}/%{qa_location}/tcf
install -m 755 %{SOURCE1} %{buildroot}%{_datadir}/qa/tools
cp -a * %{buildroot}/%{qa_location}

cat %{buildroot}/%{qa_location}/ctcs2_test_list | while read test; do
	echo "timer 300"
	echo -en "fg 1 "
	echo -en "$test %{qa_location}/ctcs2_run_test.sh $test\n"
	echo -en "wait\n\n"
done > %{buildroot}%{_datadir}/qa/tcf/qa_tiff.tcf

%files
%defattr(-, root, root)
%{_datadir}/qa/
%{_mandir}/man8/qa_test_tiff.8%{ext_man}

%changelog
