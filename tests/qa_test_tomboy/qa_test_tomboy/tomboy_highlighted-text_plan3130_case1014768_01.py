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
# Date:        12/15/2010
# Description: Tomboy Highlighted Text Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Highlighted Text test===
Step1: Create a new note
Step2: Insert text "Note A\rHere is a test for case 1014768"
Step3: Get bg-color text attributes of second line that should be empty
Step4: Remove text
Step5: Enable from Text -> Highlight
Step6: Insert text "Note A\rHere is a test for case 1014768"
Step7: Reopen the note
Step8: The highlighted text was saved and retrieved properly by get bg-color text attributes of second line that should be bg-color:65535,65535,0
Step9: Restart Tomboy and open the note
Step10: The highlighted text was saved and retrieved properly by get bg-color text attributes of second line that should be bg-color:65535,65535,0
"""
# imports
import os
from strongwind import *
from tomboy_frame import *

print doc

def checkHighlight(accessible, attribute='', offset=0):
    """
    Ensure Highlight is actived by checking bg-color attribute
    """
    procedurelogger.action('Make sure highlighted text was saved and retrieved properly')
    note_text = accessible.findText(None)
    obj_text = note_text._accessible.queryText()
    attr_bg = obj_text.getAttributes(offset)[0]

    procedurelogger.expectedResult('bg-color attribute of second line should be %s' % attribute)
    assert attribute == attr_bg, "bg-color expected: %s, actual is: %s" % \
                                                    (attribute, attr_bg)

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

note_new = app.findFrame(re.compile('^New Note'))

# Step2: Insert text "Note A\rHere is a test for case 1014768"
note_text = note_new.findText(None)
note_text.enterText("Note A\r\nHere is a test for case 1014768")

# Step3: Get bg-color text attributes of second line that should be empty
checkHighlight(note_new, attribute='', offset=10)

# Step4: Remove text
note_text.deleteText()

# Step5: Enable from Text -> Highlight or <Ctrl>H
note_new.findToggleButton("Text").mouseClick()
sleep(config.SHORT_DELAY)

#app.findWindow(None).findCheckBox("Highlight").mouseClick()
hightlight_item = pyatspi.findDescendant(app.findWindow(None), lambda x: x.name == 'Highlight')
hightlight_item.mouseClick()
sleep(config.SHORT_DELAY)

# Step6: Insert text "Note A\rHere is a test for case 1014768"
note_text.typeText("Note A")
note_text.keyCombo('enter')
note_text.typeText("Here is a test for case 1014768")

# Step7: Reopen the note
note_new.altF4()

tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 6)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

note_a = app.findFrame("Note A")

# Step8: The highlighted text was saved and retrieved properly by get bg-color text attributes of second line that should be bg-color:65535,65535,0
checkHighlight(note_a, attribute='bg-color:65535,65535,0', offset=10)

# Step9: Restart Tomboy and open the note
quitTomboy(tomboy_panel)

(app, subproc) = cache.launchApplication('/usr/bin/tomboy', app_name, wait=config.MEDIUM_DELAY)

# Find tomboy on panel
tomboy_panel = tomboyPanel()

note_a = app.findFrame("Note A")

# Step10: The highlighted text was saved and retrieved properly by get bg-color text attributes of second line that should be bg-color:65535,65535,0
checkHighlight(note_a, attribute='bg-color:65535,65535,0', offset=10)

# Delete Note A
deleteNote(app, note_a)

# Quit Tomboy
quitTomboy(tomboy_panel)

