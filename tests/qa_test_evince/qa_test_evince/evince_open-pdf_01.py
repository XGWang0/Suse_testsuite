#!/usr/bin/env python

##############################################################################
# Written by:  Leon Ling Wang <lwang@novell.com>
#              Cachen Chen <cachen@novell.com>
# Date:        07/22/2010
# Description: Evince test for "Open..." MenuItem
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Evince Menu Functions test==
==="Open..." MenuItem test===
Step1: From <File> menu select <Open...> menu item to invoke Open Document dialog
Step2: Click ToggleButton "Type a file name" to show the textbox of input URL 
Step3: Input pdf path and press Open button
Step4: Assert frame with new name
Step5: Click that ToggleButton again to clean the test env.
"""

# imports
from strongwind import *
from evince_frame import openFile

# open the label sample application
try:
  app = launchApp("/usr/bin/evince", "evince")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
eFrame = app.evinceFrame

print doc
# Open an PDF
openFile(eFrame, app)

# Close application
menubar = eFrame.findMenuBar(None)
menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
eFrame.assertClosed()
