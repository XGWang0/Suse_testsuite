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
# Date:        02/21/2011
# Description: Automatic wireless network connetction Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Automatic wireless network connection===
Step1: Left click on the NetworkManager icon and select wireless1_name check item
Step2: Enter password wireless1_pwd and click Connect if authentication dialog pops up
Step3: Make sure wireless1_name is connecting
Step4: Right click on the NetworkManager icon, uncheck "Enable Wireless" to leave 
the wireless network
Step5: Check "Enable Wireless" to make wireless available again
Step6: Left click on the NetworkManager icon, make sure wireless1_name is checked
Step7: From Connection Information to make sure wireless1_name is connecting
"""
# imports
from nm_frame import *
from nm_config import *

print doc

# Make sure have Wireless settings
if wireless1_name == "":
    raise Exception, "ERROR: Please config nm_config to give Wireless settings"
    exit(11)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Step1: Left click on the NetworkManager icon and select wireless1_name check item 
# make it to be the last wireless connection
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findCheckMenuItem(wireless1_name).mouseClick()
sleep(20)

authenWireless(wireless1_pwd)

# Step3: Make sure wireless1_name is connecting
name = 'Auto ' + wireless1_name
checkInfo([name,])

# Step4: Right click on the NetworkManager icon, uncheck "Enable Wireless" to leave
# the wireless network
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)

enable_wireless = nm_applet_app.findWindow(None).findCheckMenuItem("Enable Wireless")
if enable_wireless.checked:
    enable_wireless.mouseClick()
    sleep(config.MEDIUM_DELAY)

# Step5: Check "Enable Wireless" to make wireless available again
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findCheckMenuItem("Enable Wireless").mouseClick()
sleep(30)

try:
    authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")
except SearchError:
    pass
else:
    authen_dialog.findPushButton("Cancel").mouseClick()
    sleep(config.SHORT_DELAY)
    raise Exception, "ERROR: Doesn't auto connect to the last connected wireless"
    exit(1)

# Step6: Left click on the NetworkManager icon, make sure wireless1_name is checked
checkConnection(wireless1_name)

# Step7: From Connection Information to make sure wireless1_name is connecting
checkInfo(['Auto ' + wireless1_name,])

