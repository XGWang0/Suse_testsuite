#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        10/27/2010
# Description: Firefox Location control Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===Location control test===

Step1: File->Open Location
Step2: Make sure URL Location text fileld is focused
Step3: Type a URL"www.google.com" and click Enter
Step4: Make sure the page is opened
Step5: Select any URL from text field to visit
Step6: Make sure the page is opened
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

# Step1: File->Open Location
fFrame.findMenu("File").mouseClick()
sleep(config.SHORT_DELAY)

fFrame.findMenuItem(re.compile('^Open Location')).mouseClick()
sleep(config.SHORT_DELAY)

# Step2: Make sure URL Location text field is focused
location_entry = fFrame.findEntry("Search Bookmarks and History")

procedurelogger.expectedResult("Make sure URL Location text field is focused")
assert location_entry.focused == True, "URL location text field is not focused"

# Step3: Type a URL"www.google.com" and click Enter
procedurelogger.action('insert %s' % "www.google.com")
location_entry.text = "www.google.com"
location_entry.keyCombo("enter")
sleep(config.LONG_DELAY)

# Step4: Make sure the page is opened
procedurelogger.expectedResult('Make sure "Google" is loaded')
fFrame.findDocumentFrame("Google")

# Step5: Select any URL from text field to visit
buttons = fFrame.findAutocomplete("Search Bookmarks and History").findAllPushButtons(None)
buttons[-1].mouseClick()
sleep(config.SHORT_DELAY)

fFrame.keyCombo("Down", grabFocus=False)
sleep(config.SHORT_DELAY)

fFrame.keyCombo("Down", grabFocus=False)
sleep(config.SHORT_DELAY)

fFrame.keyCombo("enter", grabFocus=False)
sleep(config.MEDIUM_DELAY)

# Step6: Make sure the page is opened
procedurelogger.expectedResult('Make sure the page is updated')
if fFrame.findDocumentFrame(None).name == "Google":
    raise Exception, "ERROR: Google page shouldn't appears again"
    exit(2)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()
