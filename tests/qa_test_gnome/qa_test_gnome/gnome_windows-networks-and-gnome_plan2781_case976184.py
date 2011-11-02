#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE. All Rights Reserved.
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
# Written by: Calen Chen <cachen@novell.com>
# Date:        05/30/2011
# Description: Windows networks and GNOME Test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Windows netowrks and GNOME===
Step1: Open Nautilus, click Go -> Network
Step2: Make sure nautilus frame is updated to 'Network - File Browser', 
location text is updated to 'network:///', Content View is updated to 
show SMB servers
Step3: Double-click 'Windows Network' icon to see workgroups in the network
Step4: Make sure nautilus frame is updated to 'Windows Network - File Browser',
location text is updated to 'smb:///', Content View is updated to show workgroup
Step5: Double-click the default workgroup icon which is determined by "workgroup"
key under [global] in /etc/samba/smb.conf
Step6: See a list of the servers in that workgroup
"""

# imports
from strongwind import *
from gnome_frame import *
import os

print doc

# Launch Nautilus
try:
	app = launchNautilus("/usr/bin/nautilus", "nautilus")
except IOError, msg:
	print "ERROR:  %s" % msg
	exit(2)

# just an alias to make things shorter
who = os.getenv("USER")
nFrame = app.findFrame(re.compile('^%s' % who))

# Step1: Open Nautilus, click Go -> Network
nFrame.findMenuBar(None).select(['Go', 'Network'])
sleep(config.MEDIUM_DELAY)

content_view = nFrame.findScrollPane("Content View")
icon_view = content_view.findLayeredPane("Icon View")

# Step2: Make sure nautilus frame is updated to 'Network - File Browser', 
# location text is updated to 'network:///', Content View is updated to 
# show SMB servers
expect_name = "Network - File Browser"
expect_text = "network:///"

procedurelogger.expectedResult("Make sure nautilus frame is updated to " + expect_name)
assert nFrame.name == expect_name, \
                 "frame name expect: %s, actual: %s" % (expect_name, nFrame.name)

procedurelogger.expectedResult("Make sure location text is updated to " + expect_text)
l_text = nFrame.findText(None)
assert l_text.text == expect_text, \
                 "location text expect: %s, actual: %s" % (expect_text, l_text.text)

procedurelogger.expectedResult("Make sure Content View is updated to show SMB servers")
network_icon = icon_view.findIcon("Windows Network", checkShowing=False)

# Step3: Double-click 'Windows Network' icon to see workgroups in the network
#network_icon.open(log=True)
openAction(network_icon)
sleep(config.LONG_DELAY)

# Step4: Make sure nautilus frame is updated to 'Windows Network - File Browser',
# location text is updated to 'smb:///', Content View is updated to show workgroup
expect_name = "Windows Network - File Browser"
expect_text = "smb:///"

procedurelogger.expectedResult("Make sure nautilus frame is updated to " + expect_name)
assert nFrame.name == expect_name, \
                 "frame name expect: %s, actual: %s" % (expect_name, nFrame.name)

procedurelogger.expectedResult("Make sure location text is updated to " + expect_text)
l_text = nFrame.findText(None)
assert l_text.text == expect_text, \
                 "location text expect: %s, actual: %s" % (expect_text, l_text.text)

procedurelogger.expectedResult("Make sure Content View is updated to show default workgroup")
workgroup_name = os.popen('grep workgroup /etc/samba/smb.conf').read().strip('\n').split(' = ')[1]
workgroup_icon = icon_view.findIcon(workgroup_name, checkShowing=False)

# Step5: Double-click the default workgroup icon which is determined by "workgroup"
# key under [global] in /etc/samba/smb.conf
openAction(workgroup_icon)
sleep(config.LONG_DELAY)

# Step6: See a list of the servers in that workgroup
expect_text = "smb://workgroup/"
procedurelogger.expectedResult("Make sure location text is updated to " + expect_text)
l_text = nFrame.findText(None)
assert l_text.text == expect_text, \
                 "location text expect: %s, actual: %s" % (expect_text, l_text.text)

procedurelogger.expectedResult("See a list of the servers in that workgroup")
list_num = content_view.findLayeredPane("Icon View").childCount
assert list_num > 0, "list %s server in workgroup" % list_num

# Quit app
nFrame.findMenuBar(None).select(['File', 'Close'])
sleep(config.SHORT_DELAY)
app.assertClosed()

