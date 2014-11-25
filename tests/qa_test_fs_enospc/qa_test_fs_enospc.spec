# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
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
#
# spec file for package qa_fs_enospc (Version 0.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_fs_enospc
License:        SUSE Proprietary
#BuildRequires:  ctcs2
Group:          SUSE internal
Summary:        file system stress test
Provides:	qa_fs_enospc
Obsoletes:	qa_fs_enospc
Requires:       ctcs2
Requires:       fs_mark
Version:        0.1
Release:        2
Source0:        %{name}-%{version}.tar.bz2
Source1:        fs_enospc-btrfs.tcf
Source2:        test_fs_enospc-btrfs-run
Source3:        qa_test_fs_enospc.8
Source4:        test_fs_enospc-run
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
Filesystem tests for ENOSPC conditions

%prep
%setup -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
cp %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tcf
cp %{S:4} $RPM_BUILD_ROOT/usr/share/qa/tools
ln -s ../../../share/qa/tcf/fs_enospc-btrfs.tcf $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
cp %{S:2} $RPM_BUILD_ROOT/usr/share/qa/%name/
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_fs_enospc.8.gz
/usr/share/qa
/usr/share/qa/%name/*
/usr/lib/ctcs2
%attr (0755, root, root) /usr/share/qa/tools/test_fs_enospc-run
%doc COPYING
