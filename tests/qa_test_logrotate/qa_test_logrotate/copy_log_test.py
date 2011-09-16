#!/usr/bin/python

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

