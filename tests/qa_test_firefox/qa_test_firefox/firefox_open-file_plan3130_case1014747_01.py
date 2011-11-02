#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Date:        11/16/2010
# Description: Firefox Open File Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===Open File test===
Step1: From File | Open File... to load a local .html file
Step2: Make sure local html file is loaded
Step3: From File | Open File... to load .wav format file
Step4: Make sure wav file is opened
Step5: Load .rpm format file
Step6: Select "Save File"
Step7: Make sure rpm is saving
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

test_source = '/usr/share/qa/qa_test_firefox/test_source/'
html_url = 'example1.html'
wav_url = '/usr/share/sounds/question.wav'
rpm_name = 'CASA-cli-1.7.1592-2.3.53.i586.rpm'

# Step1: From File | Open File... to load a local .html file
menubar = fFrame.findMenuBar(None)
menubar.findMenu("File").mouseClick()
sleep(config.SHORT_DELAY)
menubar.findMenuItem(re.compile('^Open File')).click(log=True)
sleep(config.SHORT_DELAY)

open_dialog = app.findDialog("Open File")
file_toggle = open_dialog.findToggleButton("Type a file name")

if not file_toggle.checked:
    file_toggle.mouseClick()
    sleep(config.SHORT_DELAY)

open_dialog.findText(None, labelledBy="Location:").text = test_source + html_url
open_dialog.findPushButton("Open").mouseClick()
sleep(config.SHORT_DELAY)
open_dialog.assertClosed()

# Step2: Make sure local html file is loaded
procedurelogger.expectedResult("make sure %s is opened" % html_url)
fFrame.findDocumentFrame("The Animator Applet (1.1) - example 1")

# Step3: From File | Open File... to load .wav format file
menubar.findMenu("File").mouseClick()
sleep(config.SHORT_DELAY)
menubar.findMenuItem(re.compile('^Open File')).click(log=True)
sleep(config.SHORT_DELAY)

open_dialog = app.findDialog("Open File")
file_toggle = open_dialog.findToggleButton("Type a file name")

open_dialog.findText(None, labelledBy="Location:").text = wav_url
open_dialog.findPushButton("Open").mouseClick()
sleep(config.SHORT_DELAY)
open_dialog.assertClosed()

# Step4: Make sure wav file is opened
procedurelogger.expectedResult("make sure %s is opened" % wav_url)
fFrame.findDocumentFrame(re.compile('^question.wav'))

# Step5: Load .rpm format file
rpm_url = test_source + rpm_name

menubar.findMenu("File").mouseClick()
sleep(config.SHORT_DELAY)
menubar.findMenuItem(re.compile('^Open File')).click(log=True)
sleep(config.SHORT_DELAY)

open_dialog = app.findDialog("Open File")
file_toggle = open_dialog.findToggleButton("Type a file name")

open_dialog.findText(None, labelledBy="Location:").text = rpm_url
open_dialog.findPushButton("Open").mouseClick()
sleep(config.SHORT_DELAY)
open_dialog.assertClosed()

# Step6: Select "Save File"
save_dialog = app.findDialog(re.compile('^Opening'))

save_dialog.findRadioButton("Save File").mouseClick()
sleep(config.SHORT_DELAY)
save_dialog.findPushButton("OK").mouseClick()
save_dialog.assertClosed()

# Step7: Make sure rpm is saving
app.findFrame(re.compile('Downloads$'))

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

