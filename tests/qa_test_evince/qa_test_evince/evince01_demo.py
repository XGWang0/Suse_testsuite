#!/usr/bin/env python

##############################################################################
# Description: Evince test logic
# Written by: Leon
##############################################################################

# The docstring below  is used in the generated log file
"""
  ===Evince test demo===
Step1: From <File> menu select <Open> menu item to invoke Open Document dialog
Step2: Click ToggleButton "Type a file name" to show the textbox of input URL 
Step3: Input pdf path and press Open button
Step4: Assert if there's a label "of 1"
Step5: Click that ToggleButton again to clean the test env.
Step6: Click Cancel button of the dialog and close the whole frame
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
lFrame = app.evinceFrame

# Step1: From <File> menu select <Open> menu item to invoke Open Document dialog
menubar = lFrame.findMenuBar(None)
menubar.select(['File', 'Open...'])
sleep(config.SHORT_DELAY)

# Step2: Click ToggleButton "Type a file name" to show the textbox of input URL 
newdialog = lFrame.findNewItem("Dialog", "Open Document")
sleep(config.SHORT_DELAY)
newdialog.clickItem("ToggleButton", "Type a file name")
sleep(config.SHORT_DELAY)

# Step3: Input pdf path and press Open button
textdata={"0":"/usr/share/doc/packages/iproute2/rtstat.pdf"}
newdialog.inputItem("Texts", textdata)
sleep(config.SHORT_DELAY)
newdialog.clickItem("PushButton", "Open")
sleep(config.SHORT_DELAY)

# Step4: Assert if there's a label "of 1"
lFrame.assertobject("Label", "of 1")
sleep(config.SHORT_DELAY)

# Step5: Click that ToggleButton again to clean the test env.
menubar.select(['File', 'Open...'])
sleep(config.SHORT_DELAY)
newdialog = lFrame.findNewItem("Dialog", "Open Document")
sleep(config.SHORT_DELAY)
newdialog.clickItem("ToggleButton", "Type a file name")
sleep(config.SHORT_DELAY)

# Step6: Click Cancel button of the dialog and close the whole frame
newdialog.clickItem("PushButton", "Cancel")
sleep(config.SHORT_DELAY)
menubar.select(['File', 'Close'])
