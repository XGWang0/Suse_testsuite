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
# Date:        01/19/2011
# Description: 802.1x Wireless Authentication Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===802.1x Wireless Authentication test===
Step1: Left click on the NetworkManager icon and select wireless1_name check item
Step2: Enter password wireless1_pwd, click Connect
Step3: Check Connection Information
Step4: Left click on the NetworkManager icon, make sure wireless1_name is checked
"""
# imports
import os
from nm_frame import *
from nm_config import *

print doc

# Make sure have Wireless settings
if wireless1_name=="":
    raise Exception, "ERROR: Please config nm_config to give Wireless settings"
    exit(11)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Clean up the exist wireless for authentication dialog pops up
cleanConnection(wireless1_name)
sleep(config.MEDIUM_DELAY)

# Step1: Left click on the NetworkManager icon and select wireless1_name check item
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findCheckMenuItem(wireless1_name).mouseClick()
sleep(20)

running = True
count = 0
while running:
    try:
        authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")
    except SearchError:
        if count == 0:
            raise SearchError, "Delete wireless action doesn't remove password, please remove it from seahorse"
            exit(1)
        else:
            running = False
    else:
        count += 1
        if count == 3:
            authen_dialog.findPushButton("Cancel").mouseClick(log=False)
            sleep(config.SHORT_DELAY)
            raise Exception, "ERROR: Fails to connect Novell Wifi, Please make sure it works"
            exit(22)
        else:
            # Step2: Enter password wireless1_pwd, click Connect
            authen_dialog.findPasswordText(None).enterText(wireless1_pwd)
            sleep(config.SHORT_DELAY)

            authen_dialog.findPushButton("Connect").mouseClick()
            sleep(30)

# Step3: Check Connection Information
checkInfo(['Auto ' + wireless1_name,])

# Step4: Left click on the NetworkManager icon, make sure wireless1_name is checked
checkConnection(wireless1_name)

