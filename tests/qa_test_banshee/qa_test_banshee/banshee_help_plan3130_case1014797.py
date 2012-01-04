#!/usr/bin/env python
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
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

##############################################################################
# Description: Test all of the functionality about About dialog of banshee
# Written by:  Felicia Mu<fxmu@novell.com>
##############################################################################

# The docstring below is used in the generated log file
"""
Step1: Launch firefox process
Step2: Launch "Banshee User Guide (Wiki)" web page
Step3: Launch "Open browser to banshee homepage" web page
Step4: Launch "get involved homepage" web page
Step5: On "About" dialog, verify that the credits show up correctly
Step6: On "About" dialog, verify that the license is showing
Step7: On "About" dialog, verify that the proper version is showing
Step8: On "About" dialog, Open Banshee Wiki:Steps                                                                                
Step9: On "About" dialog, test the close button
"""
# imports
from strongwind import *

# open the label sample application
try:
  app = launchApp("/usr/bin/banshee-1", "Banshee")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
bFrame = app.findFrame("Banshee Media Player")

# Step1: Launch firefox process
procedurelogger.action("Launch firefox process")
os.popen("firefox &")
firefoxapp = cache._desktop.findApplication('Firefox', checkShowing=False)
fFrames = firefoxapp.findAllFrames(None)
url_entry = fFrames[0].findEntry("Search Bookmarks and History")
sleep(config.SHORT_DELAY)

restorebutton = pyatspi.findDescendant(fFrames[0], lambda x:x.name == "Start New Session")
if (restorebutton):
        restorebutton.mouseClick(log = False)
        procedurelogger.expectedResult("the page of firefox is a new session")
else:
        procedurelogger.expectedResult("the page of firefox is restored to previous")
sleep(config.SHORT_DELAY)

# Step2: Launch "Banshee User Guide (Wiki)" web page
helpMenu = bFrame.findMenu("Help")
helpMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)

webMenu= helpMenu.findMenu("Web Resources")
webMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)

webMenuItem= bFrame.findMenuItem("Banshee User Guide (Wiki)")
webMenuItem.mouseClick(log=True)
sleep(config.LONG_DELAY)

procedurelogger.action("Open browser to banshee homepage")
assert (url_entry.text == "http://banshee.fm/support/guide/")
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the url is loaded correctly")

# Step3: Launch "Open browser to banshee homepage" web page
helpMenu = bFrame.findMenu("Help")
helpMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)

webMenu= bFrame.findMenu("Web Resources")
webMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)

webMenuItem= bFrame.findMenuItem("Banshee Home Page")
webMenuItem.mouseClick(log=True)
sleep(config.LONG_DELAY)
sleep(config.SHORT_DELAY)

procedurelogger.action("Open browser to banshee homepage")
assert (url_entry.text == "http://banshee.fm/")
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the url is loaded correctly")

# Step4: Launch "get involved homepage" web page
helpMenu = bFrame.findMenu("Help")
helpMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)

webMenu= bFrame.findMenu("Web Resources")
webMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)

webMenuItem= bFrame.findMenuItem("Get Involved")
webMenuItem.mouseClick(log=True)
sleep(config.LONG_DELAY)

procedurelogger.action("Open browser to get involved homepage")
assert (url_entry.text == "http://banshee.fm/contribute/")
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the url is loaded correctly")

# Step5: On "About" dialog, verify that the credits show up correctly
helpMenu = bFrame.findMenu("Help")
helpMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)

webMenu= bFrame.findMenuItem("About")
webMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)

aboutDialog = app.findDialog("About Banshee")
licenseButton = aboutDialog.findPushButton("Credits")
licenseButton.mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.action("assert the credits shows up correctly")
creditsDialog = app.findDialog("Credits")
writtenbyPageTab = creditsDialog.findPageTab("Written by")
translatedbyPageTab = creditsDialog.findPageTab("Translated by")
artworkbyPageTab = creditsDialog.findPageTab("Artwork by")

if (writtenbyPageTab and translatedbyPageTab and artworkbyPageTab ):
	procedurelogger.expectedResult("the credits shows up correctly")
else:
	procedurelogger.expectedResult("the credits shows up not correctly")

closeButton = creditsDialog.findPushButton("Close")  
closeButton.mouseClick()
sleep(config.SHORT_DELAY)
creditsDialog.assertClosed()

# Step6: On "About" dialog, verify that the license is showing
licenseButton = aboutDialog.findPushButton("License")
licenseButton.mouseClick()
sleep(config.SHORT_DELAY)
 
procedurelogger.action("assert the license shows up correctly")
licenseDialog = app.findDialog("License")
licenseText = licenseDialog.findText("")
if (licenseText):
	procedurelogger.expectedResult("the license shows up correctly")
else:
	procedurelogger.expectedResult("the license shows up not correctly")

closeButton = licenseDialog.findPushButton("Close")  
closeButton.mouseClick()
sleep(config.SHORT_DELAY)
licenseDialog.assertClosed()

# Step7: On "About" dialog, verify that the proper version is showing
procedurelogger.action("Verify the version displayed matches the version of the version of the packages")
version = os.popen("rpm -qi banshee-1 |grep Version | awk '{print $3}'").read()
version = version[0:5]

labels =aboutDialog.findAllLabels(None)
firstlabel = labels[0].name.split(' ')[-1]
versionLabel = firstlabel[1: -1]

assert (versionLabel == version)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("The version displayed matches the version of the package")

# Step8: On "About" dialog, Open Banshee Wiki:Steps                                                                                
# Click url to banshee homepage
procedurelogger.action("Open browser to banshee homepage")
aboutDialog.findPushButton("Banshee Website").click(log=False)
sleep(config.LONG_DELAY)
procedurelogger.expectedResult("the url is loaded correctly")

# Quit firefox application
procedurelogger.action("kill firefox process")
os.popen("killall firefox-bin").read()
sleep(config.SHORT_DELAY)

# Step9: On "About" dialog, test the close button
closePushButton = aboutDialog.findPushButton("Close")  
print "the button is ",closePushButton  
closePushButton.mouseClick()
sleep(config.SHORT_DELAY)
aboutDialog.assertClosed()

