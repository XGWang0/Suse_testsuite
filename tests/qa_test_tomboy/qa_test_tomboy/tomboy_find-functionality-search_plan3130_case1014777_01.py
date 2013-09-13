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
# Date:        11/29/2010
# Description: Tomboy Find Functionality In "Search All Notes" Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Find Functionality In "Search All Notes" To Search Text test===
Step1: Launch "Search All Notes"
Step2: Enable "Case Sensitive" check box
Step3: Input "welcome" into Search text that nothing to be find
Step4: Input "Welcome" into Search text that "Start Here" cell appears 
Step5: Disable "Case Sensitive" check box
Step6: Input "welcome" into Search text that "Start Here" cell appears

NOTE:
(1) "Case Sensitive" only happens in tomboy-0.12.1 version
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

# Step1: Launch "Search All Notes"
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 3)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

search_frame = app.findFrame("Search All Notes")

if app_name is "Tomboy":
    # Step2: Enable "Case Sensitive" check box
    search_frame.findCheckBox("Case Sensitive").mouseClick()
    sleep(config.SHORT_DELAY)

    # Step3: Input "welcome" into Search text that nothing to be find
    search_frame.findText(None).typeText("welcome")
    sleep(config.SHORT_DELAY)

    procedurelogger.expectedResult("Start Here doesn't appears in the table")
    try:
        search_frame.findTableCell("Start Here")
    except SearchError:
        pass # expected
    else:
        assert False, "Start Here shouldn't appears"

    # Step4: Input "Welcome" into Search text that "Start Here" cell appears 
    procedurelogger.action("Input Welcome into Search text")
    search_frame.findText(None).text = "Welcome"
    procedurelogger.expectedResult("Start Here appears in the table")
    search_frame.findTableCell("Start Here")

    # Step5: Disable "Case Sensitive" check box
    search_frame.findCheckBox("Case Sensitive").mouseClick()
    sleep(config.SHORT_DELAY)

# Step6: Input "welcome" into Search text that "Start Here" cell appears
procedurelogger.action("Input welcome into Search text")
search_frame.findText(None).text = "welcome"
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("Start Here appears in the table")
search_frame.findTableCell("Start Here")

# Close frame
menubar = search_frame.findMenuBar(None)
menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
search_frame.assertClosed()

# Quit Tomboy
quitTomboy(tomboy_panel)

