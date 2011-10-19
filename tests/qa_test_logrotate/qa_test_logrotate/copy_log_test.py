#!/usr/bin/python
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


import os, subprocess
from logrotate import *

# Create dummy log and config file.
setup(copy=True)

# Run logrotate.
rotate_log()

# Verify that the log and the rotated log contain the same data.
assert_contains('First rotation.')
first_rotation = TEST_LOG + '.1'
assert_contains('First rotation.', file_name=first_rotation)

# Run logrotate.
fill_log(text='Second rotation.')
rotate_log()

# Verify that the log contains both 1st and 2nd rotation text.
assert_contains('First rotation.')
assert_contains('Second rotation.')

# Verify that first rotation also contains both 1st and 2nd rotation text.
assert_contains('First rotation.', file_name=first_rotation)
assert_contains('Second rotation.', file_name=first_rotation)

# Verify that second rotation contains only the 1st rotation text.
second_rotation = TEST_LOG + '.2'
assert_contains('First rotation.', file_name=second_rotation)
assert_not_contains('Second rotation.', file_name=second_rotation)

# Delete temporary files created for the test.
cleanup()

# Exit without errors if none were encountered.
exit (0)


