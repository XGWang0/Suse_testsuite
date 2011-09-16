#!/usr/bin/python

import os, subprocess
from logrotate import *

# Create dummy log and config file.
setup(ifempty=True)

# Run logrotate without filling the log.
rotate_log()
rotate_log()
rotate_log()
rotate_log()
rotate_log()
rotate_log()

# Make sure the rotations were created.
assert_exists(TEST_LOG + '.1')
assert_exists(TEST_LOG + '.2')
assert_exists(TEST_LOG + '.3')
assert_exists(TEST_LOG + '.4')
assert_exists(TEST_LOG + '.5')

# Delete temporary files created for the test.
cleanup()

# Exit without errors if none were encountered.
exit (0)

