#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************
#


##############################################################################
# Description: Move a file from nautilus to the desktop.
# Written by:  David Mulder<dmulder@novell.com>
##############################################################################

# The docstring below is used in the generated log file
"""
Click on a file in the Nautilus window and drag it to the desktop.
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
nFrame = app.findFrame(re.compile('^%s' % os.getenv('USER')))

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

# Drag the test file to the Desktop.
procedurelogger.action('Drag the test file to the Desktop.')
test_icon = nFrame.findIcon('test')
test_icon._accessible.querySelection().selectChild(test_icon.getIndexInParent())
(x, y) = screenDimensions()
drag(test_file, toXY=(x-40, y-40))
desktop_directory = os.path.join(home_directory, 'Desktop')
test_file = os.path.join(desktop_directory, 'test')
test_directory = os.path.join(test_directory, 'Desktop')
test_file = os.path.join(test_directory, 'test')
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult('%s is moved to the Desktop.' % test_file)
assert os.path.exists(test_file), 'The file was not moved.'

# Delete the test file.
procedurelogger.action('Delete the test file.')
os.remove(test_file)
procedurelogger.expectedResult('%s was deleted.', test_file)
assert not os.path.exists(test_file), 'The file was not deleted.'

# Close Nautilus
nFrame.findMenuBar(None).select(['File', 'Close'])
sleep(config.SHORT_DELAY)
nFrame.assertClosed()


