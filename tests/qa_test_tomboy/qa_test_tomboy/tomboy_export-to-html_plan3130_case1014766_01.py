#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
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
# Date:        12/14/2010
# Description: Tomboy Export To HTML Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Export To HTML test===
Step1: Create a new note
Step2: Insert text "Note A\r\nHere is a link to Note B"
Step3: Create a new note
Step4: Insert text "Note B\r\nHere is a link to Note C"
Step5: Create a new note
Step6: Insert text "Note C\r\nHere is a note for case1014766
Step7: Active Note A, From Tools -> Export to HTML, disable "Export linked notes" check box, Save "Note A.html" to ~/Desktop
Step8: Auto-launch Note A.html in Firefox, make sure there are only one heading
Step9: Active Note A, From Tools -> Export to HTML, enable "Export linked notes" check box, Save "Note A.html" to ~/Desktop
Step10: Auto-launch Note A.html in Firefox, make sure there are only two heading
Step11: Active Note A, From Tools -> Export to HTML, enable "Export linked notes" check box, enable "Include all other linked notes", Save "Note A.html" to ~/Desktop
Step12: Auto-launch Note A.html in Firefox, make sure there are only three heading
"""
# imports
import os
from strongwind import *
from tomboy_frame import *

print doc

def launchExport():
    new1_frame.findAllToggleButtons(None)[1].click(log=True)
    sleep(config.SHORT_DELAY)
    app.findWindow(None).findMenuItem("Export to HTML").click(log=True)
    sleep(config.SHORT_DELAY)

    export_dialog = app.findDialog("Destination for HTML Export")
    return export_dialog

def saveHTML():
    procedurelogger.action('Save "Note A.html" to /tmp')
    export_dialog.findText(None, labelledBy="Name:").text = "/tmp/Note A.html"

    export_dialog.findPushButton("Save").mouseClick()
    sleep(config.SHORT_DELAY)

    try:
        app.findAlert(None).findPushButton("Replace").mouseClick()
        sleep(config.SHORT_DELAY)
    except SearchError:
        pass         

    export_dialog.assertClosed()

def checkLinks(expected_links=[]):
    procedurelogger.action("Auto-launch Note A.html in Firefox")
    firefox_app = cache._desktop.findApplication("Firefox")

    procedurelogger.expectedResult('Make sure there are only "Note A" heading')
    note_headings = firefox_app.findAllHeadings(None)
    texts = []
    for i in note_headings:
        texts.append(i.text.replace('\n',''))

    assert texts == expected_links, "Should only %s exist, actual: %s" % \
                                               (expected_links, texts)

    #firefox_app.findMenuItem("Quit", checkShowing=False).click(log=True)
    firefox_app.keyCombo('<Alt>F4')
    sleep(config.SHORT_DELAY)

    try:
        quit_dialog = app.findDialog("Quit Firefox")
    except:
        pass
    else:
        quit_dialog.findPushButton("Quit").mouseClick()
        sleep(config.SHORT_DELAY)

    firefox_app.assertClosed()

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

# Step2: Insert text "Note A\r\nHere is a link to Note B"
new1_text = new1_frame.findText(None)
new1_text.enterText("Note A\r\nHere is a link to Note B")

procedurelogger.expectedResult('The note is renamed to "Note A"')
assert new1_frame.name == "Note A", "Name shouldn't be %s" % new1_frame.name

# Step3: Create a new note
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 1)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

new2_frame = app.findFrame(re.compile('^New Note'))

# Step4: Insert text "Note B\r\nHere is a link to Note C"
new2_text = new2_frame.findText(None)
new2_text.enterText("Note B\r\nHere is a link to Note C")

procedurelogger.expectedResult('The note is renamed to "Note B"')
assert new2_frame.name == "Note B", "Name shouldn't be %s" % new2_frame.name

# Step5: Create a new note
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 1)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

new3_frame = app.findFrame(re.compile('^New Note'))

# Step6: Insert text "Note C\r\nHere is a note for case1014766"
new3_text = new3_frame.findText(None)
new3_text.enterText("Note C\r\nHere is a note for case1014766")

procedurelogger.expectedResult('The note is renamed to "Note C"')
assert new3_frame.name == "Note C", "Name shouldn't be %s" % new3_frame

# Step7: Active Note A, From Tools -> Export to HTML 
export_dialog = launchExport()

# Disable "Export linked notes" check box
export_check = export_dialog.findCheckBox("Export linked notes")
export_all_check = export_dialog.findCheckBox("Include all other linked notes")

for check_item in [export_check, export_all_check]:
    if check_item.checked:
        check_item.mouseClick()
        sleep(config.SHORT_DELAY)

# Save "Note A.html" to /tmp
saveHTML()

# Step8: Auto-launch Note A.html in Firefox, make sure there are only one heading
checkLinks(expected_links=['Note A'])

# Remove Note A.html
os.remove('/tmp/Note A.html')

# Step9: Active Note A, From Tools -> Export to HTML
export_dialog = launchExport()

# Enable "Export linked notes" check box
export_check = export_dialog.findCheckBox("Export linked notes")
export_all_check = export_dialog.findCheckBox("Include all other linked notes")

if not export_check.checked:
    export_check.mouseClick()
    sleep(config.SHORT_DELAY)
if export_all_check.checked:
    export_all_check.mouseClick()
    sleep(config.SHORT_DELAY)

# Save "Note A.html" to /tmp
saveHTML()

# Step10: Auto-launch Note A.html in Firefox, make sure there are only two heading
checkLinks(expected_links=['Note A', 'Note B'])

# Remove Note A.html
os.remove('/tmp/Note A.html')

# Step11: Active Note A, From Tools -> Export to HTML
export_dialog = launchExport()

# Enable "Export linked notes" check box, enable "Include all other linked notes"
export_check = export_dialog.findCheckBox("Export linked notes")
export_all_check = export_dialog.findCheckBox("Include all other linked notes")

if not export_check.checked:
    export_check.mouseClick()
    sleep(config.SHORT_DELAY)
if not export_all_check.checked:
    export_all_check.mouseClick()
    sleep(config.SHORT_DELAY)

# Save "Note A.html" to /tmp
saveHTML()

# Step12: Auto-launch Note A.html in Firefox, make sure there are only three heading
checkLinks(expected_links=['Note A', 'Note B', 'Note C'])

# Remove Note A.html
os.remove('/tmp/Note A.html')

# Delete the note
deleteNote(app, new3_frame)

deleteNote(app, new2_frame)

deleteNote(app, new1_frame)

# Quit Tomboy
quitTomboy(tomboy_panel)

