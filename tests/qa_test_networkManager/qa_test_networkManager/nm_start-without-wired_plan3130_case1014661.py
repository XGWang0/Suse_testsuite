#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        01/12/2011
# Description: Network Manager Start Without Wired Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Start Without Wired test===
Step1: Shutdown network manager by kill
Step2: Make sure NetworkManager disappears on Panel Notification Area
Step3: Start network manager by command "NetworkManager"
Step4: Make sure NetworkManager appears on Panel Notification Area
"""
# imports
import os
from strongwind import *
from nm_frame import *

print doc

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Count panels number on Panel Notification Area before kill nm
gnome_panel = cache._desktop.findApplication("gnome-panel", checkShowing=False)
notification_area = pyatspi.findDescendant(gnome_panel, lambda x: x.name == 'Panel Notification Area')
filler = notification_area.findFiller(None)
old_panels = filler.findAllPanels(None)

# Step1: Shutdown network manager by kill
procedurelogger.action('Shutdown network manager by kill NetworkManager')
os.system('killall -9 NetworkManager')
sleep(config.MEDIUM_DELAY)

# Step2: Make sure NetworkManager disappears on Panel Notification Area
no_nm_panels = filler.findAllPanels(None)
procedurelogger.expectedResult('Make sure NetworkManager icon disappears')
assert len(no_nm_panels) == len(old_panels) - 1, \
                        "NetworkManager icon shouldn't appears on panel"

# Step3: Start network manager by command "NetworkManager"
procedurelogger.action('Start network manager by command "NetworkManager"')
os.system('NetworkManager&')
sleep(20)

# Step4: Make sure NetworkManager appears on Panel Notification Area
nm_panels = filler.findAllPanels(None)
procedurelogger.expectedResult('Make sure NetworkManager icon appears')
assert len(nm_panels) == len(old_panels), \
                        "NetworkManager icon doesn't appears on panel"

running = True
while running:
    try:
        authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")
    except SearchError:
        running = False
    else:
        authen_dialog.findPushButton("Cancel").click(log=True)
        sleep(20)
