# ****************************************************************************
# Copyright (c) 2014 Unpublished Work of SUSE. All Rights Reserved.
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
# spec file for package qa_dovecot (Version 0.2)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_dovecot
License:        GPL v2 or later
Group:          System/Packages
Summary:        Basic dovecot tests for ctcs framework
Provides:	qa_dovecot
Obsoletes:	qa_dovecot
Requires:       dovecot libqainternal ctcs2
AutoReqProv:    on
Version:        0.2
Release:        192
Source0:        %name-%version.tar.bz2
Source1:        qa_dovecot.tcf
Source2:        test_dovecot-run	
Source3:        README
Source4:	qa_test_dovecot.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
%define qa_location /usr/share/qa/%{name}

%description
Testcases for dovecot package. Tests start, restart and stop of the
service (so far)



%prep
%setup -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}
cp -rv * $RPM_BUILD_ROOT/%{qa_location}
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/tcf
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/doc
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tools
cp %{SOURCE1} $RPM_BUILD_ROOT/%{qa_location}/tcf
ln -s ../%name/tcf/qa_dovecot.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp %{SOURCE3} $RPM_BUILD_ROOT%{qa_location}/doc
find $RPM_BUILD_ROOT/%{qa_location} -type f ! -name "README" ! -name "COPYING" ! -name "*.tcf" | xargs chmod +x

%clean
rm -rvf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)   
/usr/share/man/man8/qa_test_dovecot.8.gz
%{qa_location}
/usr/share/qa
%doc COPYING

%changelog
