#!/usr/bin/python

import os, subprocess
from logrotate import *

# Create dummy log and config file.
setup()

# Run logrotate.
rotate_log()
fill_log(text='Second rotation.')
rotate_log()
fill_log(text='Third rotation.')
rotate_log()
fill_log(text='Fourth rotation.')
rotate_log()
fill_log(text='Fifth rotation.')
rotate_log()

#Verify the logs were rotated correctly.
assert_rotated(1, 'Fifth rotation.')
assert_rotated(2, 'Fourth rotation.')
assert_rotated(3, 'Third rotation.')
assert_rotated(4, 'Second rotation.')
assert_rotated(5, 'First rotation.')

# Delete temporary files created for the test.
cleanup()

# Exit without errors if none were encountered.
exit (0)
