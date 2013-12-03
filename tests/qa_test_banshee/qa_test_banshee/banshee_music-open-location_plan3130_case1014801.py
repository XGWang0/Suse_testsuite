#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE, Inc. All Rights Reserved.
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
# Description: Test the Open Location dialogue, try all of the supported 
#              file types.
# Written by:  Felicia Mu<fxmu@novell.com>
##############################################################################

# The docstring below is used in the generated log file
"""
Step1: opens the dialogue
Step2: Open a http location:http://vietnamese.cri.cn/mmsource/audio/2009/02/11/tiankongM.mp3
Step3: Open mp3 from ftp server
Step4: Open mp3 from smb server
Step5: Verify the browse button
Step6: Verify the Cancel button
"""
# imports
from strongwind import *
from banshee_config import *

ftp_mp3 = ftp_mp3_source
smb_mp3 = smb_mp3_source

# open the label sample application
try:
  app = launchApp("/usr/bin/banshee-1", "Banshee")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
bFrame = app.findFrame("Banshee Media Player")


# Step1: Open the dialogue
helpMenu = bFrame.findMenu("Media")
helpMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"Media\"'s submenu is shown")

# Step2: Open a http location:http://vietnamese.cri.cn/mmsource/audio/2009/02/11/tiankongM.mp3
webMenu= helpMenu.findMenuItem("Open Location...")
webMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)
locationDialog = app.findDialog("Open Location")

# Input the address in the text
procedurelogger.action("input the \"http://vietnamese.cri.cn/mmsource/audio/2009/02/11/tiankongM.mp3\" in the text")
text = locationDialog.findText("")
text.text = "http://vietnamese.cri.cn/mmsource/audio/2009/02/11/tiankongM.mp3" 
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"http://vietnamese.cri.cn/mmsource/audio/2009/02/11/tiankongM.mp3\" is in the text")

# Click the "Open" button
openButton = locationDialog.findPushButton("Open")
openButton.mouseClick()
sleep(config.LONG_DELAY)
procedurelogger.expectedResult("the song is loaded in the banshee")

# Test if the slider's change
procedurelogger.action("open the http location in banshee")
slider = bFrame.findSlider("")
sliderFirst = slider._accessible.queryValue().currentValue
sleep(config.LONG_DELAY)

sliderSecond = slider._accessible.queryValue().currentValue
assert (sliderFirst != sliderSecond)
procedurelogger.expectedResult("the http location is opened by banshee")

# Step3: Open mp3 from ftp server
# Launch firefox process

procedurelogger.action("Launch firefox process")
os.popen("firefox &")
firefoxapp = cache._desktop.findApplication('Firefox', checkShowing=False)
fFrames = firefoxapp.findAllFrames(None)
url_entry = fFrames[0].findEntry("Search Bookmarks and History")
sleep(config.SHORT_DELAY)

newSessionButton = pyatspi.findDescendant(fFrames[0], lambda x:x.name == "Start New Session")
#restoreButton = pyatspi.findDescendant(fFrames[0], lambda x:x.name == "Restore" and x.role == pyatspi.ROLE_PUSH_BUTTON)
if (newSessionButton):
        newSessionButton.mouseClick(log = False)
	sleep(config.SHORT_DELAY)
        procedurelogger.expectedResult("the page of firefox is a new session")
elif (restoreButton):
	sleep(config.SHORT_DELAY)
        procedurelogger.expectedResult("the page of firefox is restored to previous")

# focus to URL location
fFrames[0].findMenuItem(re.compile('^Open Location'), checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

# Input the url in firefox's entry
procedurelogger.action("Open browser to a ftp %s" % ftp_mp3)
url_entry.mouseClick(log = False)
url_entry.text = ftp_mp3
sleep(config.SHORT_DELAY)
assert (url_entry.text == ftp_mp3)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the url is loaded correctly")

# Click "Enter" button
url_entry.keyCombo("enter")
sleep(config.LONG_DELAY)
procedurelogger.expectedResult("the url is activated")

# On the new launched dialog, click "OK" button
newDialog = firefoxapp.findDialog(re.compile('^Opening'))
okButton = newDialog.findPushButton("OK")
okButton.mouseClick()
sleep(config.SHORT_DELAY)
newDialog.assertClosed()

# Test if the ftp location can be played in banshee
procedurelogger.action("play the ftp location in banshee")
sliderFirst = slider._accessible.queryValue().currentValue
sleep(config.LONG_DELAY)

sliderSecond = slider._accessible.queryValue().currentValue
assert (sliderFirst != sliderSecond)
procedurelogger.expectedResult("the ftp location is opened by banshee")

# Quit firefox application
procedurelogger.action("kill firefox process")
os.popen("killall firefox-bin").read()
sleep(config.SHORT_DELAY)

# Step4: Open mp3 from smb server
helpMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"Media\"'s submenu is shown")

webMenu.mouseClick()
sleep(config.SHORT_DELAY)
locationDialog = app.findDialog("Open Location")

# Input the address in the text
procedurelogger.action("input the %s in the text" % smb_mp3)
text = locationDialog.findText("")
text.text = smb_mp3
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the %s is in the text" % smb_mp3)

# Click the "Open" button
openButton = locationDialog.findPushButton("Open")
openButton.mouseClick()
sleep(config.LONG_DELAY)
procedurelogger.expectedResult("the song is loaded in the banshee")

# Step5: Verify the browse button
helpMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"Media\"'s submenu is shown")

webMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)
locationDialog = app.findDialog("Open Location")

# Click the "browse" button
browseButton = locationDialog.findPushButton("Browse...")
browseButton.mouseClick()
sleep(config.LONG_DELAY)
procedurelogger.expectedResult("the song is loaded in the banshee")

# assert the button can launch the "Open Location" dialog
procedurelogger.action("assert the button can launch the \"Open Location\" dialog")
openDialogs = app.findAllDialogs("Open Location")
sleep(config.SHORT_DELAY)
assert(openDialogs[1])

# close the new launched dialog
cancelButton = openDialogs[1].findPushButton("Cancel")
cancelButton.mouseClick()
sleep(config.LONG_DELAY)
openDialogs[1].assertClosed()

# Step6: Verify the Cancel button
cancel = locationDialog.findPushButton("Cancel")
cancel.mouseClick()
sleep(config.LONG_DELAY)
locationDialog.assertClosed()

