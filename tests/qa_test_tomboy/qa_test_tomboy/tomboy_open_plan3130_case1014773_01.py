#!/usr/bin/env python

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
