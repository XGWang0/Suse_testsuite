#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        12/03/2010
# Description: Tomboy Delete Note Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Delete Note test===
Step1: Create a new note and open the note
Step2: Update note's name to "Text Note"
Step3: Click 'Delete' button on the toolbar
Step4: Delete the note
Step5: Make sure the note doesn't appears in the list
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

# Step1: Create a new note and open the note
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 1)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

new_frame = app.findFrame(re.compile('^New Note'))

# Step2: Update note's name to "Text Note"
procedurelogger.action("Update note's name to \"Text Note\"")
new_frame.findText(None).text = "Text Note"

# Step3: Click 'Delete' button on the toolbar
new_frame.findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)

# Step4: Delete the note
app.findDialog(None).findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)
new_frame.assertClosed()

# Step5: Make sure the note doesn't appears in the list
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("Text Note doesn't appears in the list")
tomboy_context = app.findWindow(None)
try:
    tomboy_context.findMenuItem("Test Note")
except SearchError:
    pass
else:
    assert False, "Text Note shouldn't appears, Delete testing failed"

tomboy_panel.mouseClick(log=False)
sleep(config.SHORT_DELAY)

# Quit Tomboy
quitTomboy(tomboy_panel)
