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
# Written by: Calen Chen <cachen@novell.com>
# Date:        12/20/2010
# Description: Tomboy Hotkeys Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Hotkeys test===
Step1: Right click tomboy icon on panel, select Preferences -> Hotkeys
Step2: Set <Alt>s for "Show notes menu"
Step3: Set <Alt>o for "Open Start Here"
Step4: Set <Ctrl>c for "create new note"
Step5: Set <Ctrl>o for "Open Search All Notes"
Step6: Close the preferences dialog
Step7: Restart Tomboy
Step8: Perform <Alt>s to show notes menu on panel
Step9: Perform <Alt>o to open Start Here note
Step10: Perform <Ctrl>c to create a new note
Step11: Perform <Ctrl>o to open Search All Notes frame
Step12: clean up environment by reset hotkeys to default value
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

# Load Tomboy for the first time
(app, subproc) = cache.launchApplication('/usr/bin/tomboy', app_name, wait=config.MEDIUM_DELAY)

# Find tomboy on panel
tomboy_panel = tomboyPanel()

# Step1: Right click tomboy icon on panel, select Preferences -> Hotkeys
tomboy_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 4)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

pref_dialog = app.findDialog("Tomboy Preferences")

pref_dialog.findPageTab("Hotkeys").mouseClick()
sleep(config.SHORT_DELAY)

# Step2: Set <Alt>s for "Show notes menu"
show_menu_text = pref_dialog.findText(None, labelledBy="Show notes menu")

show_menu_text.enterText("<Alt>s")
sleep(config.SHORT_DELAY)

# Step3: Set <Alt>o for "Open Start Here"
open_start_text = pref_dialog.findText(None, labelledBy="Open \"Start Here\"")

open_start_text.enterText("<Alt>o")
sleep(config.SHORT_DELAY)

# Step4: Set <Ctrl>c for "create new note"
create_new_text = pref_dialog.findText(None, labelledBy="Create new note")

create_new_text.enterText("<Ctrl>c")
sleep(config.SHORT_DELAY)

# Step5: Set <Ctrl>o for "Open Search All Notes"
open_search_text = pref_dialog.findText(None, labelledBy="Open \"Search All Notes\"")

open_search_text.enterText("<Ctrl>o")
sleep(config.SHORT_DELAY)

# Step6: Close the preferences dialog
pref_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
pref_dialog.assertClosed()

# Step7: Restart Tomboy
quitTomboy(tomboy_panel)

(app, subproc) = cache.launchApplication('/usr/bin/tomboy', app_name, wait=config.MEDIUM_DELAY)

# Find tomboy on panel
tomboy_panel = tomboyPanel()

# Step8: Perform <Alt>s to show notes menu on panel
tomboy_panel.keyCombo('<Alt>s', grabFocus=False)

try:
    app.findWindow(None)
except:
    raise SearchError, "Hotkey <Alt>s doesn't show notes menu"
else:
    tomboy_panel.mouseClick()
    sleep(config.SHORT_DELAY)

# Step9: Perform <Alt>o to open Start Here note
tomboy_panel.keyCombo('<Alt>o', grabFocus=False)

try:
    start_frame = app.findFrame("Start Here")
except:
    raise SearchError, "Hotkey <Alt>o doesn't open Start Here note"
else:
    start_frame.altF4()

# Step10: Perform <Ctrl>c to create a new note
tomboy_panel.keyCombo('<Ctrl>c', grabFocus=False)

try:
    new_frame = app.findFrame(re.compile('^New Note'))
except:
    raise SearchError, "Hotkey <Ctrl>c doesn't create new note"
else:
    new_frame.findText(None).grabFocus()
    sleep(config.SHORT_DELAY)
    deleteNote(app, new_frame)

# Step11: Perform <Ctrl>o to open Search All Notes frame
tomboy_panel.keyCombo('<Ctrl>o', grabFocus=False)

try:
    search_frame = app.findFrame("Search All Notes")
except:
    raise SearchError, "Hotkey <Ctrl>o doesn't open Search All Notes"
else:
    search_frame.altF4()

# Step12: clean up environment
tomboy_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 4)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

pref_dialog = app.findDialog("Tomboy Preferences")
hotkey_tab = pref_dialog.findPageTab("Hotkeys")

hotkey_tab.mouseClick()
sleep(config.SHORT_DELAY)

# Reset hotkeys to default value
labelledbys = ["Show notes menu", "Open \"Start Here\"", "Create new note", "Open \"Search All Notes\""]
texts = [pref_dialog.findText(None, labelledBy=x) for x in labelledbys ]

texts[0].enterText("<Alt>F12")
texts[1].enterText("<Alt>F11")
texts[2].enterText("disable")
texts[3].enterText("disable")

pref_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
pref_dialog.assertClosed()

# Quit Tomboy
quitTomboy(tomboy_panel)

