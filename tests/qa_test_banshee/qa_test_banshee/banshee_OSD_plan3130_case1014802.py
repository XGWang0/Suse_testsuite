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
# Description: Test The tray icon of banshee. 
# Written by:  Felicia Mu<fxmu@novell.com>
##############################################################################

# The docstring below is used in the generated log file
"""
Step1: To play a song of Library (verify the "Stop When Finished " item is not selected).
Step2: Minimize the  Banshee window.
Step3: When Banshee switch to the next  song,check the tray icon.
"""

# imports
from strongwind import *
from banshee_frame import *

# open the label sample application
try:
  app = launchApp("/usr/bin/banshee-1", "Banshee")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
bFrame = app.findFrame("Banshee Media Player")

# Step1: Open a song in http location
helpMenu = bFrame.findMenu("Media")
helpMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"Media\"'s submenu is shown")

# Open a http location
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

# Step2: Minimize the  Banshee window.
bFrame.keyCombo('<Alt>F4')
sleep(config.SHORT_DELAY)
bFrame.assertClosed()

# Step3: When Banshee switch to the next  song,check the tray icon.
gnomepanel = cache._desktop.findApplication('gnome-panel', checkShowing=False)
noticepanel = pyatspi.findDescendant(gnomepanel, lambda x:x.name == "Panel Notification Area")
filler = noticepanel.findFiller('')
panels = filler.findAllPanels('')

# right click the nm-applet icon
for i in range(len(panels)):
        if (panels[i]._accessible.queryComponent().getSize()[0] == panels[i]._accessible.queryComponent().getSize()[1]):
                break
absoluteMotion(1189, 672)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("The tray icon will show an unobtrusive popup,it shows some information which should match the actual playing track.")





