#!/usr/bin/env python

##############################################################################
# Written by:  Cachen Chen <cachen@novell.com>
# Date:        09/26/2010
# Description: Evince test for "Fullscreen" MenuItem
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Evince Menu Functions test==
==="Fullscreen" MenuItem test===
Step1: Open a pdf
Step2: From <View> menu select <Fullscreen> menu item
Step3: Make sure frame's size is changed to th same as resolution
Step4: Make sure Leave Fullscreen push button is showing
Step5: Click Leave Fullscreen push button
"""

# imports
import gtk
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

# Step2: From <View> menu select <Fullscreen> menu item
menubar.select(['View', 'Fullscreen'])
sleep(config.SHORT_DELAY)

# Step3: Make sure frame's size is changed to th same as resolution
expected_size = (gtk.gdk.screen_width(), gtk.gdk.screen_height())
actual_size = eFrame._accessible.queryComponent().getSize()
procedurelogger.expectedResult("the frame's size should change to %s" % str(expected_size))
assert actual_size == expected_size, "%s doesn't match to %s" % \
                                              (str(actual_size), str(expected_size))

# Step4: Make sure Leave Fullscreen push button appears,
# otherwise, will return SearchError
procedurelogger.expectedResult("%s is showing" % "Leave Fullscreen push button")
leave_full = eFrame.findPushButton("Leave Fullscreen")

# Step5: Click Leave Fullscreen push button
leave_full.mouseClick()
sleep(config.SHORT_DELAY)

# Step6 Close the application
menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
eFrame.assertClosed()
