#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
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
#


##############################################################################
# Written by:  Leon Ling Wang <lwang@novell.com>
#              Cachen Chen <cachen@novell.com>
# Date:        07/22/2010
# Description: Evince test logic
##############################################################################

# The docstring below  is used in the generated log file
"""

==Evince Menu Functions test==
"""

# imports
from strongwind import *

# open the label sample application
try:
  app = launchApp("/usr/bin/evince", "evince")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter

eFrame = app.evinceFrame

doc="""

==="Open..." MenuItem test===
Step1: From <File> menu select <Open...> menu item to invoke Open Document dialog
Step2: Click ToggleButton "Type a file name" to show the textbox of input URL 
Step3: Input pdf path and press Open button
Step4: Assert frame with new name
Step5: Click that ToggleButton again to clean the test env.
"""
print doc
# Step1: From <File> menu select <Open> menu item to invoke Open Document dialog
menubar = eFrame.findMenuBar(None)
menubar.select(['File', 'Open...'])
sleep(config.SHORT_DELAY)

# Step2: Click ToggleButton "Type a file name" to show the textbox of input URL 
open_dialog = eFrame.findNewItem("Dialog", "Open Document")
sleep(config.SHORT_DELAY)
if not open_dialog.findToggleButton("Type a file name").checked:
    open_dialog.clickItem("ToggleButton", "Type a file name")
else:
    pass
sleep(config.SHORT_DELAY)

# Step3: Input pdf path and press Open button
textdata={"0":"/usr/share/doc/packages/iproute2/rtstat.pdf"}
open_dialog.inputItem( "Texts", textdata)
sleep(config.SHORT_DELAY)
open_dialog.clickItem("PushButton", "Open")
sleep(config.SHORT_DELAY)
open_dialog.assertClosed()

# Step4: Assert frame with new name
app.assertobject("Frame", "rtstat.dvi (rtstat.pdf)")
sleep(config.SHORT_DELAY)

# Step5: Click that ToggleButton again to clean the test env.
menubar.select(['File', 'Open...'])
sleep(config.SHORT_DELAY)
open_dialog = eFrame.findNewItem("Dialog", "Open Document")
sleep(config.SHORT_DELAY)
open_dialog.clickItem("ToggleButton", "Type a file name")
sleep(config.SHORT_DELAY)

# Step6: Click Cancel button of the dialog and close the whole frame
open_dialog.clickItem("PushButton", "Cancel")
sleep(config.SHORT_DELAY)
open_dialog.assertClosed()

doc="""

==="Open a Copy" MenuItem test===
Step1: From <File> menu select <Open a Copy> menu item to copy a new frame window
Step2: Assert there are 2 frame with the same name
Step3: Close the copy frame
"""
print doc
# Step1: From <File> menu select <Open a Copy> menu item to copy a new frame window
menubar.select(['File', 'Open a Copy'])
sleep(config.SHORT_DELAY)

# Step2: Assert there are 2 frame with the same name
evince_frames = app.findAllFrames(re.compile('^rtstat.dvi'))
procedurelogger.expectedResult('there are 2 %s appears.' % eFrame.name)
assert len(evince_frames) == 2, "new frame should be copied"

#Step3: Close the copy frame
new_frame_menubar = evince_frames[1].findMenuBar(None)
new_frame_menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
evince_frames[1].assertClosed()

doc="""

==="Save a Copy" MenuItem test===
Step1: From <File> menu select <Save a Copy...> menu item to invoke new dialog
Step2: assert the file's name is the same as the opened file
Step3: Save the file to the default path, or replace the exists file
Step4: assert Save a Copy dialog closed
"""
print doc
# Step1: From <File> menu select <Save a Copy...> menu item to invoke new dialog
menubar.select(['File', 'Save a Copy...'])
sleep(config.SHORT_DELAY)
save_dialog = app.findDialog('Save a Copy')

# Step2: assert the file's name is the same as the opened file
procedurelogger.expectedResult("text in Name text box is \
                                            the same as the opened file's name")
assert save_dialog.findText(None).text == "rtstat.pdf", \
                                         "expected: rtstat.pdf, actual: %s" %\
                                                   save_dialog.findText(None).text

# Step3: Save the file to the default path, or replace the exists file
save_dialog.findPushButton("Save").click()
sleep(config.SHORT_DELAY)
try:
    alert = app.findAlert(None)
    alert.findPushButton("Replace").click()
except SearchError:
    pass

# Step3: assert Save a Copy dialog closed
save_dialog.assertClosed()

doc="""

==="Page Setup" MenuItem test===
Step1: From <File> menu select <Page Setup...> menu item to invoke new dialog
Step2: Change Paper size by choosing 'A4' from size combobox
Step3: Change Orientation to Landscape
Step4: Apply the changes to close the dialog
"""
print doc
# Step1: From <File> menu select <Page Setup...> menu item to invoke new dialog
menubar.select(['File', 'Page Setup...'])
sleep(config.SHORT_DELAY)
page_dialog = app.findDialog('Page Setup')

# Step2: Change Paper size by choosing 'A4' from size combobox
procedurelogger.expectedResult("%s menu item is chosed, %s label appears" %\
                                                ("A4", "8.27 x 11.69 inch"))
size_combo = page_dialog.findAllComboBoxs(None)[0]
sleep(config.SHORT_DELAY)
size_combo.mouseClick(log="Left click Page size combo box")
sleep(config.SHORT_DELAY)
size_combo.findAllMenuItems(None)[2].mouseClick(log="Left click A4 menu item")
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("size is changed to A4, \
                               label is updated to \"8.27 x 11.69 inch\" ")
assert page_dialog.findLabel("8.27 x 11.69 inch"), \
                              "label %s doesn't appears" % "8.27 x 11.69 inch"

# Step3: Change Orientation to Landscape
page_dialog.findRadioButton("Landscape").mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("%s RadioButton is checked" % "Landscape")
assert page_dialog.findRadioButton("Landscape").checked == True, \
                                      "Orientation type should be checked"

# Step4: Apply the changes to close the dialog
page_dialog.findPushButton("Apply").mouseClick()
sleep(config.SHORT_DELAY)
page_dialog.assertClosed()

doc="""

==="Print and Print Preview" MenuItem test===
Step1: From <File> menu select <Print...> menu item to invoke Print dialog
Step2: Select Print to File, Updage Name to 'test.svg' and Save in folder to Document, Output as SVG, choose Current Page In General tab page
Step3: Change Pages per side, change Page ordering, change Only print and Scale in Page Setup tab page
Step4: Click Print Preview push button to invoke a new application
Step5: Click Print push button in the new application window
Step6: From <File> menu select <Open...> menu item to invoke dialog, assert 'test.svg' item is in Document folder
"""
print doc

# remove the exist file first
import os
home = os.getenv("HOME")
if os.path.isfile('%s/Desktop/test.svg' % home):
    os.remove('%s/Desktop/test.svg' % home)

# Step1: From <File> menu select <Print...> menu item to invoke Print dialog
menubar.select(['File', 'Print...'])
sleep(config.SHORT_DELAY)
print_dialog = app.findDialog("Print")

# Step2: Select Print to File, Updage Name to 'test.svg' and Save in folder to 
# Document, Output as SVG, choose Current Page In General tab page
general_tab = print_dialog.findPageTab("General")
print_to_file_tablecell = general_tab.findTableCell("Print to File")
print_to_file_tablecell.mouseClick()
sleep(config.SHORT_DELAY)
general_tab.findText(None, labelledBy="Name:").text = "test"
sleep(config.SHORT_DELAY)
general_tab.findMenuItem("Desktop", checkShowing=False).click()
sleep(config.SHORT_DELAY)
general_tab.findRadioButton("PDF").mouseClick()
sleep(config.SHORT_DELAY)
general_tab.findRadioButton("SVG").mouseClick()
sleep(config.SHORT_DELAY)
general_tab.findRadioButton("Current Page").mouseClick()
sleep(config.SHORT_DELAY)

# Step3: Change Pages per side, change Only print and Scale in Page Setup tab page
page_setup_tab = print_dialog.findPageTab("Page Setup")
page_setup_tab.mouseClick()
sleep(config.SHORT_DELAY)
page_setup_tab.findMenuItem("2", checkShowing=False).click()
sleep(config.SHORT_DELAY)
page_setup_tab.findMenuItem("All sheets", checkShowing=False).click()
sleep(config.SHORT_DELAY)
page_setup_tab.findSpinButton(None, labelledBy="Scale:").value = 110
sleep(config.SHORT_DELAY)

# Step4: Click Print Preview push button to invoke a new application
print_dialog.findPushButton("Print Preview").mouseClick()
sleep(config.SHORT_DELAY)
preview_app = cache._desktop.findApplication("evince-previewer", checkShowing=False)
cache.addApplication(preview_app)

# Step5: Click Print push button in the new application window
preview_app.findPushButton("Print").click()
sleep(config.SHORT_DELAY)
preview_app.assertClosed()

# Step6: From <File> menu select <Open...> menu item to invoke dialog, 
# assert 'test.svg' item is in Document folder 
menubar.select(['File', 'Open...'])
sleep(config.SHORT_DELAY)
open_dialog = app.findDialog("Open Document")
open_dialog.findTableCell("Desktop").mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("%s should in the file list" % "test.svg")
assert open_dialog.findTableCell("test.svg").showing == True, \
                                             "doesn't find test.svg file"

# Close the application
menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
eFrame.assertClosed()

