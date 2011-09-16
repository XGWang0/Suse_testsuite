#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        03/31/2011
# Description: WEP 128-bit Passphrase Security Method Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===WEP 128-bit Passphrase Security Method===
Step1: Left click on the NetworkManager icon, click the wireless item that is WEP128bit_net_name setting
Step2: On "Wireless Network Authentication Required" dialog, make sure "WEP 128-bit Passphrase" is selected
Step3: enter Key that is WEP128bit_key setting, click "Connect"
Step4: Make sure the wireless is connected
"""
# imports
import os
from nm_frame import *
from nm_config import *

print doc

# Make sure have Wireless security methods settings
if WEP128bit_net_name == "":
    raise Exception, "ERROR: Please config nm_config to give Wireless security methods settings"
    exit(11)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Step1: Left click on the NetworkManager icon, click the wireless item that is WEP128bit_net_name setting
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

try:
    WEP128bit_wireless = nm_applet_app.findWindow(None).findCheckMenuItem(WEP128bit_net_name)
except SearchError:
    nm_panel.mouseClick(log=False)
    sleep(config.SHORT_DELAY)
    raise Exception, "ERROR: WEP 128-bit Passphrase wireless doesn't exist, please set up a wireless with this security method and give settings in nm_config.py"
    exit(22)
else:
    WEP128bit_wireless.mouseClick()
    sleep(20)

# Step2: On "Wireless Network Authentication Required" dialog
try:
    authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")
except SearchError:
    pass
else:
    # Make sure "WEP 128-bit Passphrase" is selected
    if not authen_dialog.findComboBox("WEP 128-bit Passphrase"):
        authen_dialog.findPushButton("Cancel").mouseClick()
        sleep(config.SHORT_DELAY)
        raise Exception, "ERROR: Wireless Security doesn't match WEP 128-bit Passphrase"
        exit(1)

    # Step3: enter Key that is WEP128bit_key setting
    authen_dialog.findPasswordText.enterText(WEP128bit_key)
    sleep(config.SHORT_DELAY)

    # Click "Connect"
    authen_dialog.findPushButton("Connect").mouseClick()
    sleep(30)

# Step4: Make sure the wireless is connected
checkConnection(WEP128bit_net_name)

checkInfo([WEP128bit_net_name,])
