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
# Date:        03/28/2011
# Description: UI Enable Networking and Wireless Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===UI Enable Networking and Wireless===
Step1: Right click on the NetworkManager icon and uncheck "Enable Wireless"
Step2: Left click on the NetworkManager icon, "wireless is disabled" appears
Step3: Right click on the NetworkManager icon and check "Enable Wireless"
Step4: Left click on the NetworkManager icon, click wireless1_name wireless
Step5: Make sure wireless1_name wireless is connected
Step6: Right click on the NetworkManager icon and uncheck "Enable Networking"
Step7: Left click on the NetworkManager icon, "networking disabled" appears
Step8: Right click on the NetworkManager icon and check "Enable Networking"
Step9: Make sure "System eth0" and last known wireless wireless1_name connected
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

# Step1: Right click on the NetworkManager icon and uncheck "Enable Wireless"
nm_panel = nmPanel()

nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)
enable_wireless = nm_applet_app.findWindow(None).findCheckMenuItem("Enable Wireless")
if enable_wireless.checked:
    enable_wireless.mouseClick()
    sleep(config.SHORT_DELAY)
else:
    nm_panel.mouseClick()
    sleep(config.LONG_DELAY)

# Step2: Left click on the NetworkManager icon, "wireless is disabled" appears
nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('"wireless is disabled" label appears')
nm_applet_app.findWindow(None).findMenuItem("wireless is disabled", checkShowing=False)

nm_panel.mouseClick(log=False)
sleep(config.SHORT_DELAY)

# Step3: Right click on the NetworkManager icon and check "Enable Wireless"
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)
nm_applet_app.findWindow(None).findCheckMenuItem("Enable Wireless").mouseClick()
sleep(10)

# Step4: Left click on the NetworkManager icon, click wireless1_name wireless
nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findCheckMenuItem(wireless1_name).mouseClick()
sleep(20)
authenWireless(wireless1_pwd)

# Step5: Make sure wireless1_name wireless is connected
checkInfo(['Auto ' + wireless1_name,])

# Step6: Right click on the NetworkManager icon and uncheck "Enable Networking"
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)
nm_applet_app.findWindow(None).findCheckMenuItem("Enable Networking").mouseClick()
sleep(config.SHORT_DELAY)

# Step7: Left click on the NetworkManager icon, "Networking disabled" appears
nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('"Networking disabled" label appears')
nm_applet_app.findWindow(None).findMenuItem("Networking disabled", checkShowing=False)

nm_panel.mouseClick(log=False)
sleep(config.SHORT_DELAY)

# Step8: Right click on the NetworkManager icon and check "Enable Networking"
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)
nm_applet_app.findWindow(None).findCheckMenuItem("Enable Networking").mouseClick()
sleep(30)
authenWireless(wireless1_pwd)

# Step9: Make sure "System eth0" and last known wireless wireless1_name connected
checkInfo(['eth0', 'Auto ' + wireless1_name,])


