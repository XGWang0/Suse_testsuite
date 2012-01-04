#!/usr/bin/env python
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
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


##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        11/30/2010
# Description: Tomboy Menu Functionality In "Search All Notes" Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Menu Functionality In "Search All Notes" test===
Step1: Launch "Search All Notes"
Step2: From File -> New to create a new note
Step3: From Edit -> Preferences to open Preferences dialog
Step4: From Help -> Contents to open Contents dialog
Step5: From Help -> About to open About dialog
Step6: From File -> Close to close Search All Notes frame
"""
# imports
import os
from strongwind import *
from tomboy_frame import *

print doc

# Check version
app_name = checkVersion()

# Kill the exist Tomboy process
killRunning()

# Load Tomboy for the first time
(app, subproc) = cache.launchApplication('/usr/bin/tomboy', app_name, wait=config.MEDIUM_DELAY)

# Find tomboy on panel
tomboy_panel = tomboyPanel()

# Step1: Launch "Search All Notes"
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 3)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

search_frame = app.findFrame("Search All Notes")

# Step2: From File -> New to create a new note
search_frame.findMenu("File").mouseClick()
sleep(config.SHORT_DELAY)
search_frame.findMenuItem("New").mouseClick()
sleep(config.SHORT_DELAY)

new_frame = app.findFrame(re.compile('^New Note'))
new_frame.findPushButton("Delete").click(log=True)
sleep(config.SHORT_DELAY)
app.findDialog(None).findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)

new_frame.assertClosed()

# Step3: From Edit -> Preferences to open Preferences dialog
search_frame.findMenu("Edit").mouseClick()
sleep(config.SHORT_DELAY)
search_frame.findMenuItem("Preferences").mouseClick()
sleep(config.SHORT_DELAY)

pre_dialog = app.findDialog("Tomboy Preferences")
pre_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)

pre_dialog.assertClosed()

# Step4: From Help -> Contents to open gnome-help application
search_frame.findMenu("Help").mouseClick()
sleep(config.SHORT_DELAY)
search_frame.findMenuItem("Contents").mouseClick()
sleep(config.MEDIUM_DELAY)

if app_name is "Tomboy":
    help_app = "yelp"
    if tomboy_version[0] is '0':
        help_frame = "Tomboy Notes Manual"
    else:
        help_frame = "Tomboy Notes"
else:
    help_app = "gnome-help"
    help_frame = "Tomboy Notes Manual"

help = cache._desktop.findApplication(help_app, checkShowing=False)
loading_frame = help.findFrame(re.compile('^%s' % help_frame))
loading_frame.findMenuItem("Close Window", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)
loading_frame.assertClosed()

# Step5: From Help -> About to open About dialog
search_frame.findMenu("Help").mouseClick()
sleep(config.SHORT_DELAY)
search_frame.findMenuItem("About").mouseClick()
sleep(config.SHORT_DELAY)

about_dialog = app.findDialog("About Tomboy")
about_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)

about_dialog.assertClosed()

# Step6: From File -> Close to close Search All Notes frame
search_frame.findMenu("File").mouseClick()
sleep(config.SHORT_DELAY)
search_frame.findMenuItem("Close").mouseClick()
sleep(config.SHORT_DELAY)

search_frame.assertClosed()

# Quit Tomboy
quitTomboy(tomboy_panel)

