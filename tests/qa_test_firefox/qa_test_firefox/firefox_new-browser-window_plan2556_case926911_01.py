#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        10/25/2010
# Description: Firefox New Browser window Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===New Browser window test===
Step1: Open a new browser window - File | New Window 
Step2: Make sure there are 2 Frame under Firefox application
Step3: File | New Tab to open a new browser tab
Step4: Make sure there are 2 DocumentFrame under Firefox application
"""
# imports
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# Launch Firefox.
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# Step1: Open a new browser window - File | New Window 
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'New Window'])
sleep(config.SHORT_DELAY)

# Step2: Make sure there are 2 Frame under Firefox application
procedurelogger.expectedResult('Make sure there are 2 Frame under Firefox application')
frames = app.findAllFrames(None)
assert len(frames) == 2, "expected 2 frames, actual is %s" % len(frames)

# Close new frame window
frames[1].altF4()

# Step3: File | New Tab to open a new browser tab
menubar.select(['File', 'New Tab'])
sleep(config.SHORT_DELAY)

# Step4: Make sure there are 2 DocumentFrame under Firefox application
procedurelogger.expectedResult('Make sure there are 2 Frame under Firefox application')
doc_frames = app.findAllDocumentFrames(None, checkShowing=False)
assert len(doc_frames) == 2, "expected 2 frames, actual is %s" % len(doc_frames)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
quitMultipleTabs(app)
fFrame.assertClosed()
