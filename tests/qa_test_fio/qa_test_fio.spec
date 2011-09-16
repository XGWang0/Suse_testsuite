# norootforbuild

Name:			qa_test_fio
Version:		1.35
Release:		0
Summary:		Flexible I/O Tester/benchmarker
# http://brick.kernel.dk/snaps/fio-%{version}.tar.gz
Source:			fio-%{version}.tar.bz2
Source1:		qa_test_fio.8
URL:			http://freshmeat.net/projects/fio/
Group:			System/Benchmark
License:		GNU General Public License (GPL)
BuildRoot:		%{_tmppath}/build-%{name}-%{version}
Provides:	fio
Obsoletes:	fio
Requires:		gnuplot
BuildRequires:	make gcc libaio-devel
%if 0%{?suse_version} >= 1030
#BuildRequires:  licenses
Requires:       licenses
%endif

%description
fio is an I/O tool meant to be used both for benchmark and stress/hardware
verification. It has support for 4 different types of I/O engines (sync,
mmap, libaio, posixaio), I/O priorities (for newer Linux kernels), rate I/O,
forked or threaded jobs, and much more. It can work on block devices as
well as files. fio accepts job descriptions in a simple-to-understand text
format. Several example job files are included. fio displays all sorts of
I/O performance information, such as completion and submission latencies
(avg/mean/deviation), bandwidth stats, cpu and disk utilization, and more.




Authors:
--------
    Jens Axboe <jens.axboe@oracle.com>

%debug_package
%prep
%setup -q -n "fio-%{version}"

%build
%__make \
	OPTFLAGS="%{optflags}" \
	CC="%__cc" \
	prefix="%{_prefix}" \
	libdir="%{_libdir}/fio" \
	mandir="%{_mandir}"

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
%__make \
	DESTDIR="%{buildroot}" \
	prefix="%{_prefix}" \
	bindir="%{_bindir}" \
	libdir="%{_libdir}/fio" \
	mandir="%{_mandir}" \
	install

h=/usr/share/doc/licenses/md5/$(md5sum COPYING|cut -f1 -d" ")
test -e "$h" && %__ln_s -f "$h" COPYING

%clean
%__rm -rf "%{buildroot}"

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_fio.8.gz
%doc COPYING README examples
%{_bindir}/fio
%{_bindir}/fio_generate_plots
%doc %{_mandir}/man1/fio.1*
%doc %{_mandir}/man1/fio_generate_plots.1*

%changelog
# Local Variables:
# mode: rpm-spec
# tab-width: 3
# End:
