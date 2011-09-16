#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        12/01/2010
# Description: Tomboy Undo Feature Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Undo Feature test===
Step1: Create a new note
Step2: Update the name of the note
Step3: Click Text -> Undo 1 time
Step4: Make sure the name of the note is reverted to Untitled
Step5: Close the note and reopen the note
Step6: Click Text -> Undo 1 time
Step7: Make sure the name of the note is reverted to New Note
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

# Step1: Create a new note
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 1)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

new_frame = app.findFrame(re.compile('^New Note'))

# Step2: Update the name of the note
note_text = new_frame.findText(None)
note_name = "Test Name"
procedurelogger.action("Update the name of the note to %s" % note_name)
note_text.text = note_name

test_frame = app.findFrame(note_name)

# Step3: Click Text -> Undo 1 time
test_frame.findToggleButton("Text").mouseClick()
sleep(config.SHORT_DELAY)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

# Step4: Make sure the name of the note is reverted to Untitled
untitled_frame = app.findFrame(re.compile('^\(Untitled'))

# Step5: Close the note and reopen the note
untitled_frame.altF4()

tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 6)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

untitled_frame = app.findFrame(re.compile('^\(Untitled'))

# Step6: Click Text -> Undo 1 time
untitled_frame.findToggleButton("Text").mouseClick()
sleep(config.SHORT_DELAY)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

# Step7: Make sure the name of the note is reverted to New Note
new_frame = app.findFrame(re.compile('^New Note'))

# Delete the note
new_frame.findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)

app.findDialog(None).findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)

# Quit Tomboy
quitTomboy(tomboy_panel)
