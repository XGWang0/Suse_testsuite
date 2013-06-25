#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE, Inc. All Rights Reserved.
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
# Date:        02/28/2011
# Description: Connect to a supported VPN Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Connect to a supported VPN===
Step1: Left click on the NetworkManager icon, click "VPN Connections", select "Configure VPN..."
Step2: On "VPN" tab page, click "Add"
Step3: Select "NovellVPN Client", click "Create" button
Step4: On "Editing VPN connection 1" dialog setting VPN informations:
        Gateway: vpn.bej.novell.com
        Gateway Type: Notel
        Auth Type: XAUTH
        User name: <innerweb username>
        Group name: novell
        User password: <innerweb password>
        Group password: letmein
        DH Group: DH1
Step5: Click "Apply" to save the settings
Step6: Left click on the NetworkManager icon, click "VPN Connections", select "VPN connection 1"
Step7: Make sure "VPN connection 1" is checked
"""
# imports
import os
from nm_frame import *
from nm_config import *

print doc

# Make sure have VPN settings
if vpn_user_name == "":
    raise Exception, "ERROR: Please config nm_config to give VPN settings"
    exit(11)

# Make sure have novellvpn packages
novellvpn_rpm = os.system('rpm -q NetworkManager-novellvpn')
if novellvpn_rpm != 0:
    raise Exception, "ERROR: missing NetworkManager-novellvpn and NetworkManager-novellvpn-gnome packages"
    exit(11)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Step1: Left click on the NetworkManager icon, click "VPN Connections", select "Configure VPN..."
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenu("VPN Connections").mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem(re.compile('^Configure VPN')).click(log=True)
sleep(config.SHORT_DELAY)

nm_editor_app = cache._desktop.findApplication("nm-connection-editor", checkShowing=False)
connection_dialog = nm_editor_app.findDialog("Network Connections")

# Step2: On "VPN" tab page, click "Add"
connection_dialog.findPushButton("Add").mouseClick()
sleep(config.SHORT_DELAY)

type_dialog = nm_editor_app.findAllDialogs(None)[1]

# Step3: Select "NovellVPN Client", click "Create" button
type_dialog.findMenuItem("NovellVPN Client", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

type_dialog.findPushButton("Create...").mouseClick()
sleep(config.SHORT_DELAY)

edit_frame = nm_editor_app.findFrame("Editing VPN connection 1")

# Step4: On "Editing VPN connection 1" dialog setting VPN informations:
# Gateway: vpn.bej.novell.com
edit_frame.findText(None, labelledBy="Gateway:").enterText(vpn_gateway)
sleep(config.SHORT_DELAY)

# Gateway Type: Nortel
edit_frame.findMenuItem("Nortel", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

# Auth Type: XAUTH
edit_frame.findMenuItem("XAUTH", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

# User name: <innerweb username>
edit_frame.findText(None, labelledBy="User Name:").enterText(vpn_user_name)
sleep(config.SHORT_DELAY)

# Group name: novell
edit_frame.findText(None, labelledBy="Group Name:").enterText(vpn_group_name)
sleep(config.SHORT_DELAY)

# User password: <innerweb password>
edit_frame.findPasswordText(None, labelledBy="User Password:").enterText(vpn_user_pwd)
sleep(config.SHORT_DELAY)

# Group password: letmein
edit_frame.findPasswordText(None, labelledBy="Group Password:").enterText(vpn_group_pwd)
sleep(config.SHORT_DELAY)

# DH Group: DH1
edit_frame.findPushButton("Advanced...").mouseClick()
sleep(config.SHORT_DELAY)

adv_dialog = nm_editor_app.findDialog("NovellVPN Advanced Options")
adv_dialog.findMenuItem("768 bits (DH1)", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

adv_dialog.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

adv_dialog.assertClosed()

# Step5: Click "Apply" to save the settings
edit_frame.findPushButton("Apply").mouseClick()
sleep(config.SHORT_DELAY)
connection_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)

nm_editor_app.assertClosed()

# Step6: Left click on the NetworkManager icon, click "VPN Connections", select "VPN connection 1"
nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenu("VPN Connections").mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findCheckMenuItem("VPN connection 1").mouseClick()
sleep(20)

# Step7: Make sure "VPN connection 1" is checked
nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenu("VPN Connections").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('"VPN connection 1" is checked')
assert nm_applet_app.findWindow(None).findCheckMenuItem("VPN connection 1").checked == True, \
                        "VPN connection 1 doesn't connected"

nm_panel.mouseClick(log=False)
sleep(config.SHORT_DELAY)

# Delete VNP connection 1
cleanConnection("VPN connection 1", tab="VPN")
sleep(10)

# Left click on the NetworkManager icon, click "VPN Connections", Make sure "VPN connection 1" disappear
nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenu("VPN Connections").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('"VPN connection 1" disappear')
try:
    nm_applet_app.findWindow(None).findCheckMenuItem("VPN connection 1")
except SearchError:
    nm_panel.mouseClick()
else:
    nm_panel.mouseClick()
    assert False, "VPN connection 1 shouldn't appears, Delete testing failed"

