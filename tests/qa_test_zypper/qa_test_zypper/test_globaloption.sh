#!/bin/bash
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE. All Rights Reserved.
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

source testlib.sh
assert_root

assert_output "--help" "-h"
assert_result "-h" "Usage:"

assert_output "--version" "-V"
# Not support zypper 0.x.x, so assert output has zypper [1-9]
assert_result "-V" "zypper [1-9]"

cp /etc/zypp/zypp.conf ~/zypp.conf
assert_output "zypper --config ~/zypp.conf se $PACKAGE" "zypper -c ~/zypp.conf se $PACKAGE"
assert_result "zypper --config ~/zypp.conf se $PACKAGE" "Loading repository data..."
rm -f ~/zypp.conf

assert_output "--quiet se $PACKAGE" "-q se $PACKAGE"
no_result "-q se $PACKAGE" "Loading repository data"

assert_output "--verbose se $PACKAGE" "-v se $PACKAGE"
assert_result "-v se $PACKAGE" "Checking whether to refresh metadata for"

# TODO: Currently, zypper -A se and zypper se have same output. So later you can add zypper --no-abbrev test here if necessary...

# TODO: Add zypper --table-style test here

# TODO: Add zypper --rug-compatible test here

assert_result "--non-interactive in $PACKAGE" "Installing: $PACKAGE"
assert_result "-n rm $PACKAGE" "Removing $PACKAGE"

assert_output "--xmlout se $PACKAGE" "-x se $PACKAGE"
assert_result "-x se $PACKAGE" "xml version="

# TODO: add --reposd-dir, -D; --cache-dir, -C; --raw-cache-dir test here.

echo "Test completed successfully"

