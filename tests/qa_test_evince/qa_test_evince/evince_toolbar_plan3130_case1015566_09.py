#!/usr/bin/env python

##############################################################################
# Written by:  Calen Chen <cachen@novell.com>
# Date:        09/27/2010
# Description: Evince test for "Toolbar" MenuItem
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Evince Menu Functions test==
==="Toolbar" MenuItem test===
Step1: Open a pdf
Step2: From <Edit> menu select <Toolbar> menu item
Step3: Make sure "Toolbar Editor" dialog appears
Step4: Drag "Reload" icon from dialog to the toolbar
Step5: Make sure "Reload" push button appears in toolbar, disappears in dialog
Step6: Drag "Reload" push button from toolbar to dialog
Step7: Make sure "Reload" push button appears in dialog, disappears in toolbar
Step8: Close Toolbar Editor dialog
"""

# imports
from os import system
from strongwind import *
from evince_frame import *

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
    openFile(eFrame, app)

toolbar = eFrame.findAllToolBars(None)[0]

# Step2: From <Edit> menu select <Toolbar> menu item
menubar.findMenu("Edit").mouseClick()
sleep(config.SHORT_DELAY)

menubar.findMenuItem("Toolbar").mouseClick()
sleep(config.SHORT_DELAY)

# Step3: Make sure "Toolbar Editor" dialog appears
toolbar_dialog = app.findDialog("Toolbar Editor")
#drag(fromXY=(317,178), toXY=(600,700), log=False)

# Step4: Drag "Reload" icon from dialog to the toolbar
reload_label = toolbar_dialog.findLabel("Reload")
drag(reload_label, toolbar)

# Step5: Make sure "Reload" push button appears in toolbar, disappears in dialog
procedurelogger.expectedResult("%s appears in toolbar, disappears in dialog" % \
                                                             "Reload")
reload_button = toolbar.findPushButton("Reload")

try:
    toolbar_dialog.findLabel("Reload")
except SearchError:
    assert True, "Reload should not appears in dialog"

# Step6: Drag "Reload" icon from toolbar to the dialog
drag(reload_button, toolbar_dialog)

# Step7: Make sure "Reload" appears in dialog, disappears in toolbar
procedurelogger.expectedResult("%s appears in dialog, disappears in toolbar" % \
                                                               "Reload")
toolbar_dialog.findLabel("Reload")

try:
    toolbar.findPushButton("Reload")
except SearchError:
    assert True, "Reload should not appears in toolbar"

# Step8: Close Toolbar Editor dialog
toolbar_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)

# Step9: Close the application
menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
eFrame.assertClosed()
