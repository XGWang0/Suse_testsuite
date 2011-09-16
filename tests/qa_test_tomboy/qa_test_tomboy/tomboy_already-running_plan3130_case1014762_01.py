#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        11/17/2010
# Description: Tomboy Already Running Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Already Running test===
Step1: Load Tomboy for the first time
Step2: Load Tomboy again from the application browser
Step3: Make sure "Search All Notes" window pops up
"""
# imports
import os
from strongwind import *
from tomboy_frame import *

print doc

# Check version
app_name = checkVersion()

# Kill the exist Tomboy process
killRunning()

# Step1: Load Tomboy for the first time
(app, subproc) = cache.launchApplication('/usr/bin/tomboy', app_name, wait=config.MEDIUM_DELAY)

# Find tomboy on panel
tomboy_panel = tomboyPanel()

# Step2: Load Tomboy again
procedurelogger.action('Load Tomboy again')
os.system('tomboy&')
sleep(config.SHORT_DELAY)

# Step3: Make sure "Search All Notes" window pops up
procedurelogger.expectedResult('Make sure "Search All Notes" window pops up')
tFrame = app.findFrame("Search All Notes")

# Close application
menubar = tFrame.findMenuBar(None)
menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
tFrame.assertClosed()

# Quit Tomboy
quitTomboy(tomboy_panel)
