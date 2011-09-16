#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        10/18/2010
# Description: Firefox Bookmarks Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===Bookmarks test===
Step1: Open browser to http://www.opensuse.org/en/
Step2: Use Bookmarks | Bookmark This Page to add a bookmark
Step3: Select Bookmarks | Organize Bookmarks
Step4: Locate new bookmark and double-click to load http://www.opensuse.org/en/

NOTE: 
Some accessibility problems in Firefox:
(1) "Bookmark This Page" window doesn't accessible, use "Bookmark All Tabs..." 
to instead in this test
(2) Unidentified encode key of "..." in MenuItem name, use click to instead select
"""

# imports
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# Step1: Open browser
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# Load http://www.opensuse.org/en/
web = "http://www.opensuse.org/en/"
entry = fFrame.findEntry("Search Bookmarks and History")
procedurelogger.action('Load to %s' % web)
entry.text = web
entry.mouseClick()
sleep(config.SHORT_DELAY)
fFrame.keyCombo("enter", grabFocus=False)
sleep(config.MEDIUM_DELAY)

procedurelogger.expectedResult('%s frame appears' % web)
fFrame.findDocumentFrame(re.compile('penSUSE.org'))

# Step2: Use Bookmarks | Bookmark This Page to add a bookmark
fFrame.findMenuItem("New Tab", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)
fFrame.findMenu("Bookmarks").mouseClick()
sleep(config.SHORT_DELAY)

# Unidentified encode key of "..." in the name, use click to instead select
#menubar.select(['Bookmarks', 'Bookmarks All Tabs...'])
bm_menuitem = fFrame.findMenuItem(re.compile('^Bookmark All Tabs'))
bm_menuitem.click(log=True)
sleep(config.SHORT_DELAY)

# New Bookmarks dialog appears, add openSUSE bookmarks
b_dialog = app.findDialog("New Bookmarks")
b_dialog.findEntry("Name:").typeText("openSUSE")
sleep(config.SHORT_DELAY)
b_dialog.findPushButton("Add Bookmarks").mouseClick()
sleep(config.SHORT_DELAY)
b_dialog.assertClosed

# Step3: Select Bookmarks | Organize Bookmarks
# Unidentified encode key of "..." in the name, use click to instead select
#menubar.select(['Bookmarks', 'Organize Bookmarks...'])
ob_menuitem = fFrame.findMenuItem(re.compile('^Organize Bookmarks'), \
                                                        checkShowing=False)
ob_menuitem.click(log=True)
sleep(config.SHORT_DELAY)
ob_frame = app.findFrame("Library")

# Search for "openSUSE" Bookmarks
book_menu = ob_frame.findListItem("Bookmarks Menu")
if book_menu.expanded:
    pass
else:
    book_menu.expand(log=True)
    sleep(config.SHORT_DELAY)
    
ob_frame.findListItem("openSUSE").mouseClick()
sleep(config.SHORT_DELAY)

# Step4: Locate new bookmark and double-click to load http://www.opensuse.org/en/
suse_cell = ob_frame.findTableCell("openSUSE.org")

procedurelogger.action('double click %s' % suse_cell)
x, y = suse_cell._getAccessibleCenter()
pyatspi.Registry.generateMouseEvent(x, y, 'b1d')
sleep(config.MEDIUM_DELAY)

# Make sure there are two "openSUSE.org" document frame appear
procedurelogger.expectedResult('make sure there are 2 "openSUSE.org" document frame appear')
suse_frames = fFrame.findAllDocumentFrames("openSUSE.org", checkShowing=False)
assert len(suse_frames) == 2, \
                 "%s openSUSE.org to be found" % len(suse_frames)

# Active Library frame, Clear the existing Bookmarks
ob_menuitem.click(log=True)
sleep(config.SHORT_DELAY)   
ob_frame.findListItem("openSUSE").mouseClick()
sleep(config.SHORT_DELAY)
ob_frame.findMenu("Organize").mouseClick()
sleep(config.SHORT_DELAY)
ob_frame.findMenuItem("Delete").mouseClick()
sleep(config.SHORT_DELAY)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
quitMultipleTabs(app)
app.assertClosed()
