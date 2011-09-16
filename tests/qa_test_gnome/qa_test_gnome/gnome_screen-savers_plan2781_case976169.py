#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        08/08/2011
# Description: GUI for Bluetooth configuration test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===GUI For Bluetooth Configuration===
Step1: Launch "gnome-screensaver-preferences" 
Step2: Check each screen saver
Step3: Check blacklist of some screensavers
"""

# imports
from strongwind import *
from gnome_frame import *
import os

print doc  

screen_cells_list = []
screen_black_list = ["apple2", "cube21", "flyingtoasters", "glmatrix", "lavalite", "loop", "m6502", "noseguy", "pacman", "penetrate", "pipes", "pong", "providence", "rubik", "sproingies", "stairs", "starwars"]

# Step1: Launch "gnome-screensaver-preferences" 
try:
    app = launchApp("gnome-screensaver-preferences", "gnome-screensaver-preferences", window="Dialog")
except IOError, msg:
    print "ERROR:  %s" % msg
    exit(2)

# just an alias to make things shorter
spDialog = app.gnomeScreensaverPreferencesDialog

# Step2: Check each screen saver by grabFocus
screen_cells = spDialog.findTreeTable(None).findAllTableCells(None, checkShowing=False)

for i in screen_cells:
    screen_cells_list.append(i.name)

for i in screen_cells:
    procedurelogger.action("grab focus on %s" % i)
    i.grabFocus()
    sleep(config.SHORT_DELAY)

# Step3: Check blacklist of some screensavers
procedurelogger.action("Check blacklist %s doesn't appears in screensavers list" % screen_black_list)
for i in screen_black_list:
    if i in screen_cells_list:
        spDialog.findPushButton("Close").mouseClick()
        sleep(config.SHORT_DELAY)
        raise Exception, "ERROR: %s in blacklist appears in Screensaver theme list" % i

# Close application
spDialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
app.assertClosed()
