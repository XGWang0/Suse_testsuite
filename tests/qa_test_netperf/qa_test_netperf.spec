#!BuildIgnore: post-build-checks
#
# spec file for package netperf (Version 2.4.4)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
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
License:        HP; Any Noncommercial; Any permissive
Group:          System/Benchmark
Summary:        network performance benchmark
Url:            http://www.netperf.org/netperf/
Version:        2.6.0
Release:        69
Source0:        netperf-%{version}.tar.bz2
Source1:        ctcstools-%version.tar.bz2
Source2:        qa_test_netperf.8
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
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/config/netperf
install -D -m 755 ctcstools/test_netperf-run $RPM_BUILD_ROOT/usr/share/qa/tools/test_netperf-run
install -D -m 755 ctcstools/netperf.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/netperf.tcf
install -D -m 755 ctcstools/netperf6.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/netperf6.tcf
install -D -m 755 ctcstools/qa_test_netperf-config $RPM_BUILD_ROOT/usr/lib/ctcs2/config/netperf/qa_test_netperf-config
install -D -m 755 ctcstools/netperf-client $RPM_BUILD_ROOT/usr/lib/ctcs2/config/netperf/netperf-client
install -D -m 755 ctcstools/netperf-client_all_size $RPM_BUILD_ROOT/usr/lib/ctcs2/config/netperf/netperf-client_all_size
install -D -m 755 ctcstools/netperf-server $RPM_BUILD_ROOT/usr/lib/ctcs2/config/netperf/netperf-server
install -D -m 755 ctcstools/netperf_peer_loop-run $RPM_BUILD_ROOT/usr/share/qa/tools/netperf_peer_loop-run
install -D -m 755 ctcstools/netperf_peer_loop_tcp-run $RPM_BUILD_ROOT/usr/share/qa/tools/netperf_peer_loop_tcp-run
install -D -m 755 ctcstools/netperf_peer_loop_udp-run $RPM_BUILD_ROOT/usr/share/qa/tools/netperf_peer_loop_udp-run
install -D -m 755 ctcstools/netperf_peer_loop_tcp-run6 $RPM_BUILD_ROOT/usr/share/qa/tools/netperf_peer_loop_tcp-run6
install -D -m 755 ctcstools/netperf_peer_loop_udp-run6 $RPM_BUILD_ROOT/usr/share/qa/tools/netperf_peer_loop_udp-run6
install -D -m 755 ctcstools/netperf_peer_loop_allsizes-run $RPM_BUILD_ROOT/usr/share/qa/tools/netperf_peer_loop_allsizes-run
install -D -m 755 ctcstools/netperf_peer_loop_allsizes-run6 $RPM_BUILD_ROOT/usr/share/qa/tools/netperf_peer_loop_allsizes-run6
install -D -m 755 ctcstools/netperf-peer-loop.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/netperf-peer-loop.tcf
install -D -m 755 ctcstools/netperf_peer_loop-run6 $RPM_BUILD_ROOT/usr/share/qa/tools/
install -D -m 755 ctcstools/netperf-peer-fiber-run $RPM_BUILD_ROOT/usr/share/qa/tools/
install -D -m 755 ctcstools/netperf-peer-fiber-run6 $RPM_BUILD_ROOT/usr/share/qa/tools/
install -D -m 755 ctcstools/netperf-peer-fiber-tcp-run $RPM_BUILD_ROOT/usr/share/qa/tools/
install -D -m 755 ctcstools/netperf-peer-fiber-tcp-run6 $RPM_BUILD_ROOT/usr/share/qa/tools/
install -D -m 755 ctcstools/netperf-peer-fiber-udp-run $RPM_BUILD_ROOT/usr/share/qa/tools/
install -D -m 755 ctcstools/netperf-peer-fiber-udp-run6 $RPM_BUILD_ROOT/usr/share/qa/tools/
install -D -m 755 ctcstools/netperf-peer-fiber-server $RPM_BUILD_ROOT/usr/share/qa/tools/
install -D -m 755 ctcstools/netperf-peer-fiber-server6 $RPM_BUILD_ROOT/usr/share/qa/tools/

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
/usr/lib/ctcs2

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Oct 25 2011 cachen@suse.com
- remove change-hostip-in_tcf.diff; add configuration file
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
