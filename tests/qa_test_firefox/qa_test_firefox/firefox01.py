#!/usr/bin/env python
##############################################################################
# Description: Test logic of Firefox
# Written by Leon
##############################################################################
# The docstring below  is used in the generated log file
"""
       ===Firefox test demo===
Step1: Input "opensuse.org" in google search bar
Step2: Press Enter to launch the search
Step3: Click the 1st match "openSUSE.org"
Step4: Click Menubar "Bookmarks"->"Bookmark This Page"
Step5: Press Enter to save the bookmark
Step6: Assert if the bookmark is there, and close firefox
"""
from firefox_frame import *

# open the label sample application
try:
  app = launchApp("/usr/bin/firefox", "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)

# make sure we got the app back
if app is None:
  exit(4)

# just an alias to make things shorter
lFrame = app.firefoxFrame

# Step1: Input "opensuse.org" in google search bar
sbar = lFrame.findEntry("Search using Google")
sbar.keyCombo('< >', grabFocus=True)
sbar.text="opensuse.org"

# Step2: Press Enter to launch the search
sbar.keyCombo('<Enter>', grabFocus=True)
sleep(config.LONG_DELAY)

# Step3: Click the 1st match "openSUSE.org"
lFrame.clickItem("Link", "openSUSE.org")
sleep(config.LONG_DELAY)

# Step4: Click Menubar "Bookmarks"->"Bookmark This Page"
menubar = lFrame.findMenuBar(None)
menubar.select(['Bookmarks', 'Bookmark This Page'])
sleep(config.SHORT_DELAY)

# Step5: Press Enter to save the bookmark
lFrame.keyCombo("Return")
sleep(config.SHORT_DELAY)

# Step6: Assert if the bookmark is there, and close firefox
assert lFrame.findMenuItem("openSUSE.org", checkShowing=False)
sleep(config.SHORT_DELAY)

# Close application
menubar = lFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
quitMultipleTabs(app)
app.assertClosed()
