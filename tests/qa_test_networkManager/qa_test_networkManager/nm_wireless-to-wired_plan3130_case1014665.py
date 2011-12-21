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
# Date:        02/14/2011
# Description: Wireless to Wired Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Wireless to Wired===
Step1: Left click on the NetworkManager icon and select wireless1_name check item
Step2: Enter password wireless1_pwd and click Connect if authentication dialog pops up
Step3: Left click on the NetworkManager icon, make sure "System eth0" and wireless1_name are checked
Step4: Right click on the NetworkManager icon, uncheck Enable Wireless 
Step5: Make sure "Wired Network" System eth0 is still connected
Step6: Right click on the NetworkManager icon, check Enable Wireless 
Step7: Make sure "Wired Network" System eth0 is still connected
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

# Step1: Left click on the NetworkManager icon and select wireless1_name check item
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findCheckMenuItem(wireless1_name).mouseClick()
sleep(20)
authenWireless(wireless1_pwd)

# Step3: Left click on the NetworkManager icon, make sure "System eth0" and wireless1_name are checked
checkConnection("System eth0")
checkConnection(wireless1_name)

# Check Connection Information
checkInfo(['System eth0 (default)', 'Auto ' + wireless1_name,])

# Step4: Right click on the NetworkManager icon, uncheck Enable Wireless 
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)

enable_wireless = nm_applet_app.findWindow(None).findCheckMenuItem("Enable Wireless")
if enable_wireless.checked:
    enable_wireless.mouseClick()
    sleep(config.MEDIUM_DELAY)

# Step5: Make sure "Wired Network" System eth0 is still connected
checkConnection("System eth0")

# Check Connection Information
checkInfo(['System eth0 (default)',])

# Step6: Right click on the NetworkManager icon, check Enable Wireless 
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)

enable_wireless = nm_applet_app.findWindow(None).findCheckMenuItem("Enable Wireless")
if not enable_wireless.checked:
    enable_wireless.mouseClick()
    sleep(30)

authenWireless(wireless1_pwd)

# Step7: Make sure "Wired Network" System eth0 is still connected
checkConnection("System eth0")
checkConnection(wireless1_name)

# Check Connection Information
checkInfo(['System eth0 (default)', 'Auto ' + wireless1_name,])

# Remove connection
cleanConnection(wireless1_name)

