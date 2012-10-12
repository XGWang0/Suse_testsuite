# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************
#
# spec file for package qa_test_llcbench (Version 0.1)
#
# Please submit bugfixes or comments via http://bugzilla.novell.com/
#

# norootforbuil
#
# spec file for package qa_test_llcbench
# Copyright (c) 2012 SUSE.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugzilla.novell.com/
#

# norootforbuild

Name:           qa_test_llcbench
License:        SUSE Proprietary
Group:          SuSE internal
AutoReqProv:    on
Version:        1.0
Release:        1
Summary:        qa_test_llcbench
Url:            http://www.novell.com/
Source0:        llcbench.tar.gz
Source1:        ctcstools-%{version}.tar.bz2
Source2:	%name.8
Source3:	test_llcbench-run
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       ctcs2 gcc blas gcc33-fortran
BuildRequires:  ctcs2 gcc
BuildArch:	noarch

%description
Low Level Architectural Characterization Benchmark Suite,
Including 3 bench mark test suites: MPBench, CacheBench, 
and BLASBench, for detail, please refer to the documents
in the package and the url below:
    http://icl.cs.utk.edu/projects/llcbench.

Author:
--------
    LLCbench was written by Philip J. Mucci of the Innovative Computing Laboratory.

#Authors:
#--------
#  Create package:
#    Jia,Yao (jyao@suse.com, SUSE Inc)
#    Oct 12, 2012

%prep
%setup -q -n llcbench -a1

%build
make linux-lam

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/llcbench
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
install -m 755 %{S:3} $RPM_BUILD_ROOT/usr/share/qa/%name
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8

cp * -arf $RPM_BUILD_ROOT/usr/share/qa/%name/llcbench
cd ctcstools
install -m 744 run/do_cachebench     $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 744 run/do_mpbench        $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 744 run/do_blasbench      $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 744 tcf/qa_llcbench.tcf   $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 744 parser/llcbenchparser $RPM_BUILD_ROOT/usr/share/qa/%{name}
ln -s ../qa_test_llcbench/qa_llcbench.tcf    $RPM_BUILD_ROOT/usr/share/qa/tcf/qa_llcbench.tcf
ln -s ../qa_test_llcbench/test_llcbench-run  $RPM_BUILD_ROOT/usr/share/qa/tools/test_llcbench-run
cd ..

find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name CVS -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)   
/usr/share/qa/%name
/usr/share/qa/tcf/qa_llcbench.tcf
/usr/share/qa/tools
/usr/share/man/man8/%{name}.8.gz
%doc COPYING

%changelog
* Tue Oct 09 2012 - jyao@suse.com
- Package (v.1.0) created automatically using qa_sdk_spec_generator

