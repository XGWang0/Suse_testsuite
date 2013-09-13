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

