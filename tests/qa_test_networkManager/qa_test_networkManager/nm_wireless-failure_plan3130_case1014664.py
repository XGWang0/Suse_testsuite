#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        02/22/2011
# Description: Wireless failure-revert to wired
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Wireless failure-revert to wired===
Step1: Make sure "Wired Network" System eth0 is connected
Step2: Clean up wireless wireless1_name from Network Connections editor
Step3: Left click on the NetworkManager icon, select wireless1_name to connect
Step4: Enter wrong password wireless1_pwd and click Connect when authentication dialog pops up
Step5: Make sure wireless connection is failed
Step6: Make sure wired System eth0 connection is successful
"""
# imports
import sys
from nm_frame import *
from nm_config import *

print doc

# Make sure have Wireless settings
if wireless1_name=="":
    raise Exception, "ERROR: Please config nm_config to give Wireless settings"
    exit(11)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Step1: Make sure "Wired Network" System eth0 is connected
try:
    checkInfo(['System eth0 (default)',])
except:
    print "Please connect your wired network with cabled"
    exit(11)

# Step2: Clean up last connection of wireless wireless1_name from Network 
# Connections editor
cleanConnection(wireless1_name)

# Step3: Left click on the NetworkManager icon, select wireless1_name to connect
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findCheckMenuItem(wireless1_name).mouseClick()
sleep(20)

try:
    authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")
except SearchError:
    raise SearchError, "Delete wireless action doesn't remove password, please remove it from seahorse"
    exit(1)
else:
    # Step4: Enter wrong password "bbbbbbbbbb" and click Connect when authentication dialog pops up
    authen_dialog.findPasswordText(None).enterText("bbbbbbbbbb")
    sleep(config.SHORT_DELAY)

    authen_dialog.findPushButton("Connect").mouseClick()
    sleep(30)

# Step5: Make sure wireless connection is failed that authentication dialog pops up again
procedurelogger.expectedResult("Wireless connection is failed")
authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")
authen_dialog.findPushButton("Cancel").mouseClick()
sleep(config.SHORT_DELAY)
authen_dialog.assertClosed()

checkConnection(wireless1_name, status=False)

# Step6: Make sure wired System eth0 connection is successful
checkConnection("System eth0")
checkInfo(['System eth0 (default)',])

# Clean wireless
cleanConnection(wireless1_name)
