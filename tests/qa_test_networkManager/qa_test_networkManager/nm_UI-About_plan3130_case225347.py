#!/usr/bin/env python

##############################################################################
# Written by:  Felicia Mu<fxmu@novell.com>
#              Calen Chen<cachen@novell.com>
# Date:        03/25/2011
# Description: UI About Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===UI About===
Step1: Right click on the NetworkManager icon and select "About" item to launch dialog
Step2: Verify the version displayed matches the version of the packages
Step3: Click "NetworkManager Website" url launch firefox to the page
"""
# imports
from nm_frame import *

print doc

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Step1: Right click on the NetworkManager icon and select "About" item
nm_panel = nmPanel()

nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem("About").click(log=True)
sleep(config.SHORT_DELAY)

# find the new launced dialog
nmapplet = cache._desktop.findApplication('nm-applet', checkShowing=False)
aDialog = nm_applet_app.findDialog("About NetworkManager Applet")

# Step2: Verify the version displayed matches the version of the packages
procedurelogger.action("Verify the version displayed matches the version of the version of the packages")
version = os.popen("rpm -qi NetworkManager |grep Version | awk '{print $3}'").read() 
version = version[0:5]

labels = aDialog.findAllLabels(None)
firstlabel = labels[0].name.split(' ')[-1]

procedurelogger.expectedResult("The version displayed matches the version of the package")
assert firstlabel == version, "expected: %s, actual is: %s" % (version, firstlabel)

# Click url to network manager homepage
aDialog.findLabel("NetworkManager Website").mouseClick()
sleep(config.LONG_DELAY)

procedurelogger.expectedResult("the url is loaded correctly")
firefox_app = cache._desktop.findApplication('Firefox', checkShowing=False)
firefox_app.findFrame(re.compile('^NetworkManager'))

# Quit firefox application
firefox_app.findMenuItem("Quit", checkShowing=False).click(log=False)
sleep(config.SHORT_DELAY)
firefox_app.assertClosed()

# Click "Close" button to close dialog
aDialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
aDialog.assertClosed()
