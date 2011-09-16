#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        08/01/2011
# Description: Gnome Application starts on login test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Application Startup===
Step1: Launch "gnome-session-properties" 
Step2: In tab "Startup Program", add an application (e,g. banshee) to Startup program list
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

# Revert settings to remove Banshee
sDialog.findTableCell("Banshee\nadd banshee to startup").grabFocus()
sleep(config.SHORT_DELAY)
sDialog.findPushButton("Remove").mouseClick()
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
