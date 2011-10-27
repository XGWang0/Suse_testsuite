#
# spec file for package qa_specweb (Version 0.1)
#

Name:         qa_test_specweb
#BuildRequires: ctcs2
License:      Proprietary SPEC
Group:        SuSE internal
Summary:      Specweb benchmark for ctcs framework
Provides:	specweb specweb-ctcs2-glue
Obsoletes:	specweb specweb-ctcs2-glue
Requires:     apache2 apache2-mod_perl coreutils perl ctcs2
Version:      0.1
Release:      1
Source0:      specweb-%{version}.tar.bz2
Source1:      test_specweb-run
Source2:	qa_test_specweb.8
Source3:      ctcstools-%{version}.tar.bz2
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
Specweb benchmark. Tests local web server from one local client with various number of simultaneous connections.

#%package ctcs2-glue
#Summary:        Let specweb run via ctcs2
#Group:          SuSE internal
#AutoReqProv:    on
#Requires:       ctcs2 qa_dummy
#Requires:       specweb = %{version}
#
#%description ctcs2-glue
#CTCS2 framework for specweb benchmark.
#
%prep
%setup -q -n specweb -a3
./configure
make all
rm -rf *.c *.h *.o */*.c */*.h */*.o

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools
ln -s ../%name/tcf/specweb.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
mv client $RPM_BUILD_ROOT/usr/bin/specweb-client
mv Wafgen99/wafgen99 $RPM_BUILD_ROOT/usr/bin/wafgen99
mv Cadgen99/cadgen99 $RPM_BUILD_ROOT/usr/bin/cadgen99
mv Upfgen99/upfgen99 $RPM_BUILD_ROOT/usr/bin/upfgen99
rm -rf Wafgen99
rm -rf Cadgen99
rm -rf Upfgen99
rm -rf HTTP
rm -rf test
rm -f config* Makefile* tags
mkdir $RPM_BUILD_ROOT/usr/share/qa/%name/specweb
cp -a ctcstools/* $RPM_BUILD_ROOT/usr/share/qa/%name
rm -fr ctcstools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name/specweb


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_specweb.8.gz
/usr/bin/specweb-client
/usr/bin/wafgen99
/usr/bin/cadgen99
/usr/bin/upfgen99


#%files ctcs2-glue
#%defattr(-, root, root)
%dir /usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf
/usr/share/qa/tools

%changelog
* Fri Jul 11 2008 - michalsrb@gmail.com
- package created, version 0.1
