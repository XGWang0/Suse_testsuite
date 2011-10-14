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
# Date:        12/23/2010
# Description: Tomboy What Link Here Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===What Link Here test===
Step1: Create a new note
Step2: Insert text "Note B\r\nHere is a test for case 1014775"
Step3: Create a new note
Step4: Insert text "Note A\r\nLink to Note B"
Step5: Go to Note B
Step6: Selete Tools -> What links here
Step7: "Note A" menu item should appears
Step8: Click Note A menu item under What links here
Step9: "Note A" pops up on top with active states, Find bar appears
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

note_b_frame = app.findFrame(re.compile('^New Note'))

# Step2: Insert text "Note B\r\nHere is a test for case 1014775"
note_b_text = note_b_frame.findText(None)

note_b_text.enterText("Note B\r\nHere is a test for case 1014775")
sleep(config.SHORT_DELAY)

# Step3: Create a new note
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 1)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

note_a_frame = app.findFrame(re.compile('^New Note'))

# Step4: Insert text "Note A\r\nLink to Note B"
note_a_text = note_a_frame.findText(None)

note_a_text.enterText("Note A\r\nLink to Note B")
sleep(config.SHORT_DELAY)

# Step5: Go to Note B
procedurelogger.action('Go to Note B')
note_b_text.grabFocus()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('Note B frame is on top with active states')
assert note_b_frame.active == True, "Note B frame doesn't pops up on top"

# Step6: Selete Tools -> What links here
tool_button = note_b_frame.findAllToggleButtons(None)[1]

tool_button.mouseClick()
sleep(config.SHORT_DELAY)

app.findWindow(None).findMenu("What links here?").mouseClick()
sleep(config.SHORT_DELAY)

# Step7: "Note A" menu item should appears
procedurelogger.expectedResult('"Note A" menu item should appears')
note_a_item = app.findWindow(None).findMenuItem("Note A")

# Step8: Click Note A menu item under What links here
note_a_item.mouseClick()
sleep(config.SHORT_DELAY)

# Step9: "Note A" pops up on top with active states
procedurelogger.expectedResult('Note A frame is on top with active states')
assert note_a_frame.active == True, "Note A frame doesn't pops up on top"

#  Find bar appears
procedurelogger.expectedResult('Find bar appears')
note_a_frame.findText(None, labelledBy="Find:")

# Delete Note A
deleteNote(app, note_a_frame)
deleteNote(app, note_b_frame)

# Quit Tomboy
quitTomboy(tomboy_panel)

