#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        10/19/2010
# Description: Firefox Sidebar Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===Sidebar test===
Step1: Load http://www.mozilla.org/
Step2: Click on View -> Sidebar to open and close the Sidebar
"""

# imports
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# Launch browser
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# Step1: Load http://www.mozilla.org/
entry = fFrame.findEntry("Search Bookmarks and History")
procedurelogger.action('Load to http://www.mozilla.org')
entry.text = "http://www.mozilla.org/"
entry.mouseClick()
sleep(config.SHORT_DELAY)
fFrame.keyCombo("enter", grabFocus=False)
sleep(config.MEDIUM_DELAY)

procedurelogger.expectedResult('mozilla.org frame appears')
fFrame.findDocumentFrame("Home of the Mozilla Project")


# Step2: Click on View -> Sidebar to open each Sidebar
sidebar_menu = fFrame.findMenu("Sidebar", checkShowing=False)
for i in range(sidebar_menu.childCount):
    fFrame.findMenu("View").mouseClick()
    sleep(config.SHORT_DELAY)
    sidebar_menu.mouseClick()
    sleep(config.SHORT_DELAY)
    sidebar_menu.getChildAtIndex(i).mouseClick()
    sleep(config.SHORT_DELAY)
    procedurelogger.expectedResult('%s Sidebar appears' % \
                                     sidebar_menu.getChildAtIndex(i).name)
    sidebar = fFrame.findInternalFrame(sidebar_menu.getChildAtIndex(i).name)

# Close Sidebar
for i in range(sidebar_menu.childCount):
    if sidebar_menu.getChildAtIndex(i).checked:
        sidebar_name = sidebar_menu.getChildAtIndex(i).name
        sidebar_menu.getChildAtIndex(i).click(log=True)
        sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('%s Sidebar disappears' % \
                             sidebar_name)
if sidebar.showing:
    raise Exception, "Sidebar shouldn't appears"
    exit(1)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()
