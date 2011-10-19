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
# Written by: Calen Chen <cachen@novell.com>
# Date:        10/20/2010
# Description: Firefox Adobe Flash plugin Test
##############################################################################

# imports
import sys
import os

from strongwind import *
from firefox_frame import *

class PluginError(Exception):
    "Raised when plugin doesn't exist"
    pass

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===Adobe Flash plugin test===
Step1: load to http://www.adobe.com/software/flash/about/
Step2: make sure Flash plugin installed
Step3: make sure what version is being used

NOTE: 
There are some accessibility problems:
(1) Version Information doesn't accessible, check the change of section's 
number to ensure the flash plugin works
(2) Should update to MozillaFirefox-3.5.11, otherwise Disable and Enable 
button in the test doesn't accessible
"""

# Launch browser
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# Step1: load to http://www.adobe.com/software/flash/about/
flash_web = "http://www.adobe.com/software/flash/about/"
entry = fFrame.findEntry("Search Bookmarks and History")
procedurelogger.action('Load to %s' % flash_web)
entry.text = flash_web
entry.mouseClick()
sleep(config.SHORT_DELAY)
fFrame.keyCombo("enter", grabFocus=False)
sleep(config.LONG_DELAY)

procedurelogger.expectedResult('%s frame appears' % \
                                    "Adobe - Flash Player")
assert fFrame.name.startswith("Adobe - Flash Player"), \
              "frame name shouldn't be %s" % fFrame.name  

# Step2: make sure Flash plugin installed
menubar = fFrame.findMenuBar(None)
menubar.select(['Tools', 'Add-ons'])

addon_frame = app.findFrame("Add-ons")
addon_frame.findListItem("Plugins").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('Make sure Adobe flash in plugin list')
try:
    flash_plugin = addon_frame.findListItem(re.compile('^Shockwave Flash'))
except SearchError:
    quitFirefox(fFrame)
    raise PluginError, "Adobe Flash plugin doesn't installed, Please download and install plugin first from https://addons.mozilla.org/en-US/firefox/browse/type:7"
    sys.exit(22)
else:
    # Disable Flash plugin to check Section's number
    procedurelogger.action('Select Shockwave Flash list item')
    flash_index = flash_plugin.getIndexInParent()
    addon_frame.findList(None).clearSelection()
    sleep(config.SHORT_DELAY)
    addon_frame.findList(None).selectChild(flash_index)
    sleep(config.SHORT_DELAY)

    addon_frame.findListItem(re.compile('^Shockwave Flash')).findPushButton("Disable").press(log=True)
    sleep(config.MEDIUM_DELAY)
    section_num_old = len(fFrame.findDocumentFrame("Adobe - Flash Player").findAllSections(None))

# Step3: make sure what version is being used
# Enable Flash plugin
addon_frame.findListItem(re.compile('^Shockwave Flash')).findPushButton("Enable").press(log=True)
sleep(config.SHORT_DELAY)

# reload the web
fFrame.findPushButton("Reload").press(log=True)
sleep(config.LONG_DELAY)

procedurelogger.expectedResult('Make sure Flash plugin works')
section_num_new = len(fFrame.findDocumentFrame("Adobe - Flash Player").findAllSections(None))

assert section_num_new != section_num_old

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

