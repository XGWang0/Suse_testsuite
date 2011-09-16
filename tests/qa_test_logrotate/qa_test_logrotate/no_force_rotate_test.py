#!/usr/bin/python

import os, subprocess
from logrotate import *

# Create dummy log and config file.
setup()

# Run logrotate.
rotate_log()
fill_log(text='Second rotation.')
rotate_log(force=False)
fill_log(text='Third rotation.')
rotate_log(force=False)
fill_log(text='Fourth rotation.')
rotate_log(force=False)
fill_log(text='Fifth rotation.')
rotate_log(force=False)

# Verify the log was not rotated on 2nd, 3rd, 4th, and 5th attempts.
assert_contains('Second rotation.')
rotated_log = TEST_LOG + '.1'
assert_contains('First rotation.', file_name=rotated_log)
assert_exists(rotated_log)
no_rotation = TEST_LOG + '.2'
assert_not_exists(no_rotation)

# Delete temporary files created for the test.
cleanup()

# Exit without errors if none were encountered.
exit (0)
