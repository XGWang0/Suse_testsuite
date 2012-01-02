#!/usr/bin/env python
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
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
# Date:        12/06/2010
# Description: Tomboy Search For Text In Title of Note Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Search For Text In Title of Note test===
Step1: Open "Using Links in Tomboy"
Step2: Click Text -> Find in This Note
Step3: Find text box is showing
Step4: Input "using" into Find text that "Previous" button is sensitive
Step5: Input "Using" into Find text that "Previous" button is sensitive 
Step6: Input "Novell" into FInd text that "Previous" button is unsensitive
Step7: Close Find text box

NOTE:
(1) "Case Sensitive" only happens in "Search All Notes" of tomboy-0.12.1 version, it doesn't effect on "Find in This Note"
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
find_text.insertText("using")
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("using is found")
assert using_frame.findPushButton("Previous").sensitive == True, \
                                             "using is not found"

# Step5: Input "Using" into Find text that "Next" button is sensitive
find_text.deleteText() 
sleep(config.SHORT_DELAY)
find_text.insertText("Using")
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("Using is found")
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

