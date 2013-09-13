#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
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
# Written by:  Calen Chen <cachen@novell.com>
# Date:        09/30/2010
# Description: Evince test for "Zoom In" and "Zoom Out" MenuItem
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Evince Menu Functions test==
==="Zoom" MenuItem test===
Step1: Open a pdf
Step2: Return the original zoom level to 100% in toolbar combobox
Step3: From <View> menu select <Zoom In> menu item 2 times
Step4: Make sure zoom level combobox's name is updated from 100% to 150%
Step5: Make sure document view is zoom in by checking the value of scrollbar
Step6: From <View> menu select <Zoom Out> menu item 2 times
Step7: Make sure zoom level combobox's name is updated from 150% to 100%
Step8: Make sure document view is zoom in by checking the value of scrollbar
"""

# imports
from os import system
from strongwind import *
from evince_frame import *

# open the label sample application
try:
  app = launchApp("/usr/bin/evince", "evince")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter

eFrame = app.evinceFrame

print doc

# Step1: Open an exited pdf
menubar = eFrame.findMenuBar(None)
try:
    menubar.select(['File', '1.  rtstat.pdf'])
except SearchError:
    openFile(eFrame, app)
sleep(config.SHORT_DELAY)

# variable maximum value of horizontal scrollbar in document view
scrollbars = eFrame.findAllScrollBars(None)
if len(scrollbars) > 2:
    doc_hscrollbar = scrollbars[1]
else:
    doc_hscrollbar = scrollbars[0]

# Step2: Return the original zoom level to 100% in toolbar combobox
zoom_combobox = eFrame.findComboBox(None)
zoom_combobox.findMenuItem("100%", checkShowing=False).click()
sleep(config.SHORT_DELAY)

old_value_hscrollbar = doc_hscrollbar._accessible.queryValue().maximumValue

# Step3: From <View> menu select <Zoom In> menu item
menubar.select(['View', 'Zoom In'])
sleep(config.SHORT_DELAY)

# Step4: Make sure zoom level combobox's name is updated from 100% to 125%
procedurelogger.expectedResult("zoom combobox's name should update to %s" % "125%")
assert zoom_combobox.name == "125%", "zoom combobox's name expected: %s, actual: %s" % \
                                              ("125%", zoom_combobox.name)

# Step5: From <View> menu select <Zoom In> menu item again
menubar.select(['View', 'Zoom In'])
sleep(config.SHORT_DELAY)

# Step6: Make sure zoom level combobox's name is updated from 125% to 150%
procedurelogger.expectedResult("zoom combobox's name should update to %s" % "150%")
assert zoom_combobox.name == "150%", "zoom combobox's name expected: %s, actual: %s" % \
                                              ("150%", zoom_combobox.name)

# Step7: Make sure document view is zoom in by checking the value of scrollbar
procedurelogger.expectedResult("maximum value of hscrollbar is larger than the old %s" % \
                                                                old_value_hscrollbar)
new_value_hscrollbar = doc_hscrollbar._accessible.queryValue().maximumValue

assert new_value_hscrollbar > old_value_hscrollbar, \
                               "new value %s shouldn't small than old value %s" % \
                                       (new_value_hscrollbar, old_value_hscrollbar)

# Step8: From <View> menu select <Zoom Out> menu item
menubar.select(['View', 'Zoom Out'])
sleep(config.SHORT_DELAY)

# Step9: Make sure zoom level combobox's name is updated from 150% to 125%
procedurelogger.expectedResult("zoom combobox's name should update to %s" % "125%")
assert zoom_combobox.name == "125%", "zoom combobox's name expected: %s, actual: %s" % \
                                              ("125%", zoom_combobox.name)

# Step10: From <View> menu select <Zoom Out> menu item again
menubar.select(['View', 'Zoom Out'])
sleep(config.SHORT_DELAY)

# Step11: Make sure zoom level combobox's name is updated from 125% to 100%
procedurelogger.expectedResult("zoom combobox's name should update to %s" % "100%")
assert zoom_combobox.name == "100%", "zoom combobox's name expected: %s, actual: %s" % \
                                              ("100%", zoom_combobox.name)

# Step12: Make sure document is zoom in by checking the value of scrollbar
procedurelogger.expectedResult("maximum value of hscrollbar is turn to the old %s" % \
                                                                old_value_hscrollbar)
new_value_hscrollbar = doc_hscrollbar._accessible.queryValue().maximumValue

assert new_value_hscrollbar == old_value_hscrollbar, \
                                 "new value expected: %s, actual: %s" %\
                                    (old_value_hscrollbar, new_value_hscrollbar)

# Step13: Close the application
menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
eFrame.assertClosed()

