#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        10/25/2010
# Description: Firefox Customize View Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===Customize View test===
Step1: Click on View -> Toolbars -> Customize
Step2: Change a component of choice by drag tool to ToolBar
Step3: Vary the component choice between tests
Step4: Save the Customized view
Step5: Restart firefox, and check toolbar
"""
# imports
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# Launch Firefox.
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# Step1: Click on View -> Toolbars -> Customize
tool_toolbar = fFrame.findAllToolBars(None)[1]

fFrame.findMenuItem(re.compile('^Customize'), checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)
customize_frame = app.findFrame("Customize Toolbar")

# Step2: Change a component of choice by drap tool to ToolBar
# Drag History tool to ToolBar
history_tool = customize_frame.findPushButton("History")
drag(history_tool, tool_toolbar)

# Step3: Vary the component choice between tests by make sure "History" 
# push button appears in toolbar
procedurelogger.expectedResult("%s appears in toolbar" % "History")
tool_toolbar.findPushButton("History")

# Step4: Save the Customized view
customize_frame.findPushButton("Done").mouseClick()
sleep(config.SHORT_DELAY)

quitFirefox(fFrame)

# Step5: Restart firefox
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)

fFrame = app.firefoxFrame

# Check ToolBar again, make sure "History" push button appears in toolbar
procedurelogger.expectedResult("%s appears in toolbar" % "History")
fFrame.findAllToolBars(None)[1].findPushButton("History")

# Restore ToolBar to default
fFrame.findMenuItem(re.compile('^Customize'), checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)
customize_frame = app.findFrame("Customize Toolbar")
customize_frame.findPushButton("Restore Default Set").press(log=True)
sleep(config.SHORT_DELAY)

# Make sure "History" push button disappears in toolbar
procedurelogger.expectedResult("%s disappears in toolbar" % "History")
try:
    fFrame.findAllToolBars(None)[1].findPushButton("History")
    sleep(config.SHORT_DELAY)
except SearchError:
    assert True, "History tool button shouldn't appears in tool bar"

customize_frame.findPushButton("Done").press(log=True)
sleep(config.SHORT_DELAY)
customize_frame.assertClosed()

# Close application
fFrame.altF4()
sleep(config.SHORT_DELAY)
app.assertClosed()
