#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
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
#


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

