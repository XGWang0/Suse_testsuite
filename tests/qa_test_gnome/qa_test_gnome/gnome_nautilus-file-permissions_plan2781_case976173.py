#!/usr/bin/env python
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE. All Rights Reserved.
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
# Description: Change the permissions of a file.
# Written by:  David Mulder<dmulder@novell.com>
##############################################################################

# The docstring below is used in the generated log file
"""
Right click on a file
Select Properties
Click on the Permissions tab
Change the permissions
Click on Close
"""

# imports
from strongwind import *
from gnome_frame import *
import os

def get_stdout(args):
	"""
	Return the output of a command.
	"""
	p = subprocess.Popen(args, stdout=subprocess.PIPE)
	(stdout, stdin) = p.communicate()
	return stdout

try:
	app = launchNautilus("/usr/bin/nautilus", "nautilus")
except IOError, msg:
	print "ERROR:  %s" % msg
	exit(2)
# just an alias to make things shorter
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

# Highlight the file.
procedurelogger.action('Select test from Icon View.')
icon_view = nFrame.findLayeredPane('Icon View')
test_icon = nFrame.findIcon('test')
icon_view._accessible.querySelection().selectChild(test_icon.getIndexInParent())
sleep(config.SHORT_DELAY)

# Open the properties dialog.
nFrame.findMenuBar(None).select(['File', 'Properties'])
procedurelogger.expectedResult('The Properties dialog appears.')
properties_dialog = nFrame.findDialog(re.compile('^Properties'))

# Change the file permissions.
permissions_tab = properties_dialog.findPageTab(re.compile('^Permissions'))
permissions_tab.mouseClick()
permissions_combo = permissions_tab.findComboBox(re.compile('^Read and write'))
permissions_combo.mouseClick()
read_only = permissions_tab.findMenuItem(re.compile('^Read-only'))
read_only.mouseClick()
procedurelogger.expectedResult('Change file permissions.')

# Close the properties dialog.
close_button = properties_dialog.findPushButton(re.compile('^Close'))
close_button.mouseClick()
procedurelogger.expectedResult('Close the properties dialog.')

# Verify that the file properties have been changed.
permissions = get_stdout(['ls', '-l', test_file])
assert re.search(r'-rw-r--r--')
procedurelogger.expectedResult('Verify the properties have changed.')

# Delete the test file.
os.remove(test_file)
procedurelogger.expectedResult('Delete the test file.')

# Close Nautilus
nFrame.findMenuBar(None).select(['File', 'Close'])
sleep(config.SHORT_DELAY)
app.assertClosed()


