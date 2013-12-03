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
# Written by: Calen Chen <cachen@novell.com>
# Date:        05/31/2011
# Description: Gnome Session Test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Gnome Session===
Step1: Launch "gnome-session-properties" 
Step2: In tab "Startup Program", add an application (e,g. banshee) to Startup program list, and remove an application (e.g. gnome-do) from Startup program list.
Step3: In tab"Options", check box "Automatically remember running applications when logging out"
Step4: Launch "gnome-session-properties" again and check setting.

NOTES: Couldn't check logout|login
"""

# imports
from strongwind import *
from gnome_frame import *
import os

print doc

def assertFind(item_name, item_role, available=True):
    '''
    Make sure the expected item can be found
    '''
    procedurelogger.expectedResult("Find %s %s is %s" % (item_role, item_name, available))

    function = getattr(sDialog, "find" + item_role)
    if available:
        function(item_name)
    else:
        try:
            function(item_name)
        except SearchError:
            pass
        else:
            raise Exception, "%s shouldn't exist" % item_name        

# Step1: Launch "gnome-session-properties" 
try:
    app = launchApp("/usr/bin/gnome-session-properties", "gnome-session-properties", window='Dialog')
except IOError, msg:
    print "ERROR:  %s" % msg
    exit(2)

# just an alias to make things shorter
sDialog = app.gnomeSessionPropertiesDialog

# Step2: In tab "Startup Program"
sDialog.findPushButton("Add").mouseClick()
sleep(config.SHORT_DELAY)

add_dialog = app.findDialog("Add Startup Program")

# Add an application (e,g. banshee) to Startup program list
text_dict = {'Name:':'Banshee', 'Command:':'banshee-1', 'Comment:':'add banshee to startup'} 
text_list = add_dialog.findAllTexts(None)
for i in text_list:
    #if i.get
    if utils.labelledBy(i, "Name:"):
        i.enterText(text_dict['Name:'])
    if utils.labelledBy(i, "Command:"):
        i.enterText(text_dict['Command:'])
    if len(i.getRelationSet()) == 0:
        i.enterText(text_dict['Comment:'])
sleep(config.SHORT_DELAY)

add_dialog.findPushButton("Add").mouseClick()
sleep(config.SHORT_DELAY)

assertFind("Banshee\nadd banshee to startup", "TableCell")

# Remove an application (e.g. gnome-do) from Startup program list.
gnome_do = sDialog.findTableCell(re.compile('^GNOME Do'))

gnome_do.grabFocus()
sleep(config.SHORT_DELAY)

# Variable gnome-do program informations
sDialog.findPushButton("Edit").mouseClick()
sleep(config.SHORT_DELAY)

edit_dialog = app.findDialog("Edit Startup Program")

g_dict = {}
g_text_list = edit_dialog.findAllTexts(None)
for i in g_text_list:
    if utils.labelledBy(i, "Name:"):
        g_dict['Name:'] = i.text
    if utils.labelledBy(i, "Command:"):
        g_dict['Command:'] = i.text
    if len(i.getRelationSet()) == 0:
        g_dict['Comment:'] = i.text
procedurelogger.expectedResult("GNOME DO programs information %s" % g_dict)

edit_dialog.findPushButton("Cancel").mouseClick()
sleep(config.SHORT_DELAY)

# Remove GNOME Do
sDialog.findPushButton("Remove").mouseClick()
sleep(config.SHORT_DELAY)

assertFind(re.compile('^GNOME Do\nDo things as quickly'), "TableCell", available=False)

# Step3: In tab"Options", check box "Automatically remember running applications when logging out"
sDialog.findPageTab("Options").mouseClick()
sleep(config.SHORT_DELAY)

checkbox = sDialog.findCheckBox(None)
if not checkbox.checked:
    checkbox.mouseClick()
    sleep(config.SHORT_DELAY)

sDialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
app.assertClosed()

# Step4: Launch "gnome-session-properties" again
app = launchApp("/usr/bin/gnome-session-properties", "gnome-session-properties", window='Dialog')
sDialog = app.gnomeSessionPropertiesDialog

# Check setting
assertFind("Banshee\nadd banshee to startup", "TableCell")
assertFind(re.compile('^GNOME Do\nDo things as quickly'), "TableCell", available=False)

# Revert settings to remove Banshee
sDialog.findTableCell("Banshee\nadd banshee to startup").grabFocus()
sleep(config.SHORT_DELAY)
sDialog.findPushButton("Remove").mouseClick()
sleep(config.SHORT_DELAY)

# Revert settings to add GNOME Do
sDialog.findPushButton("Add").mouseClick()
sleep(config.SHORT_DELAY)

add_dialog = app.findDialog("Add Startup Program")

text_list = add_dialog.findAllTexts(None)
for i in text_list:
    if utils.labelledBy(i, "Name:"):
        i.insertText(g_dict['Name:'])
    if utils.labelledBy(i, "Command:"):
        i.insertText(g_dict['Command:'])
    if len(i.getRelationSet()) == 0:
        i.insertText(g_dict['Comment:'])

add_dialog.findPushButton("Add").mouseClick()
sleep(config.SHORT_DELAY)

# Revert settings to uncheck the "Automatically remember"
sDialog.findPageTab("Options").mouseClick()
sleep(config.SHORT_DELAY)

checkbox = sDialog.findCheckBox(None)
if checkbox.checked:
    checkbox.mouseClick()
    sleep(config.SHORT_DELAY)

# Quit app
sDialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
app.assertClosed()

