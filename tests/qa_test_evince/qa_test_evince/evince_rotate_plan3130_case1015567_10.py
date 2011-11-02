#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE. All Rights Reserved.
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
# Date:        09/29/2010
# Description: Evince test for "Rotate" MenuItem
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Evince Menu Functions test==
==="Rotate" MenuItem test===
Step1: Open a pdf
Step2: From <Edit> menu select <Rotate Left> menu item
Step3: Make sure document is rotated by checking the value of scrollbar
Step4: Make sure number(width, height) of icon size under Thumbnails is changed to (height, width)
Step5: From <Edit> menu select <Rotate Right> menu item
Step6: Make sure document is rotated by checking the value of scrollbar
Step7: Make sure number of icon size under Thumbnails is roll back to (width, height)
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

# variable icon's size before rotated
icon_1 = eFrame.findIcon(None, checkShowing=False)

old_size = icon_1._accessible.queryImage().getImageSize()
old_size_width = old_size[0]
old_size_height = old_size[1]

# variable maximum value of horizontal scrollbar in document view
scrollbars = eFrame.findAllScrollBars(None)
if len(scrollbars) > 2:
    doc_hscrollbar = scrollbars[1]
else:
    doc_hscrollbar = scrollbars[0]

old_value_hscrollbar = doc_hscrollbar._accessible.queryValue().maximumValue

# Step2: From <Edit> menu select <Rotate Left> menu item
menubar.select(['Edit', 'Rotate Left'])
sleep(config.SHORT_DELAY)

# Step3: Make sure document is rotated by checking the value of scrollbar
procedurelogger.expectedResult("maximum value of hscrollbar is larger than the old %s" % \
                                                                old_value_hscrollbar)
new_value_hscrollbar = doc_hscrollbar._accessible.queryValue().maximumValue

assert new_value_hscrollbar > old_value_hscrollbar, \
                                 "new value %s shouldn't small than old value" % \
                                                     (new_value_hscrollbar)

# Step4: Make sure number(width, height) of icon size under Thumbnails is changed to (height, width)
procedurelogger.expectedResult("icon size under Thumbnails is changed to (%s, %s)" % \
                                                 (old_size_height, old_size_width))
icon_1 = eFrame.findIcon(None, checkShowing=False)
new_size = icon_1._accessible.queryImage().getImageSize()

assert new_size == (old_size_height, old_size_width), \
                                         "icon size shouldn't be %s" % str(old_size)

# Step5: From <Edit> menu select <Rotate Right> menu item
menubar.select(['Edit', 'Rotate Right'])
sleep(config.SHORT_DELAY)

# Step6: Make sure document is rotated by checking the value of scrollbar
procedurelogger.expectedResult("maximum value of hscrollbar is turn to the old %s" % \
                                                                old_value_hscrollbar)
new_value_hscrollbar = doc_hscrollbar._accessible.queryValue().maximumValue

assert new_value_hscrollbar == old_value_hscrollbar, \
                                 "new value expected: %s, actual: %s" %\
                                    (old_value_hscrollbar, new_value_hscrollbar)

# Step7: Make sure number of icon size under Thumbnails is roll back to (width, height)
procedurelogger.expectedResult("icon size under Thumbnails is turn to %s" % \
                                                                       str(old_size))
icon_1 = eFrame.findIcon(None, checkShowing=False)
new_size = icon_1._accessible.queryImage().getImageSize()

assert new_size == old_size, "new size expected: %s, actual: %s" % (old_size, new_size)

# Step9: Close the application
menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
eFrame.assertClosed()

