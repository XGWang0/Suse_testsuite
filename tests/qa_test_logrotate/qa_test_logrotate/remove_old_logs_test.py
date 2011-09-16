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
fill_log(text='Sixth rotation.')
rotate_log()

#Verify the correct log was removed.
first_log = TEST_LOG + '.6'
assert_not_exists(first_log)

# Delete temporary files created for the test.
cleanup()

# Exit without errors if none were encountered.
exit (0)

