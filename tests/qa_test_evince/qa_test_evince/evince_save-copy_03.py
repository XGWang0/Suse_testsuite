#!/usr/bin/env python

##############################################################################
# Written by:  Cachen Chen <cachen@novell.com>
# Date:        07/22/2010
# Description: Evince test for "Save a copy" MenuItem
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Evince Menu Functions test==
==="Save a Copy" MenuItem test===
Step1: From <File> menu select <Save a Copy...> menu item to invoke new dialog
Step2: assert the file's name is the same as the opened file
Step3: Save the file to the default path, or replace the exists file
Step4: assert Save a Copy dialog closed
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

# Step2: From <File> menu select <Save a Copy...> menu item to invoke new dialog
menubar.select(['File', 'Save a Copy...'])
sleep(config.SHORT_DELAY)
save_dialog = app.findDialog('Save a Copy')

# Step3: assert the file's name is the same as the opened file
procedurelogger.expectedResult("text in Name text box is \
                                            the same as the opened file's name")
assert save_dialog.findText(None).text == "rtstat.pdf", \
                                         "expected: rtstat.pdf, actual: %s" %\
                                                   save_dialog.findText(None).text

# Step4: Save the file to the default path, or replace the exists file
save_dialog.findPushButton("Save").click()
sleep(config.SHORT_DELAY)
try:
    alert = app.findAlert(None)
    alert.findPushButton("Replace").click()
except SearchError:
    pass

# Step3: assert Save a Copy dialog closed
save_dialog.assertClosed()

# Step5 Close the application
menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
eFrame.assertClosed()
