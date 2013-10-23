#
# spec file for package dt (Version 0.21)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Url:            http://home.comcast.net/~SCSIguy/SCSI_FAQ/RMiller_Tools/dt.html
Name:           dt
License:		Robin's Nest Software
Group:          Hardware/Other
AutoReqProv:    on
Version:        17.25
Release:        1
Summary:        Generic data test program
Source:         http://home.comcast.net/~SCSIguy/SCSI_FAQ/RMiller_Tools/ftp/dt/dt-source.tar.gz
Source1:        dt.man
Source2:	dt.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
dt is a generic data test program used to verify proper operation of
peripherals, file systems, device drivers, or any data stream supported
by the operating system.  In its simplest mode of operation, dt writes
and then verifys its default data pattern, then displays performance
statisics and other test parameters before exiting.  Since verification
of data is performed, dt can be thought of as a generic diagnostic tool.

Authors:
--------
    Robin Miller <Robin.Miller@netapp.com>

%package doc
License:		SUSE Proprietary
Group:          Documentation
Summary:        Documentation for dt
Requires:       dt = %{version}

%description doc
This package provide user documentation for dt.

%prep
%setup -n dt-%{version}

%build
make PORG="$RPM_OPT_FLAGS" -f Makefile.linux

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d $RPM_BUILD_ROOT/%{_bindir}
install -m 755 dt $RPM_BUILD_ROOT/%{_bindir}
install -d $RPM_BUILD_ROOT/%{_mandir}/man1
install -m 644 %{S:1} $RPM_BUILD_ROOT/%{_mandir}/man1/dt.1
install -d $RPM_BUILD_ROOT/%{_docdir}/%{name}/examples
install -m 755 DiskTests.ksh $RPM_BUILD_ROOT%{_docdir}/%{name}/examples

%files
%defattr(-, root, root)
/usr/share/man/man8/dt.8.gz
%attr(755,root,root) %{_bindir}/dt
%doc %{_mandir}/man1/dt.1.gz

%files doc
%defattr(-, root, root)
%dir %{_docdir}/%{name}
%dir %{_docdir}/%{name}/examples
%doc dt-UsersGuide.htm dt-UsersGuide.pdf dt-UseCases.pdf
%doc %{_docdir}/%{name}/examples/DiskTests.ksh

%changelog


