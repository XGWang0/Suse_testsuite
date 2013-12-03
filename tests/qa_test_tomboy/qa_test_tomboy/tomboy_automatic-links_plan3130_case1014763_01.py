#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE, Inc. All Rights Reserved.
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
# Date:        11/25/2010
# Description: Tomboy Automatic Links In Notes Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Automatic Links In Notes test===
Step1: Create a new note named "Note A", close the note
Step2: Create the second note named "Note B"
Step3: Insert some test "Note A should be a link" into Note B
Step4: Click "Note A" text in Note B
Step5: "Note A" note should be opened
Step6: Click tomboy from gnome-panel again
Step7: Click "Note A" text in the Note B
Step8: "Note A" note should be opened again

NOTE:
Some problems in accessibility:
(1) context menu of Tomboy on notification area doesn't accessible
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

# Step1: Create a new note named "Note A"
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 1)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

new1_frame = app.findFrame(re.compile('^New Note'))
new1_text = new1_frame.findText(None)
new1_text.enterText("Note A\r\n\r\nThis is a note for test case 1014763")

# Close the note
new1_frame.altF4()

# Step2: Create the second note named "Note B"
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 1)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

new2_frame = app.findFrame(re.compile('^New Note'))
new2_text = new2_frame.findText(None)

# Step3: Insert some test "Note A should be a link" into Note B
new2_text.enterText("Note B\r\n\r\nNote A should be a link")
sleep(config.SHORT_DELAY)

# Step4: Click "Note A" text in Note B
bbox = new2_text._accessible.queryComponent().getExtents(pyatspi.DESKTOP_COORDS)
sleep(config.SHORT_DELAY)

x = bbox.x
y = bbox.y

procedurelogger.action('Click "Note A" from text')
pyatspi.Registry.generateMouseEvent(x+10, y+50, 'b1c')
sleep(config.SHORT_DELAY)

# Step5: "Note A" note should be opened
note_a = app.findFrame("Note A")

# Close note and quit tomboy
new2_frame.altF4()
note_a.altF4()

# Step6: Click tomboy from gnome-panel again
tomboy_panel.mouseClick(log=False)
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 7)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

# Step7: Click "Note A" text in the Note B
note_b = app.findFrame("Note B")
note_text = note_b.findText(None)

bbox = note_text._accessible.queryComponent().getExtents(pyatspi.DESKTOP_COORDS)
sleep(config.SHORT_DELAY)

x = bbox.x
y = bbox.y

procedurelogger.action('Click "Note A" from text again')
pyatspi.Registry.generateMouseEvent(x+10, y+50, 'b1c')
sleep(config.SHORT_DELAY)

# Step8: "Note A" note should be opened again
note_a = app.findFrame("Note A")

# Delete Note A
note_a.findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)
app.findDialog(None).findPushButton("Delete").mouseClick()

note_a.assertClosed()

# Delte Note B
note_b.findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)
app.findDialog(None).findPushButton("Delete").mouseClick()

note_b.assertClosed()

# Quit Tomboy
quitTomboy(tomboy_panel)

