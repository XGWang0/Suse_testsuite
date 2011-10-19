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
# Written by:  Calen Chen <cachen@novell.com>
# Date:        07/26/2011
# Description: Nautilus displays icon for all items Test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Nautilus displays icon for all items===
Step1: Launch Nautilus, navigate to user home directory ~/
Step2: Inspect the icons for all items
Step3: Set option "Show hidden files" from View->Show Hidden Files
Step4: Make sure all items should have the correct icons
"""

# imports
from strongwind import *
from gnome_frame import *
import os
import subprocess

print doc

home_path = os.getenv("HOME")

def changePath(acc, path_name):
    """
    Navigate folder from Location text
    """
    location_text = acc.findText(None, labelledBy="Location:", checkShowing=False)
    if not location_text.showing:
        edit_toggle = acc.findToggleButton("Edit").mouseClick()
        sleep(config.SHORT_DELAY)

    procedurelogger.action('Enter %s' % path_name)
    location_text.text = path_name

    location_text.mouseClick()
    location_text.keyCombo('enter')
    sleep(config.SHORT_DELAY)

# Step1: Launch Nautilus
try:
    app = launchNautilus("/usr/bin/nautilus", "nautilus")
except IOError, msg:
    print "ERROR:  %s" % msg
    exit(2)

# Just an alias to make things shorter.
nFrame = app.findFrame(re.compile('^%s' % os.getenv('USER')))
menubar = nFrame.findMenuBar(None)

# Navigate to user home directory ~/
changePath(nFrame, home_path)

# Showing in Icons
menubar.findMenu("View").mouseClick()
sleep(config.SHORT_DELAY)
menubar.findCheckMenuItem('Icons').mouseClick()
sleep(config.MEDIUM_DELAY)

# Uncheck the "Show hidden files"
hidden_check = menubar.findCheckMenuItem("Show Hidden Files", checkShowing=False)

if hidden_check.checked:
    menubar.findMenu("View").mouseClick()
    sleep(config.SHORT_DELAY)
    hidden_check.mouseClick()
    sleep(20)

# Step2: Inspect the icons for all items
icon_view = nFrame.findLayeredPane("Icon View")
icons = icon_view.findAllIcons(None)

# Step3: Set option "Show hidden files" from View->Show Hidden Files
hidden_check.click(log=True)
sleep(20)

# Step4: Make sure all items should have the correct icons
icons_hidden = icon_view.findAllIcons(None)

procedurelogger.expectedResult("Make sure hidden icons are showing ")
assert len(icons) != len(icons_hidden), \
                   "Should have more icons to show when hidden menu item is checked"

sleep(config.SHORT_DELAY)
icon_view.findIcon(re.compile('^.'))

# Uncheck "Show hidden files"
hidden_check.click(log=True)
sleep(config.SHORT_DELAY)

# Quit nautilus
menubar.findMenuItem("Close", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)
nFrame.assertClosed()

