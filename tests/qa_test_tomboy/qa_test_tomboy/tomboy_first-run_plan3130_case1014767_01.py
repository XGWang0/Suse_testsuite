#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        11/19/2010
# Description: Tomboy First Run Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===First Run test===
Step1: Remove ~/.tomboy if that is exist
Step2: Load Tomboy for the first time
Step3: Mouse right button click tomboy on panel to raise context menu
Step4: Move to Create New Note to invoke
Step5: Make sure "New Note 3" is created, then delete this note
Step6: Move to Start Here to invoke
Step7: Make sure "Start Here" is opened
Step8: Move to Using Links in Tomboy to invoke
Step9: Make sure "Using Links in Tomboy" is opened

NOTE:
Some problems in accessibility:
(1) context menu of Tomboy on notification area doesn't accessible
"""
# imports
import os
from strongwind import *
from tomboy_frame import *

print doc

# Step1: Remove ~/.tomboy if that is exist
who = os.popen('whoami').read().replace('\n', '')
if os.path.exists('/%s/.tomboy' % who):
    os.system('rm -fr /%s/.tomboy' % who)

# Check version
app_name = checkVersion()

# Kill the exist Tomboy process
killRunning()

# Step2: Load Tomboy for the first time
#procedurelogger.action('Load Tomboy again')
#os.system('tomboy&')
(app, subproc) = cache.launchApplication('/usr/bin/tomboy', app_name, wait=config.MEDIUM_DELAY)

# Step3: Mouse right button click tomboy on panel to raise context menu
tomboy_panel = tomboyPanel()
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)

# Step4: Move to Create New Note to invoke
tomboy_panel.keyCombo("Up", grabFocus=False)
sleep(config.SHORT_DELAY)
tomboy_panel.keyCombo("enter", grabFocus=False)
sleep(config.SHORT_DELAY)

# Step5: Make sure "New Note 3" is created, then delete this note

new_note = app.findFrame("New Note 3")
new_note.findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)
app.findDialog(None).findPushButton("Delete").mouseClick()
new_note.assertClosed()

# Step6: Move to Start Here to invoke
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)

keyPress(tomboy_panel, "Up", 4)
tomboy_panel.keyCombo("enter", grabFocus=False)
sleep(config.SHORT_DELAY)

# Step7: Make sure "Start Here" is opened
start_hear = app.findFrame(re.compile('^Start Here'))

start_hear.altF4()

# Step8: Move to Using Links in Tomboy to invoke
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)

keyPress(tomboy_panel, "Up", 5)
tomboy_panel.keyCombo("enter", grabFocus=False)
sleep(config.SHORT_DELAY)

# Step9: Make sure "Using Links in Tomboy" is opened
start_hear = app.findFrame(re.compile('^Using Links in Tomboy'))

start_hear.altF4()

# Quit Tomboy
quitTomboy(tomboy_panel)
