#!/bin/sh
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

set -x

# Copy all the tests to /tmp and make the directory writable.
mkdir -p /tmp/qa_test_coreutils || exit 1
cp -r /usr/share/qa/qa_test_coreutils/* /tmp/qa_test_coreutils || exit 1
chown -R nobody /tmp/qa_test_coreutils || exit 1

# Create a small virtual partition for tests that need one.
dd if=/dev/zero of=/tmp/qa_coreutils_tmpfs bs=1k count=65535 || exit 1
yes | mkfs -t ext2 /tmp/qa_coreutils_tmpfs || exit 1
mkdir /tmp/qa_coreutils_mnt || exit 1
mount -t ext2 -o loop /tmp/qa_coreutils_tmpfs /tmp/qa_coreutils_mnt || exit 1
chown -R nobody.users /tmp/qa_coreutils_mnt || exit 1

# Create a full virtual partition for tests that need one.
dd if=/dev/zero of=/tmp/qa_coreutils_full_tmpfs bs=1k count=1024 || exit 1
yes | mkfs -t ext2 /tmp/qa_coreutils_full_tmpfs || exit 1
mkdir /tmp/qa_coreutils_full_mnt || exit 1
mount -t ext2 -o loop /tmp/qa_coreutils_full_tmpfs /tmp/qa_coreutils_full_mnt || exit 1
dd if=/dev/zero of=/tmp/qa_coreutils_full_mnt/zero
chown -R nobody.users /tmp/qa_coreutils_full_mnt || exit 1

# Always succeed.
exit 0

