#!/usr/bin/python

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

