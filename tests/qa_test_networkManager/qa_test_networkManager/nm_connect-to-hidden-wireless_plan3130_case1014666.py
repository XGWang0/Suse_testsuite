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
# Date:        03/04/2011
# Description: Connect to wireless network that does not broadcast SSID Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Connect To Hidden Wireless Network===
Step1: Make sure the hidden_wireless is set and doesn't appears on the wireless list 
Step2: Left click on the NetworkManager icon and select Connect to Hidden Wireless Network
Step3: Select "WPA & WPA2 Personal" Wireless Security
Step4: Insert Network Name and Passwork
Step5: Click "Connect" button
Step6: Make sure to link hidden_wireless_dns successful
Step7: Make sure hidden_wireless is on Connection Information page tab
"""
# imports
import os

from nm_frame import *
from nm_config import *

print doc

# Get nm-applet application layer
nm_applet_app = nmAppletApp()
nm_panel = nmPanel()

# Step1: Make sure have Hidden Wireless settings
if hidden_wireless_name == "":
    raise Exception, "ERROR: Please config nm_config to give all Hidden Wireless settings"
    exit(11)

# Make sure the Hidden Wireless doesn't appears on the wireless list
nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

try:
    nm_applet_app.findWindow(None).findCheckMenuItem(hidden_wireless_name)
except SearchError:
    pass # expected!
else:
    print "ERROR: Please setting %s to Invisible Status on D-Link side" % \
                                                      hidden_wireless_name
    nm_panel.mouseClick()
    sleep(config.SHORT_DELAY)
    exit(11)

# Step2: Left click on the NetworkManager icon and select Connect to Hidden Wireless Network
nm_applet_app.findWindow(None).findMenuItem(re.compile('^Connect to Hidden')).click(log=True)
sleep(config.SHORT_DELAY)

connect_dialog = nm_applet_app.findDialog("Connect to Hidden Wireless Network")

# Step3: Select "WPA & WPA2 Personal" Wireless Security
connect_dialog.findMenuItem("WPA & WPA2 Personal", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

# Step4: Insert Network Name and Passwork
connect_dialog.findText(None, labelledBy="Network Name:").enterText(hidden_wireless_name)
sleep(config.SHORT_DELAY)

connect_dialog.findPasswordText(None).enterText(hidden_wireless_pwd)
sleep(config.SHORT_DELAY)

# Step5: Click "Connect" button
connect_dialog.findPushButton("Connect").mouseClick()
sleep(30)

# Step6: Make sure to link hidden_wireless_dns successful
loadURL("http://%s" % hidden_wireless_dns)
sleep(config.SHORT_DELAY)

# Step7: Make sure hidden_wireless is on Connection Information page tab
checkInfo(acc_name=[hidden_wireless_name])


