#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        12/09/2010
# Description: Tomboy Rename Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Rename test===
Step1: Create a new note
Step2: Change the first line text to the new name of the note and save it
Step3: The name of the note is changed
Step4: Restart Tomboy
Step5: The note still be with changed name
"""
# imports
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

# Step2: Change the first line text to the new name of the note and save it
new_text = new_frame.findText(None)
new_text.deleteText()
sleep(config.SHORT_DELAY)
new_text.insertText("Note A")
sleep(config.SHORT_DELAY)

# Step3: The name of the note is changed
procedurelogger.expectedResult('The name of the note is changed to Note A')
assert new_frame.name == "Note A", "expected name:%s, actual name:%s" % \
                                                    ("Note A", new_frame)

# Step4: Restart Tomboy
quitTomboy(tomboy_panel)

(app, subproc) = cache.launchApplication('/usr/bin/tomboy', app_name, wait=config.MEDIUM_DELAY)

# Find tomboy on panel
tomboy_panel = tomboyPanel()

# Step5: The note still be with changed name
note_frame = app.findFrame("Note A")

# Delete the note
procedurelogger.action('Click Delete button')
note_frame.findPushButton("Delete").__getattr__('click')()
sleep(config.SHORT_DELAY)
app.findDialog(None).findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)

note_frame.assertClosed()

# Quit Tomboy
quitTomboy(tomboy_panel)
