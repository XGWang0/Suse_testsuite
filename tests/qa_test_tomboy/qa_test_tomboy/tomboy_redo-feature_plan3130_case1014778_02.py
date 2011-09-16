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
Step2: Update the name of the note to Test Name
Step3: Click Text -> Undo 2 time
Step4: Make sure the name of the note is reverted to New Note
Step5: Click Text -> Redo 1 time
Step6: Make sure the name of the note is reverted to Untitiled
Step7: Close the note and reopen the note
Step8: Click Text -> Redo 1 time
Step7: Make sure the name of the note is reverted to Test Name
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

# Step2: Update the name of the note to Test Name
note_text = new_frame.findText(None)
note_name = "Test Name"
procedurelogger.action("Update the name of the note to %s" % note_name)
note_text.text = note_name

test_frame = app.findFrame(note_name)

# Step3: Click Text -> Undo 2 time
test_frame.findToggleButton("Text").mouseClick()
sleep(config.SHORT_DELAY)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

test_frame.findToggleButton("Text").mouseClick()
sleep(config.SHORT_DELAY)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

# Step4: Make sure the name of the note is reverted to New Note
new_frame = app.findFrame(re.compile('^New Note'))

# Step5: Click Text -> Redo 1 time
new_frame.findToggleButton("Text").mouseClick()
sleep(config.SHORT_DELAY)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

# Step6: Make sure the name of the note is reverted to Untitiled
untitled_frame = app.findFrame(re.compile('^\(Untitled'))

# Step7: Close the note and reopen the note
untitled_frame.altF4()

tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 6)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

# Step8: Click Text -> Redo 1 time
untitled_frame.findToggleButton("Text").mouseClick()
sleep(config.SHORT_DELAY)
keyPress(new_frame, "Down", 1)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

# Step7: Make sure the name of the note is reverted to Test Name
test_frame = app.findFrame(note_name)

# Delete the note
test_frame.findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)

app.findDialog(None).findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)

# Quit Tomboy
quitTomboy(tomboy_panel)
