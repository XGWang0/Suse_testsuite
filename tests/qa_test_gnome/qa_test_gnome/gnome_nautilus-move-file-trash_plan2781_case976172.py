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


