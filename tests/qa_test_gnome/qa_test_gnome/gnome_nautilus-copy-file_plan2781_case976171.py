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
# Written by:  Calen Chen <cachen@novell.com>
# Date:        07/29/2011
# Description: Nautilus copy file Test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Nautilus Copy File===
Step1: Launch Nautilus
Step2: Click on a file in the nautlius window and drag it to the desktop while holding the Control key
Step3: A copy of the file should show up on the desktop
Step4: Click on a file with right-button, "Copy" this file to another directory
Step5: A copy of the file should show up in the appointed directory
"""

# imports
from strongwind import *
from gnome_frame import *
import os
import subprocess

print doc

home_directory = os.getenv('HOME')
test_file = os.path.join(home_directory, 'test')
test_file_copy = os.path.join(home_directory + "/Desktop", 'test')

# Step1: Launch Nautilus
try:
    app = launchNautilus("/usr/bin/nautilus", "nautilus")
except IOError, msg:
    print "ERROR:  %s" % msg
    exit(2)

# Just an alias to make things shorter.
nFrame = app.findFrame(re.compile('^%s' % os.getenv('USER')))
menubar = nFrame.findMenuBar(None)

# Remove the exist test file
if os.path.exists(test_file_copy):
    os.remove(test_file_copy)

# Create a file for copy and verify that it was created.
procedurelogger.action('Create a test file.')
f = open(test_file, 'w')
f.write('test file')
f.close()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('%s is created.' % test_file)
assert os.path.exists(test_file), 'No test file was created.'

# Change view to list
menubar.findCheckMenuItem('List', checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

# Step2: Click on a file in the nautlius window and drag it to the desktop while holding the Control key
procedurelogger.action('Focus to test file')
list_view = nFrame.findTable('List View')
test_cell = list_view.findTableCell('test', checkShowing=False)

# focus to test file
test_cell.grabFocus()
sleep(config.SHORT_DELAY)

# holding the Control key
pyatspi.Registry.generateKeyboardEvent(37, None, pyatspi.KEY_PRESS)
sleep(config.SHORT_DELAY)

# drag the test file
(x, y) = screenDimensions()
drag(test_cell, toXY=(x-40, y-40))
sleep(config.SHORT_DELAY)

# release the Control key
pyatspi.Registry.generateKeyboardEvent(37, None, pyatspi.KEY_RELEASE)
sleep(config.SHORT_DELAY)

# Step3: A copy of the file should show up on the desktop and home directory
procedurelogger.expectedResult('%s is copy to the Desktop.' % test_file_copy)
assert os.path.exists(test_file_copy), 'The file was not copied to desktop.'
assert os.path.exists(test_file), 'The file is removed from home.'

# Delete the test file.
procedurelogger.action('Delete the test file.')
os.remove(test_file_copy)
procedurelogger.expectedResult('%s was deleted.' % test_file_copy)
assert not os.path.exists(test_file_copy), 'The file was not deleted.'

# Step4: Click on a file with right-button, "Copy" this file to another directory
menubar.findMenuItem('Copy', checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

pyatspi.Registry.generateMouseEvent(x - 40, y - 40, 'b3dc')
sleep(config.SHORT_DELAY)

app.findAllWindows(None)[-1].findMenuItem('Paste').click(log=True)
sleep(config.SHORT_DELAY)

# Step5: A copy of the file should show up in the appointed directory
procedurelogger.expectedResult('%s is copy to the Desktop.' % test_file_copy)
assert os.path.exists(test_file_copy), 'The file was not copied to desktop.'
assert os.path.exists(test_file), 'The file is removed from home.'

# Change view to Icons
menubar.findCheckMenuItem('Icons', checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

# Close Nautilus
menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
nFrame.assertClosed()

# Remove test file
os.remove(test_file)
os.remove(test_file_copy)

