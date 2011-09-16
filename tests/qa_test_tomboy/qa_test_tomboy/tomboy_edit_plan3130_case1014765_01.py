#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        12/07/2010
# Description: Tomboy Edit Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Edit test===
Step1: Create a new note
Step2: Add some texts to the note 
Step3: Close the note to save
Step4: Reopen this note
Step5: Make sure the changes in this note are still there
Step6: Restart Tomboy
Step7: Make sure the changes in this note are still there
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

new1_frame = app.findFrame(re.compile('^New Note'))

# Step2: Add some texts to the note 
new1_text = new1_frame.findText(None)
new1_text.enterText("Note A\r\n\r\nThis is a note for test case 1014765")

# Step3: Close the note to save
new1_frame.altF4()

# Step4: Reopen this note
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 6)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

# Step5: Make sure the changes in this note are still there
note_frame = app.findFrame("Note A")
note_text = note_frame.findText(None)

procedurelogger.expectedResult('The changes in this note are still there')
text_info = "Note A\r\n\r\nThis is a note for test case 1014765"
assert note_text.text == text_info, "text should be: %s, actual is: %s" %\
                                        (text_info, not_text.text)

# Step6: Restart Tomboy
quitTomboy(tomboy_panel)

(app, subproc) = cache.launchApplication('/usr/bin/tomboy', app_name, wait=config.MEDIUM_DELAY)

# Find tomboy on panel
tomboy_panel = tomboyPanel()

# Step7: Make sure the changes in this note are still there
note_frame = app.findFrame("Note A")
note_text = note_frame.findText(None)

procedurelogger.expectedResult('The changes in this note are still there')
assert note_text.text == text_info, "text should be: %s, actual is: %s" %\
                                        (text_info, not_text.text)

# Delete the note
note_frame.findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)
app.findDialog(None).findPushButton("Delete").mouseClick()

note_frame.assertClosed()

# Quit Tomboy
quitTomboy(tomboy_panel)
