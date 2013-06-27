#!/usr/bin/python
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


import os, subprocess, time
from logrotate import *

# Skip test because this test is not compatible with SLES 11.
exit(22)

# Create dummy log and config file.
setup(dateformat=True)

# Run logrotate.
rotate_log()
time.sleep(1)
fill_log()
rotate_log()
time.sleep(1)
fill_log()
rotate_log()
time.sleep(1)
fill_log()
rotate_log()
time.sleep(1)
fill_log()
rotate_log()

# Get the filename of the oldest rotation.
rotation_list_unsorted = os.listdir(TEST_DIR)
rotation_list_unsorted.remove('test_log')
rotation_list_unsorted.remove('test_log.conf')
rotation_list_sorted = sorted(rotation_list_unsorted)
oldest_rotation = rotation_list_sorted.pop(0)

# Run logrotate.
time.sleep(1)
fill_log()
rotate_log()

# Make sure the oldest file was deleted.
assert_not_exists(os.path.join(TEST_DIR, oldest_rotation))

# Delete temporary files created for the test.
cleanup()

# Exit without errors if none were encountered.
exit (0)


