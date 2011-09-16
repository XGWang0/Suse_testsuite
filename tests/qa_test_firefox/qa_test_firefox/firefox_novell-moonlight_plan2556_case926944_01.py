#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        10/26/2010
# Description: Firefox Novell Moonlight Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===Novell Moonlight test===

Step1: Make sure Silverlight Plug-In appears in Plugins list
Step2: Visit the following URL
Silverlight3 http://www.belindaperez.com/demo/deepu/SimpleImageScroller.html
Silverlight3 http://www.innoveware.com/ql3/QuakeLight.html
Silverlight2 http://147.2.207.213/moonlight_apps/DiggSample/TestPage.html
Step3: Make sure websites be showed correctly. the website should not show 
"Install Microsoft Sliverlight".

NOTES:
Some different Steps with the test case926944 in Plan2556
"""

# imports
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

try:
  app = launchApp("/usr/bin/firefox", "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# Step1: Make sure Silverlight Plug-In appears in Plugins list
menubar = fFrame.findMenuBar(None)
menubar.select(['Tools', 'Add-ons'])
sleep(config.SHORT_DELAY)

addon_frame = app.findFrame("Add-ons")

addon_frame.findListItem("Plugins").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('Make sure Silverlight Plug-In exists')
addon_frame.findListItem(re.compile('^Silverlight Plug-In'), checkShowing=False)

addon_frame.altF4()

# Step2: Visit the following URL
# Launch http://www.belindaperez.com/demo/deepu/SimpleImageScroller.html
# that is Silverlight3
openURL(fFrame, "http://www.belindaperez.com/demo/deepu/SimpleImageScroller.html")

# Step3: Make sure websites be showed correctly. the website should not show 
# "Install Microsoft Sliverlight".
procedurelogger.expectedResult('%s document frame appears' % \
                                                  "SimpleImageScrollerDemo")
fFrame.findDocumentFrame("SimpleImageScrollerDemo")
try:
    fFrame.findLink("Get Microsoft Silverlight")
except SearchError:
    pass # expected
else:
    assert False, "the website should not show Install Microsoft Sliverlight"

# Add new tab to launch http://www.innoveware.com/ql3/QuakeLight.html
# that is Silverlight3
menubar.select(['File', 'New Tab'])
sleep(config.SHORT_DELAY)

openURL(fFrame, "http://www.innoveware.com/ql3/QuakeLight.html")

# Make sure websites be showed correctly. the website should not show 
# "Install Microsoft Sliverlight".
procedurelogger.expectedResult('%s document frame appears' % \
                                                  "QuakeLight")
fFrame.findDocumentFrame(re.compile('^QuakeLight'))
try:
    fFrame.findLink("Get Microsoft Silverlight")
except SearchError:
    pass # expected
else:
    assert False, "the website should not show Install Microsoft Sliverlight"

# Add new tab to Launch http://147.2.207.213/moonlight_apps/DiggSample/TestPage.html
# that is Silverlight2
menubar.select(['File', 'New Tab'])
sleep(config.SHORT_DELAY)

openURL(fFrame, "http://147.2.207.213/moonlight_apps/DiggSample/TestPage.html")

# Make sure websites be showed correctly. the website should not show 
# "Install Microsoft Sliverlight".
procedurelogger.expectedResult('%s document frame appears' % \
                                                  "DiggSearch")
fFrame.findDocumentFrame("DiggSearch")
try:
    fFrame.findLink("Get Microsoft Silverlight")
except SearchError:
    pass # expected
else:
    assert False, "the website should not show Install Microsoft Sliverlight"

# Close application
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
quitMultipleTabs(app)
fFrame.assertClosed()
