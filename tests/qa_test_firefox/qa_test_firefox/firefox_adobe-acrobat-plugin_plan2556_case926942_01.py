#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        10/19/2010
# Description: Firefox Adobe Acrobat Reader plugin Test
##############################################################################

# imports
import sys

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
===Adobe Acrobat Reader plugin test===
Step1: make sure Adobe Acrobat Reader plugin installed
Step2: load to http://gsmworld.com/documents/a5_3_and_gea3_specifications.pdf
Step3: view this pdf file in firefox rather than a dialog pops up for download
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

# Step1: make sure Adobe Acrobat Reader plugin installed
menubar = fFrame.findMenuBar(None)
menubar.select(['Tools', 'Add-ons'])

addon_frame = app.findFrame("Add-ons")
addon_frame.findListItem("Plugins").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('Make sure Adobe Acrobat Reader in plugin list')
try:
    addon_frame.findListItem(re.compile('^Adobe Reader'))
except SearchError:
    quitFirefox(fFrame)
    pdf_web = "https://addons.mozilla.org/en-US/firefox/browse/type:7"
    raise PluginError, "Adobe Acrobat Reader plugin doesn't installed, Please download and install plugin first from https://addons.mozilla.org/en-US/firefox/browse/type:7"
    sys.exit(22)
else:
    addon_frame.altF4()
    sleep(config.SHORT_DELAY)

# Step2: load to http://gsmworld.com/documents/a5_3_and_gea3_specifications.pdf
pdf_web = "http://gsmworld.com/documents/a5_3_and_gea3_specifications.pdf"
entry = fFrame.findEntry("Search Bookmarks and History")
procedurelogger.action('Load to %s' % pdf_web)
entry.text = pdf_web
entry.mouseClick()
sleep(config.SHORT_DELAY)
fFrame.keyCombo("enter", grabFocus=False)
sleep(config.LONG_DELAY)

try:
    acroread_app = cache._desktop.findApplication('acroread', checkShowing=False)
except SearchError:
    pass
else:
    try:
        acroread_lic = acroread_app.findFrame("Adobe Reader - License Agreement")
    except SearchError:
        pass
    else:
        acroread_lic.findPushButton("Accept").mouseClick()
        sleep(config.MEDIUM_DELAY)

# Step3: view this pdf file in firefox rather than a dialog pops up 
# which prompt you to download this pdf 
procedurelogger.expectedResult('%s frame appears' % \
                                    "a5_3_and_gea3_specifications.pdf")
assert fFrame.name.startswith("a5_3_and_gea3_specifications.pdf"), \
              "frame name shouldn't be %s" % fFrame.name  

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()
