#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        10/25/2010
# Description: Firefox Search Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===Search test===
Search using the embedded search bar in the top right of the browser.
Vary Search Engines between tests

Step1: From Tools -> Web Search focus to the search bar
Step2: Entry of search bar is focused
Step3: Insert 'Novell' and make search
Step4: Make sure to load New Document Frame the name start with 'Novell'
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

# Step1: From Tools -> Web Search focus to the search bar
menubar = fFrame.findMenuBar(None)
menubar.select(['Tools', 'Web Search'])
sleep(config.SHORT_DELAY)

# Step2: Entry of search bar is focused
procedurelogger.expectedResult('Make sure Entry of search bar is focused')
search_entry = fFrame.findEntry("Search using Google")
assert search_entry.focused == True, "Search entry should be focused"

# Step3: Insert 'Novell' and make search
search_entry.insertText("Novell")
sleep(config.SHORT_DELAY)
fFrame.findAllPushButtons("Search")[1].mouseClick()
sleep(config.SHORT_DELAY)

# Step4: Make sure to load New Document Frame the name start with 'Novell'
procedurelogger.expectedResult('Make sure to load New Document Frame')
app.findDocumentFrame(re.compile('^Novell'))

# Close application
fFrame.findMenu("File").click(log=True)
sleep(config.SHORT_DELAY)
fFrame.findMenuItem("Quit", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)
app.assertClosed()
