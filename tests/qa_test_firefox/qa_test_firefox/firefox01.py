#!/usr/bin/env python
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************
#

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

