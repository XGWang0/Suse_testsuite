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
# Date:        03/21/2011
# Description: Connect to Novell and roam corporate secure "Novell" Wifi Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Connect to Novell Wifi===
Step1: Make sure have Novell secure wifi settings
Step2: Left click on the NetworkManager icon and select "Novell" check item
Step3: Enter User Name and Password in "Wireless Netowrk Authentication Required",
click Connect
Step4: Make sure "Novell" is connected

"""
# imports
import os
from strongwind import *
from nm_frame import *
from nm_config import *

print doc

# Step1: Make sure have Novell secure wifi settings
if wifi_user_name == "":
    raise Exception, "ERROR: Please config nm_config to give Novell secure Wifi settings"
    exit(11)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Step2: Left click on the NetworkManager icon and select "Novell" check item
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

try:
    novell_wifi = nm_applet_app.findWindow(None).findCheckMenuItem("Novell")
except SearchError:
    nm_panel.mouseClick()
    sleep(config.SHORT_DELAY)
    raise Exception, "ERROR: Novell wifi doesn't exist in the working area"
    exit(22)
else:
    novell_wifi.mouseClick()
    sleep(20)

running = True
count = 0
while running:
    try:
        authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")
    except SearchError:
        running = False
    else:
        count += 1
        if count == 3:
            authen_dialog.findPushButton("Cancel").mouseClick()
            sleep(config.SHORT_DELAY)
            raise Exception, "ERROR: Fails to connect Novell Wifi, Please make sure it works"
            exit(22)
        else:
            # Step3: Enter User Name and Password in "Wireless Netowrk Authentication Required",
            authen_dialog.findAllTexts(None)[0].enterText(wifi_user_name)
            sleep(config.SHORT_DELAY)

            authen_dialog.findPasswordText(None).enterText(wifi_user_pwd)
            sleep(config.SHORT_DELAY)

            # click Connect
            authen_dialog.findPushButton("Connect").mouseClick()
            sleep(config.SHORT_DELAY)

            try:
                nm_applet_app.findAllDialogs(None)[1].findPushButton("Ignore").mouseClick()
            except SearchError:
                pass

            authen_dialog.assertClosed()
            sleep(30)

# Step4: Make sure "Novell" is connected
checkConnection("Novell")

checkInfo(['Novell',])

