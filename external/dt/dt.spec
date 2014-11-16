#
# spec file for package dt (Version 0.21)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           dt
Version:        17.25
Release:        1
License:        BSD-2-Clause
Summary:        Generic data test program
Url:            http://home.comcast.net/~SCSIguy/SCSI_FAQ/RMiller_Tools/dt.html
Group:          Hardware/Other
Source:         dt-source.tar.bz2
Source1:        dt.man
Source2:        dt.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
dt is a generic data test program used to verify proper operation of
peripherals, file systems, device drivers, or any data stream supported
by the operating system.  In its simplest mode of operation, dt writes
and then verifys its default data pattern, then displays performance
statisics and other test parameters before exiting.  Since verification
of data is performed, dt can be thought of as a generic diagnostic tool.

%package doc
License:        BSD-like
Summary:        Documentation for dt
Group:          Documentation
Requires:       dt = %{version}

%description doc
This package provide user documentation for dt.

%prep
%setup -n dt-%{version}

%build
make PORG="%{optflags}" -f Makefile.linux

%install
install -m 755 -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8
gzip %{buildroot}%{_mandir}/man8/%{name}.8
install -d %{buildroot}/%{_bindir}
install -m 755 dt %{buildroot}/%{_bindir}
install -d %{buildroot}/%{_mandir}/man1
install -m 644 %{SOURCE1} %{buildroot}/%{_mandir}/man1/dt.1
install -d %{buildroot}/%{_docdir}/%{name}/examples
install -m 755 Scripts/DiskTests.ksh %{buildroot}%{_docdir}/%{name}/examples
install -m 644 Documentation/{dt-UsersGuide.htm,dt-UsersGuide.pdf,dt-UseCases.pdf} %{buildroot}%{_docdir}/%{name}

%files
%defattr(-, root, root)
%{_mandir}/man8/dt.8.gz
%attr(755,root,root) %{_bindir}/dt
%doc %{_mandir}/man1/dt.1.gz

%files doc
%defattr(-, root, root)
%dir %{_docdir}/%{name}
%dir %{_docdir}/%{name}/examples
%doc %{_docdir}/%{name}/dt-UsersGuide.htm
%doc %{_docdir}/%{name}/dt-UsersGuide.pdf
%doc %{_docdir}/%{name}/dt-UseCases.pdf
%doc %{_docdir}/%{name}/examples/DiskTests.ksh
