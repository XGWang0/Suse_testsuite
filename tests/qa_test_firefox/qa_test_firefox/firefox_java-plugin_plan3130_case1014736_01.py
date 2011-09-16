#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        11/15/2010
# Description: Firefox Java Plugin Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===Java Plugin test===
Step1: Add-on ->Plugins, disable Java(TM) Plug-in
Step2: Unable to load the testpage
Step3: Enable Java(TM) Plug-in
Step4: Load the testpage successful
"""

# imports
import os
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# Launch browser
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

source_path = '/usr/share/qa/qa_test_firefox/test_source/'
mhtml_page = 'example1.html'

# Step1: Add-on ->Plugins, disable Java(TM) Plug-in
menubar = fFrame.findMenuBar(None)
menubar.select(['Tools', 'Add-ons'])

addon_frame = app.findFrame("Add-ons")
addon_frame.findListItem("Plugins").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('Make sure Jave Plugin in the list')
try:
    java_plugin = addon_frame.findListItem(re.compile('^IcedTea Java Web Browser Plugin'))
except SearchError:
    try:
        java_plugin = addon_frame.findListItem(re.compile('^Java(IM) Plug-in'))
    except SearchError:
        menubar.select(['File', 'Quit'])
        raise Exception, "Java plugin doesn't installed"
        exit(22)
else:
    # Select Java plugin item to make 'Disable' button appear
    java_plugin._accessible.queryAction().doAction(0)
    sleep(config.SHORT_DELAY)
    # Reopen addon frame due to Disable button doesn't accessible sometimes
    menubar.select(['Tools', 'Add-ons'])
    java_plugin.mouseClick(log=False)
    java_plugin.findPushButton("Disable").mouseClick()
    sleep(config.SHORT_DELAY)

# Step2: Unable to load the testpage
fFrame.findEntry("Search using Google").mouseClick()
sleep(config.SHORT_DELAY)
openURL(fFrame, source_path + mhtml_page)

procedurelogger.expectedResult("the Text widget in example page appears")
example_doc = fFrame.findDocumentFrame("The Animator Applet (1.1) - example 1")
try:
    example_doc.findText(None)
except SearchError:
    pass # expected
else:
    assert False, "Text shouldn't appears when Java plugin disabled"

# Step3: Enable Java(TM) Plug-in
menubar.select(['Tools', 'Add-ons'])
java_plugin.findPushButton("Enable").mouseClick()
sleep(config.SHORT_DELAY)

addon_frame.altF4()

# Step4: Load the testpage successful
openURL(fFrame, source_path + mhtml_page)

procedurelogger.expectedResult("the Text widget in example page appears")
example_doc = fFrame.findDocumentFrame("The Animator Applet (1.1) - example 1")
example_doc.findText(None)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()
