#!/usr/bin/env python

##############################################################################
# Description: Move a file from nautilus to the trash.
# Written by:  David Mulder<dmulder@novell.com>
##############################################################################

# The docstring below is used in the generated log file
"""
Drag a file to the Trash icon on the desktop.
"""

# imports
from strongwind import *
from gnome_frame import *
import os

try:
	app = launchNautilus("/usr/bin/nautilus", "nautilus")
except IOError, msg:
	print "ERROR:  %s" % msg
	exit(2)
# Just an alias to make things shorter.
username = os.getenv('USER')
nFrame = app.findFrame(re.compile('^%s' % username))

# Create a file for moving and verify that it was created.
procedurelogger.action('Create a test file.')
home_directory = os.getenv('HOME')
test_file = os.path.join(home_directory, 'test')
f = open(test_file, 'w')
f.write('test file')
f.close()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult('%s is created.' % test_file)
assert os.path.exists(test_file), 'No test file was created.'

# Drag the file to the Trash
nFrame.findMenu('View').mouseClick()
sleep(config.SHORT_DELAY)
nFrame.findCheckMenuItem('List').mouseClick()
sleep(config.SHORT_DELAY)
test_icon = nFrame.findTableCell('test')
trash = nFrame.findTableCell('Trash')

test_icon.grabFocus()
sleep(config.SHORT_DELAY)

drag(test_icon, trash)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult('%s is deleted.' % test_file)
assert not os.path.exists(test_file)

# Close Nautilus
nFrame.findMenu('View').mouseClick()
sleep(config.SHORT_DELAY)
nFrame.findCheckMenuItem('Icons').mouseClick()
sleep(config.SHORT_DELAY)

nFrame.findMenuBar(None).select(['File', 'Close'])
sleep(config.SHORT_DELAY)
nFrame.assertClosed()

