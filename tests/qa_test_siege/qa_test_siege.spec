#
# spec file for package qa_siege (Version 2.64)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_siege
#BuildRequires:  ctcs2
License:        GPL v2 or later
Group:          System/Benchmark
AutoReqProv:    on
Version:        2.67
Release:        172
Summary:        Apache testing tool
Url:            http://www.joedog.org/index/siege-home
Source0:         siege-%{version}.tar.bz2
Source1:	ctcstools.tar.bz2
Source2:	qa_test_siege.8
Source3:	test_siege-run
Patch0:         url-patch.dif
Patch2:         config-patch.dif
Patch3:         strncat-patch.dif
#Patch4:	spinner-patch.dif
#Patch4:         threads-locks-patch.dif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	qa_siege
Obsoletes:	qa_siege
Requires:       apache2 ctcs2
Provides:       qa-siege
Obsoletes:      qa-siege
#BuildArchitectures: noarch
#ExclusiveArch: %ix86
BuildRequires:	openssl-devel

%description
This is a apache testing and benchmarking tool



%prep
%define qa_location /usr/share/qa/%{name}
%setup -n siege-%{version} -a1
%patch0 -p1
%patch2 -p1
%patch3 -p1
#%patch4 -p1
%{?suse_update_config:%{suse_update_config -f}}

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
export CCFLAGS="$RPM_OPT_FLAGS"
./configure --prefix=%{_prefix}/share/qa/qa_test_siege/siege --with-ssl=/usr/include/openssl
make CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS"i CCFLAGS="$RPM_OPT_FLAGS" 

%install
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/man/man8/
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d -v $RPM_BUILD_ROOT%{qa_location}
install -m 755 -d -v $RPM_BUILD_ROOT%{qa_location}/tcf
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/tools
cd $RPM_BUILD_DIR/siege-%{version}
make install prefix=$RPM_BUILD_ROOT%{qa_location}/siege
install -m 755 -v ctcstools/qa_siege_defaultrun.sh $RPM_BUILD_ROOT%{qa_location}
cp -v ctcstools/*.tcf $RPM_BUILD_ROOT/%{qa_location}/tcf
cp -v ctcstools/qa_siege_old.tcf $RPM_BUILD_ROOT/%{qa_location}/tcf
ln -s ../%{name}/tcf/qa_siege_http.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%{name}/tcf/qa_siege_https.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
cp -v %{S:3} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -v ctcstools/.siegerc $RPM_BUILD_ROOT/%{qa_location}
mkdir -p $RPM_BUILD_ROOT/etc/apache2/ssl.key
cp -v ctcstools/qa.key $RPM_BUILD_ROOT/etc/apache2/ssl.key/
mkdir -p $RPM_BUILD_ROOT/etc/apache2/ssl.crt/
cp -v ctcstools/qa.crt $RPM_BUILD_ROOT/etc/apache2/ssl.crt/
mkdir -p $RPM_BUILD_ROOT/etc/apache2/vhosts.d
cp -v ctcstools/00_localhost_ssl.conf $RPM_BUILD_ROOT/etc/apache2/vhosts.d/
cp -v ctcstools/index.html $RPM_BUILD_ROOT%{qa_location}
cd $RPM_BUILD_ROOT/usr/share/qa/tools
ln -s test_siege-run test_siege-run-http
ln -s test_siege-run test_siege-run-https

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{qa_location}
%dir /usr/share/qa
%dir /usr/share/qa/tools
%dir /usr/share/qa/tcf
/usr/share/qa/tcf/qa_siege_http.tcf
/usr/share/qa/tcf/qa_siege_https.tcf
%attr(0755,root,root) /usr/share/qa/tools/test_siege-run
/usr/share/qa/tools/test_siege-run-http
/usr/share/qa/tools/test_siege-run-https
%attr(0400,root,root) /etc/apache2/ssl.key/qa.key
%attr(0400,root,root) /etc/apache2/ssl.crt/qa.crt
/etc/apache2/vhosts.d/00_localhost_ssl.conf
%dir /etc/apache2/ssl.crt
%dir /etc/apache2/ssl.key
%dir /etc/apache2/vhosts.d
%dir /etc/apache2
/usr/share/man/man8/qa_test_siege.8.gz

%changelog
* Wed Aug 17 2011 - llipavsky@suse.cz
- Remove qa_dummy dependency
* Fri Aug 12 2011 - llipavsky@suse.cz
- Package rename: qa_siege -> qa_test_siege
* Mon Mar 14 2011 aguo@novell.com
- add man page of qa_test_siege
* Tue Apr 01 2008 vmarsik@suse.cz
- changed TCF to test 1,2,5,10,20,50,100,200,500 threads,20min each
* Mon Mar 31 2008 vmarsik@suse.cz
- added few more cancellation points
- changed condition wait in crew.c to a timed condition wait
- fixed a wrong pointer operation in crew_destroy()
- removed locks in crew_set_shutdown() that caused deadlocks
- changed handler.c so that crew_set_shutdown() is not called 3 times
* Mon Feb 05 2007 mmrazik@suse.cz
- added qa_dummy to Requires
* Mon Feb 05 2007 ro@suse.de
- added qa_dummy to buildreq
* Wed Jan 31 2007 mmrazik@suse.cz
- tcf file moved to a propper location
* Wed Jan 03 2007 mmrazik@suse.cz
- fixed possible strncat buffer overflows
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Nov 07 2005 fseidel@suse.de
- changed spec according to changes in ctcs2
* Fri Oct 21 2005 ro@suse.de
- rename to qa_siege, provide and obsolete old name
* Mon Oct 17 2005 fseidel@suse.de
- fully reworked version (uses upstream version 2.64)
* Wed Jun 18 2003 ro@suse.de
- added directories to filelist
* Wed Dec 11 2002 mistinie@suse.de
- Initial version
