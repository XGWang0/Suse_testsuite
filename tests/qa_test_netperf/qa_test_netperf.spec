#!BuildIgnore: post-build-checks
#
# spec file for package netperf (Version 2.4.4)
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


Name:           qa_test_netperf
License:        Any Noncommercial; Any permissive
Group:          System/Benchmark
Summary:        network performance benchmark
Url:            http://www.netperf.org/qa_test_netperf/
Version:        2.4.4
Release:        69
Source0:        netperf-%{version}.tar.bz2
Source1:        ctcstools-%version.tar.bz2
Source2:        qa_test_netperf.8
Patch0:         cpu_setsize.patch
Patch1:         shebang_arr_script.patch
Patch2:  		change-hostip-in_tcf.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	netperf netperf-ctcs2-glue
Obsoletes:	netperf netperf-ctcs2-glue
Requires:       ctcs2 netperf

%description
Netperf is a benchmark that can be used to measure the performance of
many different types of networking. It provides tests for both
unidirecitonal throughput, and end-to-end latency.



Authors:
--------
    Hewlett-Packard Company

#%package ctcs2-glue
#License:        GPL v2 or later
#Summary:        netperf-ctcs2-glue package
#Group:          SUSE internal
##Group:        System/Benchmark
#AutoReqProv:    on
#Requires:       ctcs2,netperf,qa_dummy
#
#%description ctcs2-glue
#This package contains the glue for integrating netperf into the ctcs
#testing framework.



%prep
%setup -n netperf-%version -a1 
%patch0
%patch1 -p1
%patch2 -p1

%build
./configure --enable-burst
make 
cp src/netperf src/netperf-burst
cp src/netserver src/netserver-burst
./configure
make

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/bin
install -m 755 -d $RPM_BUILD_ROOT/usr/lib/netperf/bin
install -m 755 src/netperf $RPM_BUILD_ROOT/%{_bindir}
install -m 755 src/netserver $RPM_BUILD_ROOT/%{_bindir}
install -m 755 src/netperf-burst $RPM_BUILD_ROOT/%{_bindir}
install -m 755 src/netserver-burst $RPM_BUILD_ROOT/%{_bindir}
install -m 755 doc/examples/*script $RPM_BUILD_ROOT/usr/lib/netperf/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
install -D -m 755 ctcstools/test_netperf-run $RPM_BUILD_ROOT/usr/share/qa/tools/test_netperf-run
install -D -m 755 ctcstools/netperf.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/netperf.tcf

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_netperf.8.gz
/usr/bin/netperf
/usr/bin/netserver
/usr/bin/netperf-burst
/usr/bin/netserver-burst
/usr/lib/netperf/bin

#%files ctcs2-glue
#%defattr(-, root, root)
/usr/share/qa

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Oct 17 2008 yxu@suse.de
- added netperf-ctcs2-glue subpackage for QA automation
* Thu Apr 10 2008 pkirsch@suse.de
- changed group to System/Benchmark
* Mon Mar 17 2008 yxu@suse.de
- retrieved from doc example scripts of running the test
* Mon Mar 03 2008 dgollub@suse.de
- Additional netperf build with burst mode:
  netserver-burst and netperf-burst
* Thu Jan 03 2008 pkirsch@suse.de
- for glibc-devel corrected cpu_set macros
* Tue Oct 30 2007 pkirsch@suse.de
- initial package
