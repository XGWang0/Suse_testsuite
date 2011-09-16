#!/usr/bin/python

import os, subprocess
from logrotate import *

# Create dummy log and config file.
setup(notifempty=True)

# Run logrotate.
rotate_log()

# Verify the first rotation was created.
assert_exists(TEST_LOG + '.1')

# Run logrotate a few times without filling the log.
rotate_log()
rotate_log()
rotate_log()
rotate_log()
rotate_log()

# Make sure the log wasn't rotated.
assert_not_exists(TEST_LOG + '.2')

# Delete temporary files created for the test.
cleanup()

# Exit without errors if none were encountered.
exit (0)

