#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        10/26/2010
# Description: Firefox History Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===History test===
Step1: Launch Browse to http://www.mono-project.com/Accessibility
Step2: Open a new Tab 
Step3: Select "Accessibility - Mono" menu item under History Menu to open it
Step4: Make sure there are 2 "Accessibility - Mono" Document Frame
Step5: Clear recent history from Firefox Preferences
Step6: Make sure "Accessibility - Mono" menu item disappears under History Menu

NOTES:
Some different Steps with the test case926906 in Plan2556
"""

# imports
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

try:
  app = launchApp("/usr/bin/firefox", "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# Step1: Launch Browse to http://www.mono-project.com/Accessibility
url_entry = fFrame.findEntry("Search Bookmarks and History")
url_entry.text = "http://www.mono-project.com/Accessibility"
sleep(config.SHORT_DELAY)
url_entry.keyCombo("enter")

procedurelogger.expectedResult('%s document frame appears' % \
                                                  "Accessibility - Mono")
fFrame.findDocumentFrame("Accessibility - Mono")

# Step2: Open a new Tab 
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'New Tab'])
sleep(config.SHORT_DELAY)

# Step3: Select "Accessibility - Mono" menu item in History view to open it
fFrame.findMenu("History").mouseClick()
sleep(config.SHORT_DELAY)
fFrame.findMenuItem("Accessibility - Mono").mouseClick()
sleep(config.MEDIUM_DELAY)

# Step4: Make sure there are 2 "Accessibility - Mono" Document Frame
procedurelogger.expectedResult('There are 2 %s document frame appears' % \
                                                   "Accessibility - Mono")
doc_frames = len(fFrame.findAllDocumentFrames("Accessibility - Mono", \
                                                      checkShowing=False))
assert doc_frames == 2, "expected: 2 %s document frames; actual: %s" % \
                                       ("Accessibility - Mono", doc_frames)

# Step5: Clear recent history from Firefox Preferences
menubar.select(['Edit', 'Preferences'])

# From Privacy Tab, click "clear your recent history"
preferences_frame = app.findFrame("Firefox Preferences")

preferences_frame.findListItem("Privacy").mouseClick()
sleep(config.SHORT_DELAY)

preferences_frame.findLink("clear your recent history").mouseClick()
sleep(config.SHORT_DELAY)

clear_frame = app.findFrame("Clear Recent History")
clear_frame.findMenuItem("Everything", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)
clear_frame.findPushButton("Clear Now").mouseClick()
sleep(config.MEDIUM_DELAY)

preferences_frame.findPushButton("Close").press(log=True)
sleep(config.SHORT_DELAY)
preferences_frame.assertClosed()

menubar.findMenu("History").mouseClick()
sleep(config.SHORT_DELAY)

# Step6: Make sure "Accessibility - Mono" menu item disappears under History Menu
try:
    menubar.findMenu("History").findMenuItem("Accessibility - Mono",\
                                                      checkShowing=False)
except SearchError:
    pass # expected
else:
    assert False, "Accessibility - Mono menu item shouldn't appear"

# Close application
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
quitMultipleTabs(app)
fFrame.assertClosed()
