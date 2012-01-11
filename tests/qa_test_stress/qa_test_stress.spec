#
# spec file for package stress (Version 1.0.1)
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
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



Name:           qa_test_stress
Url:            http://weather.ou.edu/~apw/projects/stress/
License:        GPL v2 or later
#BuildRequires:  
Group:          SUSE internal
Summary:        Simple workload generator for POSIX systems
#Requires:       perl
#Requires:       ctcs2
PreReq:			%install_info_prereq
Version:        1.0.4
Release:        1
Source0:        stress-%{version}.tar.bz2
Source1:        stress.py
Source2:        %{name}.8
Provides:	qa_stress
Obsoletes:	qa_stress
Requires:       ctcs2 >= 0.1.6
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#BuildArch:      i386

%description
Stress is a simple workload generator for POSIX systems.
It imposes a configurable amount of CPU, memory, I/O, and
disk stress on the system.

%prep
%setup -T -b 0 -n stress-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export CFLAGS
%{configure}
%{__make}

%install
%{__install} -m 755 -d $RPM_BUILD_ROOT/usr/bin
%{__install} -m 755 src/stress $RPM_BUILD_ROOT/usr/bin/
%{__strip} -s $RPM_BUILD_ROOT/usr/bin/stress
%{__install} -m 755 -d $RPM_BUILD_ROOT%{_infodir}
%{__install} -m 644 doc/stress.info $RPM_BUILD_ROOT%{_infodir}/
%{__install} -m 755 -d $RPM_BUILD_ROOT%{_mandir}
%{__install} -m 755 -d $RPM_BUILD_ROOT%{_mandir}/man1
%{__install} -m 644 doc/stress.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%{__install} -m 755 -d $RPM_BUILD_ROOT/usr/share/qa
%{__install} -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
%{__install} -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
%{__install} -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%{name}
%{__install} -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf

echo -e "#!/bin/sh\n\n/usr/lib/ctcs2/tools/run /usr/share/qa/tcf/stress.tcf" > $RPM_BUILD_ROOT/usr/share/qa/tools/test_stress-run
echo -e "timer 86400\nfg 1 stress /usr/bin/stress.py\nwait\n" > $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf/stress.tcf
ln -s ../%{name}/tcf/stress.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%{__install} -m 755 -d $RPM_BUILD_ROOT%{_mandir}/man8
%{__install} -m 644 %{S:2} $RPM_BUILD_ROOT%{_mandir}/man8/
gzip $RPM_BUILD_ROOT%{_mandir}/man8/%{name}.8

%{__install} -m 755 $RPM_SOURCE_DIR/stress.py $RPM_BUILD_ROOT/usr/bin



%post
%install_info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz


%postun
%install_info_delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz


%clean

%files
%defattr(-, root, root)
%attr (0755, root, root) %{_bindir}/stress
%attr (0644, root, root) %{_infodir}/stress.info.gz
%attr (0644, root, root) %{_mandir}/man1/stress.1.gz
%attr (0644, root, root) %{_mandir}/man8/%{name}.8.gz

/usr/share/qa
%attr (0755, root, root) /usr/share/qa/tools/test_stress-run
%attr (0755, root, root) /usr/bin/stress.py


%changelog
* Fri Aug 12 2011 - llipavsky@suse.cz
- Package rename: qa_stress -> qa_test_stress
