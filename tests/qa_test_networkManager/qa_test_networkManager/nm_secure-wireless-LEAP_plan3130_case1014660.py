#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        04/01/2011
# Description: LEAP Security Method Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===LEAP Security Method===
Step1: Left click on the NetworkManager icon, click the wireless item that is LEAP setting
Step2: On "Wireless Network Authentication Required" dialog, make sure "LEAP" is selected
Step3: enter "User Name" and "Password" those are LEAP_user_name and LEAP_user_pwd settings, click "Connect"
Step4: Make sure the wireless is connected
"""
# imports
import os
from nm_frame import *
from nm_config import *

print doc

# Make sure have Wireless security methods settings
if LEAP_net_name == "":
    raise Exception, "ERROR: Please config nm_config to give Wireless security methods settings"
    exit(11)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Step1: Left click on the NetworkManager icon, click the wireless item that is LEAP_net_name setting
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

try:
    LEAP_wireless = nm_applet_app.findWindow(None).findCheckMenuItem(LEAP_net_name)
except SearchError:
    nm_panel.mouseClick(log=False)
    sleep(config.SHORT_DELAY)
    raise Exception, "ERROR: LEAP wireless doesn't exist, please set up a wireless with this security method and give settings in nm_config.py"
    exit(22)
else:
    LEAP_wireless.mouseClick()
    sleep(20)

# Step2: On "Wireless Network Authentication Required" dialog
try:
    authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")
except SearchError:
    pass
else:
    # Make sure "LEAP" is selected
    if not authen_dialog.findComboBox("LEAP"):
        authen_dialog.findPushButton("Cancel").mouseClick()
        sleep(config.SHORT_DELAY)
        raise Exception, "ERROR: Wireless Security doesn't match LEAP"
        exit(1)

    # Step3: Enter "User Name" and "Password" those are LEAP_user_name and LEAP_user_pwd settings
    authen_dialog.findAllTexts(None)[1].enterText(LEAP_user_name)
    sleep(config.SHORT_DELAY)
    authen_dialog.findPasswordText.enterText(LEAP_user_pwd)
    sleep(config.SHORT_DELAY)

    # Click "Connect"
    authen_dialog.findPushButton("Connect").mouseClick()
    sleep(30)

# Step4: Make sure the wireless is connected
checkConnection(LEAP_net_name)

checkInfo([LEAP_net_name,])
