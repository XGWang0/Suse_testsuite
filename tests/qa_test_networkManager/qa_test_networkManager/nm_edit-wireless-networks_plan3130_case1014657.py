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
# Written by: Felicia Mu<fxmu@novell.com>
#             Calen Chen <cachen@novell.com>
# Date:       02/15/2011
# Description: Edit wireless networks Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Edit Wireless Networks===
Step1: Right click NetworkManager icon
Step2: Click "Edit Connections"
Step3: Choose Wireless tab page
Step4: Choose wireless1_name wireless, click Edit button
Step5: Update Connection name to "Edit Test"
Step6: Click "Wireless Security" tab, update Password to wrong one "bbbbbbbbbb"
Step7: Click "Apply" button
Step8: Make sure Authentication Required dialog appears due to wrong password
Step9: Close Authentication dialog
Step10: Revert Connection name to Auto wireless1_name, Password to wireless1_pwd from "Edit Connections"
Step11: Left click NetworkManager icon, select wireless1_name to connect
"""
# imports
import os
from nm_frame import *
from nm_config import *

print doc

# Make sure have machine settings
if wireless1_name == "" or wireless1_pwd == "":
    raise Exception, "ERROR: Please config nm_config to give Wireless settings"
    exit(11)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Left click on the NetworkManager icon and select wireless1_name check item
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findCheckMenuItem(wireless1_name).mouseClick()
sleep(20)
authenWireless(wireless1_pwd)

# Step1: Right click NetworkManager icon
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)

# Step2: Click "Edit Connections"
nm_applet_app.findWindow(None).findMenuItem(re.compile('^Edit Connections')).click(log=True)
sleep(config.SHORT_DELAY)

nm_editor_app = cache._desktop.findApplication("nm-connection-editor", checkShowing=False)
connection_dialog = nm_editor_app.findDialog("Network Connections")

# Step3: Choose Wireless tab page
connection_dialog.findPageTab("Wireless").mouseClick()
sleep(config.SHORT_DELAY)

# Step4: Choose wireless1_name wireless, click Edit button
connection_dialog.findTableCell("Auto %s" % wireless1_name).mouseClick()
sleep(config.SHORT_DELAY)

connection_dialog.findPushButton("Edit").mouseClick()
sleep(config.SHORT_DELAY)

editing_frame = nm_editor_app.findFrame("Editing Auto %s" % wireless1_name)

# Step5: Update Connection name to "Edit Test"
editing_frame.findText(None).enterText("Edit Test")

# Step6: Click "Wireless Security" tab, update Password to wrong one "bbbbbbbbbb"
security_tab = editing_frame.findPageTab("Wireless Security")
security_tab.mouseClick()
sleep(config.SHORT_DELAY)

security_tab.findPasswordText(None).enterText("bbbbbbbbbb")
sleep(config.SHORT_DELAY)

# Step7: Click "Apply" button
editing_frame.findPushButton("Apply").mouseClick()
sleep(config.SHORT_DELAY)
connection_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)

nm_editor_app.assertClosed()
sleep(30)

# Step8: Make sure Authentication Required dialog appears due to wrong password
try:
    authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")
except SearchError:
    # Or auto connect to other wireless but not wireless1_name
    checkConnection(wireless1_name, status=False)
else:
    # Step9: Close Authentication dialog
    authen_dialog.findPushButton("Cancel").mouseClick()
    sleep(config.SHORT_DELAY)
    authen_dialog.assertClosed()

# Step10: Revert Connection name to Auto wireless1_name, Password to wireless1_pwd from "Edit Connections"
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem(re.compile('^Edit Connections')).click(log=True)
sleep(config.SHORT_DELAY)

nm_editor_app = cache._desktop.findApplication("nm-connection-editor", checkShowing=False)
connection_dialog = nm_editor_app.findDialog("Network Connections")

connection_dialog.findPageTab("Wireless").mouseClick()
sleep(config.SHORT_DELAY)

connection_dialog.findTableCell("Edit Test").mouseClick()
sleep(config.SHORT_DELAY)

connection_dialog.findPushButton("Edit").mouseClick()
sleep(config.SHORT_DELAY)

editing_frame = nm_editor_app.findFrame("Editing Edit Test")

editing_frame.findText(None).enterText("Auto %s" % wireless1_name)

security_tab = editing_frame.findPageTab("Wireless Security")
security_tab.mouseClick()
sleep(config.SHORT_DELAY)

security_tab.findPasswordText(None).enterText(wireless1_pwd)
sleep(config.SHORT_DELAY)

editing_frame.findPushButton("Apply").mouseClick()
sleep(config.SHORT_DELAY)
connection_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)

nm_editor_app.assertClosed()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)
nm_applet_app.findWindow(None).findCheckMenuItem(wireless1_name).mouseClick()
sleep(20)
authenWireless(wireless1_pwd)

# Step11: Make sure wireless wireless1_name connection successful
checkConnection(wireless1_name)
checkInfo(['Auto ' + wireless1_name,])

# Remove test connection
cleanConnection(wireless1_name)

