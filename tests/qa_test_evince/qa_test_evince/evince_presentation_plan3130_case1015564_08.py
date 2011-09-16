#!/usr/bin/env python

##############################################################################
# Written by:  Cachen Chen <cachen@novell.com>
# Date:        09/26/2010
# Description: Evince test for "Presentation" MenuItem
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Evince Menu Functions test==
==="Presentation" MenuItem test===
Step1: Open a pdf
Step2: From <View> menu select <Presentation> menu item
Step3: Make sure Document View's size is changed to the same as resolution
Step4: Press Esc to leave presentation mode
Step5: Make sure Document View's size is changed to the old one
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

doc_view = eFrame.findUnknown("Document View")
old_size = doc_view._accessible.queryComponent().getSize()

# Step2: From <View> menu select <Fullscreen> menu item
menubar.select(['View', 'Presentation'])
sleep(config.MEDIUM_DELAY)

# Step3: Make sure Document View's size is changed to the same as resolution
expected_size = (gtk.gdk.screen_width(), gtk.gdk.screen_height())
actual_size = doc_view._accessible.queryComponent().getSize()
procedurelogger.expectedResult("the Document View's size should change to %s" % str(expected_size))
assert actual_size == expected_size, "%s doesn't match to %s" % \
                                              (str(actual_size), str(expected_size))

# Step4: Press Esc to leave presentation mode
eFrame.keyCombo("Esc", grabFocus=False)
sleep(config.SHORT_DELAY)

# Step5: Make sure Document View's size is changed to the old one
actual_size = doc_view._accessible.queryComponent().getSize()
procedurelogger.expectedResult("the Document View's size should change to %s" % str(old_size))
assert actual_size == old_size, "%s doesn't match to %s" % \
                                              (str(actual_size), str(old_size))

# Step6 Close the application
menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
eFrame.assertClosed()
