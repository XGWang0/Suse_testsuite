#!/usr/bin/python

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

