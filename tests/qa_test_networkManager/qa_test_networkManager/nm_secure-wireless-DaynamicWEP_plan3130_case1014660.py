#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        04/01/2011
# Description: Daynamic WEP (802.1X) Security Method Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Daynamic WEP (802.1X) Security Method===
Step1: Left click on the NetworkManager icon, click the wireless item that is Dynamic_net_name setting
Step2: On "Wireless Network Authentication Required" dialog, make sure "Dynamic WEP (802.1x)" is selected
Step3: Enter "Private Key Password" that is Dynamic_key_pwd setting, click "Connect"
Step4: Make sure the wireless is connected
"""
# imports
import os
from nm_frame import *
from nm_config import *

print doc

# Make sure have Wireless security methods settings
if Dynamic_net_name == "":
    raise Exception, "ERROR: Please config nm_config to give Wireless security methods settings"
    exit(11)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Step1: Left click on the NetworkManager icon, click the wireless item that is Dynamic_net_name setting
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

try:
    Dynamic_wireless = nm_applet_app.findWindow(None).findCheckMenuItem(Dynamic_net_name)
except SearchError:
    nm_panel.mouseClick(log=False)
    sleep(config.SHORT_DELAY)
    raise Exception, "ERROR: Dynamic wireless doesn't exist, please set up a wireless with this security method and give settings in nm_config.py"
    exit(22)
else:
    Dynamic_wireless.mouseClick()
    sleep(20)

# Step2: On "Wireless Network Authentication Required" dialog
try:
    authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")
except SearchError:
    pass
else:
    # Make sure "Dynamic WEP (802.1x)" is selected
    if not authen_dialog.findComboBox("Dynamic WEP (802.1x)"):
        authen_dialog.findPushButton("Cancel").mouseClick()
        sleep(config.SHORT_DELAY)
        raise Exception, "ERROR: Wireless Security doesn't match Dynamic WEP (802.1x)"
        exit(1)

    # Step3: Enter "Private Key Password" that is Dynamic_key_pwd setting, click "Connect"
    authen_dialog.findPasswordText.enterText(Dynamic_key_pwd)
    sleep(config.SHORT_DELAY)

    # Click "Connect"
    authen_dialog.findPushButton("Connect").mouseClick()
    sleep(30)

# Step4: Make sure the wireless is connected
checkConnection(Dynamic_net_name)

checkInfo([Dynamic_net_name,])
