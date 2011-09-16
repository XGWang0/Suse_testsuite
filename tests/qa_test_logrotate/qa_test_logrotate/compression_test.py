#!/usr/bin/python

import os, subprocess
from logrotate import *

# Create dummy log and config file.
setup(compress=True)

# Run logrotate.
rotate_log()

# Verify that the log was rotated and compressed in a zip file.
zipped_file = TEST_LOG + '.1.gz'
assert_exists(zipped_file)
unzip(zipped_file)
rotated_file = TEST_LOG + '.1'
assert_exists(rotated_file)
assert_contains('First rotation.', file_name=rotated_file)

# Delete temporary files created for the test.
cleanup()

# Exit without errors if none were encountered.
exit (0)
