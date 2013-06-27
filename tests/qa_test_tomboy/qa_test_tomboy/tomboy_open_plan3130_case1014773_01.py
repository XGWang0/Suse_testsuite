#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
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
# Date:        11/25/2010
# Description: Tomboy Open Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Open test===
Step1: Use <Alt>F11 to Open "Start Here" note 
Step2: Rename "Start Here" to "Test Start Here"
Step3: Close the note
Step4: Use <Alt>F11 again to Open "Test Start Here" note 
Step5: Restore the name to "Start Here"
Step6: Close the note
"""
# imports
import os
from strongwind import *
from tomboy_frame import *

print doc

# Check version
app_name = checkVersion()

# Kill the exist Tomboy process
killRunning()

# Load Tomboy for the first time
(app, subproc) = cache.launchApplication('/usr/bin/tomboy', app_name, wait=config.MEDIUM_DELAY)

# Find tomboy on panel
tomboy_panel = tomboyPanel()

# Step1: Use <Alt>F11 to Open "Start Here" note
tomboy_panel.keyCombo('<Alt>F11')
sleep(config.SHORT_DELAY)

tomboy_frame = app.findFrame("Start Here")
tomboy_text = tomboy_frame.findText(None)

# Step2: Rename "Start Here" to "Test Start Here"

tomboy_text.insertText("Test ", 0)
sleep(config.SHORT_DELAY)

bbox = tomboy_text._accessible.queryComponent().getExtents(pyatspi.DESKTOP_COORDS)
pyatspi.Registry.generateMouseEvent(bbox.x, bbox.y, 'b1dc')
sleep(config.SHORT_DELAY)

# Step3: Close the note
tomboy_frame.altF4()

# Step4: Use <Alt>F11 again to Open "Test Start Here" note
tomboy_panel.keyCombo('<Alt>F11')
sleep(config.SHORT_DELAY)

tomboy_frame = app.findFrame("Test Start Here")
tomboy_text = tomboy_frame.findText(None)

# Step5: Restore the name to "Start Here"
tomboy_text.deleteText(start=0, end=5)
sleep(config.SHORT_DELAY)

# Step6: Close the note
tomboy_frame.altF4()

# Quit Tomboy
quitTomboy(tomboy_panel)

