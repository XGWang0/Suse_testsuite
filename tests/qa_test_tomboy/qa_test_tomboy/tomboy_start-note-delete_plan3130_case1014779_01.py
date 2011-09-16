#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        11/26/2010
# Description: Tomboy Start Note Cannot Be Deleted Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Start Note Cannot Be Deleted test===
Step1: Open "Start Here" note
Step2: Make sure Delete button is not sensitive
Step3: Try to delete the note
Step4: The note still opened
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

# Step1: Open "Start Here" note
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 4)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

start_frame = app.findFrame("Start Here")

# Step2: Make sure Delete button is not sensitive
procedurelogger.action("Check sensitive status of Delete button")
delete_button = start_frame.findPushButton("Delete")

procedurelogger.expectedResult("Delete button is not sensitive")
assert delete_button.sensitive == False, "Delete button shouldn't sensitive"

# Step3: Try to delete the note
delete_button.mouseClick()
sleep(config.SHORT_DELAY)

# Step4: The note still opened
procedurelogger.action("Check showing status of Start Here note")
procedurelogger.expectedResult("Start Here note still opened")
assert start_frame.showing == True, "Start Here note shouldn't closed"

# Close note
start_frame.altF4()

# Quit Tomboy
quitTomboy(tomboy_panel)
