#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        12/13/2010
# Description: Tomboy Search For Text In Body of Note Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Search For Text In Body of Note test===
Step1: Open "Using Links in Tomboy"
Step2: Click Text -> Find in This Note
Step3: Find text box is showing
Step4: Input "automatically" into Find text that "Previous" button is sensitive
Step5: Input "Automatically" into Find text that "Previous" button is sensitive 
Step6: Input "Novell" into Find text that "Previous" button is unsensitive
Step7: Close Find text box

NOTE:
(1) "Case Sensitive" only happens in "Search All Notes" of tomboy-0.12.1 version, it doesn't effect on "Find in This Note"
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

# Step1: Open "Using Links in Tomboy"
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 5)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

using_frame = app.findFrame("Using Links in Tomboy")

# Step2: Click Text -> Find
using_frame.findToggleButton("Text").mouseClick()
sleep(config.SHORT_DELAY)

app.findWindow(None).findMenuItem("Find in This Note").mouseClick()
sleep(config.SHORT_DELAY)

# Step3: Find text box is showing
procedurelogger.expectedResult("Find text box is showing on bottom")
find_text = using_frame.findText(None, labelledBy="Find:")

# Step4: Input "using" into Find text that "Next" button is sensitive
find_text.insertText("automatically")
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("automatically is found")
assert using_frame.findPushButton("Previous").sensitive == True, \
                                             "using is not found"

# Step5: Input "Using" into Find text that "Next" button is sensitive
find_text.deleteText() 
sleep(config.SHORT_DELAY)
find_text.insertText("Automatically")
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("Automatically is found")
assert using_frame.findPushButton("Previous").sensitive == True, \
                                              "Using is not found"

# Step6: Input "Novell" into FInd text that "Next" button is unsensitive
find_text.deleteText()
sleep(config.SHORT_DELAY) 
find_text.insertText("Novell")
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("Novell is not found")
assert using_frame.findPushButton("Previous").sensitive == False, \
                                         "Novell shouldn't be found"

# Step7: Close Find text box
using_frame.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("Find text box disappears")
try:
    using_frame.findText(None, labelledBy="Find:")
except SearchError:
    pass
else:
    assert False, "Find text box shouldn't appears"

# Close frame
using_frame.altF4()

# Quit Tomboy
quitTomboy(tomboy_panel)
