#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        12/21/2010
# Description: Tomboy Print Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Print test===
Step1: Create a new note
Step2: Change font style and size from Text -> Italic, Large
Step3: Insert text "Note A\rHere is a test for case 1014774" 
Step4: Get text attributes of second line that should be 'scale:1.44; style:italic'
Step5: Launch Print dialog from Tool -> Print
Step6: Selete "Print to File" with PDF format to current folder
Step7: Print the note
Step8: Make sure output.pdf is saved in current folder, should manually open the pdf to check text's style and size
"""
# imports
import os
from strongwind import *
from tomboy_frame import *

print doc

def checkStyle(accessible, attribute='', offset=0):
    """
    Ensure text style is the expected attribute
    """
    procedurelogger.action('Make sure text style is the expected attribute')
    note_text = accessible.findText(None)
    obj_text = note_text._accessible.queryText()
    attr_style = obj_text.getAttributes(offset)[0]

    procedurelogger.expectedResult('Text attribute of second line should be %s' % attribute)
    assert attribute == attr_style, "expected: %s, actual is: %s" % \
                                                    (attribute, attr_style)

# Remove the exist output.pdf file to clean up environment
pwd = os.getenv('HOME')

if os.path.exists('%s/output.pdf' % pwd):
    os.system('rm -fr %s/output.pdf' % pwd)

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

note_frame = app.findFrame(re.compile('^New Note'))
note_text = note_frame.findText(None)

# Delete note texts
note_text.deleteText()
sleep(config.SHORT_DELAY)

# Step2: Change font style and size from Text -> Italic, Large
note_frame.findToggleButton("Text").mouseClick()
sleep(config.SHORT_DELAY)

italic_item = pyatspi.findDescendant(app.findWindow(None), lambda x: x.name == 'Italic')
if not italic_item.checked:
    italic_item.mouseClick()
    sleep(config.SHORT_DELAY)

note_frame.findToggleButton("Text").mouseClick()
sleep(config.SHORT_DELAY)

pyatspi.findDescendant(app.findWindow(None), lambda x: x.name == 'Large').mouseClick()
sleep(config.SHORT_DELAY)

# Step3: Update text to "Note A\rHere is a test for case 1014774" 
note_text.typeText("Note A")
note_text.keyCombo('enter')
note_text.typeText("Here is a test for case 1014774")
sleep(config.SHORT_DELAY)

# Step4: Get text attributes of second line that should be 'scale:1.44; style:italic'
checkStyle(note_frame, attribute='scale:1.44; style:italic', offset=10)

# Step5: Launch Print dialog from Tool -> Print
tool_button = note_frame.findAllToggleButtons(None)[1]

tool_button.mouseClick()
sleep(config.SHORT_DELAY)

app.findWindow(None).findMenuItem("Print").mouseClick()
sleep(config.SHORT_DELAY)

print_dialog = app.findDialog("Print")

# Step6: Selete "Print to File" with PDF format to current folder
if app_name is "tomboy":
    print_dialog.findTableCell("Print to File").mouseClick()
    sleep(config.SHORT_DELAY)
else:
    print_dialog.findTableCell("Create a PDF document").mouseClick()
    sleep(config.SHORT_DELAY)

# Step7: Print the note
print_dialog.findMenuItem(os.getenv('USERNAME'), checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

print_dialog.findPushButton("Print").mouseClick()
sleep(config.MEDIUM_DELAY)

print_dialog.assertClosed()

# Step8: Make sure output.pdf is saved in current folder, should manually open the pdf to check text's style and size
procedurelogger.expectedResult('output.pdf is saved in %s' % pwd)
assert os.path.exists('%s/output.pdf' % pwd), \
                                      "There is no output.pdf in %s" % pwd

# Delete Note A
deleteNote(app, note_frame)

# Quit Tomboy
quitTomboy(tomboy_panel)
