#!/usr/bin/python
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE. All Rights Reserved.
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
setup(fill=False, weekly=False, size='1k')

# Fill the log with 1k of data and run logrotate.
fill_log(text='00000000000000000000', lines=50)
rotate_log(force=False)

# Verify the log was rotated.
assert_exists(TEST_LOG + '.1')

# Fill the log with less than 1k of data and run logrotate.
fill_log(text='00000000000000000000', lines=5)
rotate_log(force=False)

# Verify the log was not rotated.
assert_not_exists(TEST_LOG + '.2')

# Fill the log with much more than 1k of data and run logrotate.
fill_log(text='00000000000000000000', lines=1000)
rotate_log(force=False)

# Verify the log was rotated.
assert_exists(TEST_LOG + '.2')

# Delete temporary files created for the test.
cleanup()

# Exit without errors if none were encountered.
exit (0)


