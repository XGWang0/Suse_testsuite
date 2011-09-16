#!/usr/bin/env python

##############################################################################
# Written by:  Cachen Chen <cachen@novell.com>
# Date:        07/22/2010
# Description: Evince test for "Page Setup" MenuItem
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Evince Menu Functions test==
==="Page Setup" MenuItem test===
Step1: From <File> menu select <Page Setup...> menu item to invoke new dialog
Step2: Change Paper size by choosing 'A4' from size combobox
Step3: Change Orientation to Landscape
Step4: Apply the changes to close the dialog
"""

# imports
from os import system
from strongwind import *

# open the label sample application
try:
  app = launchApp("/usr/bin/evince", "evince")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter

eFrame = app.evinceFrame

print doc
# Step1: Open an exited pdf
menubar = eFrame.findMenuBar(None)
try:
    menubar.select(['File', '1.  rtstat.pdf'])
except SearchError:
    from evince_frame import *
    openFile(eFrame, app)

# Step2: From <File> menu select <Page Setup...> menu item to invoke new dialog
try:
    menubar.select(['File', 'Page Setup...'])
except SearchError:
    menubar.select(['File', 'Print Setup...'])
sleep(config.SHORT_DELAY)
page_dialog = app.findDialog('Page Setup')

# Step3: Change Paper size by choosing 'A4' from size combobox
size_combo = page_dialog.findAllComboBoxs(None)[0]
sleep(config.SHORT_DELAY)
size_combo.mouseClick(log="Left click Page size combo box")
sleep(config.SHORT_DELAY)
size_combo.findAllMenuItems(None)[2].mouseClick(log="Left click A4 menu item")
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("size is changed to A4")
try:
    new_label = page_dialog.findLabel("8.27 x 11.69 inch")
except SearchError:
    new_label = page_dialog.findLabel("210 x 297 mm")

# Step4: Change Orientation to Landscape
page_dialog.findRadioButton("Landscape").mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("%s RadioButton is checked" % "Landscape")
assert page_dialog.findRadioButton("Landscape").checked == True, \
                                      "Orientation type should be checked"

# Step5: Apply the changes to close the dialog
page_dialog.findPushButton("Apply").mouseClick()
sleep(config.SHORT_DELAY)
page_dialog.assertClosed()

# Step6 Close the application
menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
eFrame.assertClosed()
