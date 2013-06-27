#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
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
# Date:        02/22/2011
# Description: Wireless failure-revert to wired
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Wireless failure-revert to wired===
Step1: Make sure "Wired Network" System eth0 is connected
Step2: Clean up wireless wireless1_name from Network Connections editor
Step3: Left click on the NetworkManager icon, select wireless1_name to connect
Step4: Enter wrong password wireless1_pwd and click Connect when authentication dialog pops up
Step5: Make sure wireless connection is failed
Step6: Make sure wired System eth0 connection is successful
"""
# imports
import sys
from nm_frame import *
from nm_config import *

print doc

# Make sure have Wireless settings
if wireless1_name=="":
    raise Exception, "ERROR: Please config nm_config to give Wireless settings"
    exit(11)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Step1: Make sure "Wired Network" System eth0 is connected
try:
    checkInfo(['eth0',])
except:
    print "Please connect your wired network with cabled"
    exit(11)

# Step2: Clean up last connection of wireless wireless1_name from Network 
# Connections editor
cleanConnection(wireless1_name)

# Step3: Left click on the NetworkManager icon, select wireless1_name to connect
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findCheckMenuItem(wireless1_name).mouseClick()
sleep(20)

try:
    authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")
except SearchError:
    raise SearchError, "Delete wireless action doesn't remove password, please remove it from seahorse"
    exit(1)
else:
    # Step4: Enter wrong password "bbbbbbbbbb" and click Connect when authentication dialog pops up
    authen_dialog.findPasswordText(None).enterText("bbbbbbbbbb")
    sleep(config.SHORT_DELAY)

    authen_dialog.findPushButton("Connect").mouseClick()
    sleep(60)

# Step5: Make sure wireless connection is failed that authentication dialog pops up again
procedurelogger.expectedResult("Wireless connection is failed")
authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")
authen_dialog.findPushButton("Cancel").mouseClick()
sleep(config.SHORT_DELAY)
authen_dialog.assertClosed()

checkConnection(wireless1_name, status=False)

# Step6: Make sure wired System eth0 connection is successful
checkConnection("eth0")
checkInfo(['eth0',])

# Clean wireless
cleanConnection(wireless1_name)

