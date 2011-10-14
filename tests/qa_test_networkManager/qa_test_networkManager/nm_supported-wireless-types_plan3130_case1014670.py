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
# Description: Supported Wireless network types Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Supported Wireless Types===
802.11b only:
Step1: Connect to SLEDQATEAM-DLINK
Step2: Invoke Firefox and Set D-LINK SYSTEM to "802.11b only" type
Step3: Re-connect "SLEDQATEAM-DLINK"
Step4: make sure "SLEDQATEAM-DLINK" is connected

802.11g only:
Step1: Invoke Firefox and Set D-LINK SYSTEM to "802.11g only" type
Step2: Re-connect "SLEDQATEAM-DLINK"
Step3: make sure "SLEDQATEAM-DLINK" is connected

Mixed 802.11g and 802.11b:
Step1: Invoke Firefox and Set D-LINK SYSTEM to "Mixed 802.11g and 802.11b" type
Step2: Re-connect "SLEDQATEAM-DLINK"
Step3: make sure "SLEDQATEAM-DLINK" is connected
"""
# imports
import os
from nm_frame import *
from nm_config import *

print doc

def connectWireless(wireless_name, wireless_pwd):
    """
    Connect wireless to check the connection when wireless type is updated
    """
    # Right click on the NetworkManager icon, re-enable wireless by click 
    # "Enable Wireless" 2 times
    nm_panel = nmPanel()

    nm_panel.mouseClick(button=3)
    sleep(config.SHORT_DELAY)
    enable_wireless = nm_applet_app.findWindow(None).findCheckMenuItem("Enable Wireless")
    enable_wireless.mouseClick()
    sleep(config.SHORT_DELAY)

    nm_panel.mouseClick(button=3)
    sleep(config.SHORT_DELAY)
    enable_wireless = nm_applet_app.findWindow(None).findCheckMenuItem("Enable Wireless")
    enable_wireless.mouseClick()
    sleep(20)

    # Left click on the NetworkManager icon and select wireless_name check item
    nm_panel.mouseClick()
    sleep(config.SHORT_DELAY)

    nm_applet_app.findWindow(None).findCheckMenuItem(wireless_name).mouseClick()
    sleep(30)

    running = True
    count = 0
    while running:
        try:
            authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")
        except SearchError:
            running = False
        else:
            # Enter password and click Connect if authentication dialog pops up
            count += 1
            if count == 3:
                authen_dialog.findPushButton("Cancel").mouseClick(log=False)
                sleep(config.SHORT_DELAY)
                raise Exception, "ERROR: Fails to connect %s" % wireless_name
                exit(11)

            else:
                authen_dialog.findPasswordText(None).enterText(wireless_pwd)
                sleep(config.SHORT_DELAY)

                authen_dialog.findPushButton("Connect").mouseClick()
                sleep(30)

    # Make sure wireless is connected
    checkInfo(['Auto ' + wireless_name,])

# Make sure have Wireless settings
if wireless1_name == "":
    raise Exception, "ERROR: Please config nm_config to give Wireless settings"
    exit(11)

# Make sure have D-LINK settings
if dlink_url == "":
    raise Exception, "ERROR: Please config nm_config to give D-LINK settings"
    exit(11)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Clean up the exist connection
cleanConnection(wireless1_name)

# Step1: Connect to wireless1_name
connectWireless(wireless1_name, wireless1_pwd)

# 802.11b only:
# Step2: Invoke Firefox and Set D-LINK SYSTEM to "802.11b only" type
setDLink(dlink_url=dlink_url, admin_pwd=admin_pwd, item_name="802.11b only",
                                            item_role="MenuItem", set_info=None)

# Re-connect wireless1_name
connectWireless(wireless1_name, wireless1_pwd)

# 802.11g only:
# Step1: Invoke Firefox and Set D-LINK SYSTEM to "802.11g only" type
setDLink(dlink_url=dlink_url, admin_pwd=admin_pwd, item_name="802.11g only",
                                            item_role="MenuItem", set_info=None)

# Re-connect wireless1_name
connectWireless(wireless1_name, wireless1_pwd)

# Mixed 802.11g and 802.11b:
# Step1: Invoke Firefox and Set D-LINK SYSTEM to "802.11g only" type
setDLink(dlink_url=dlink_url, admin_pwd=admin_pwd, item_name="Mixed 802.11g and 802.11b",
                                            item_role="MenuItem", set_info=None)

# Re-connect wireless1_name
connectWireless(wireless1_name, wireless1_pwd)

