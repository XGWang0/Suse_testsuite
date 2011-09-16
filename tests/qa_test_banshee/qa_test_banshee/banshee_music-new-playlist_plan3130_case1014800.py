#!/usr/bin/env python

##############################################################################
# Description: Test the functionality available under the Music -> New Playlist
#  menu item. 
# Written by:  Felicia Mu<fxmu@novell.com>
##############################################################################

# The docstring below is used in the generated log file
"""
Step1: Create New Playlist from right-click "Music Library". 
Step2: Create Many Playlists(ten playlists) :New many Playlists by "Ctrl-N".
Step3. Assert that large Playlists can be created.
Step4. Rename Playlist
Step5: Rename plsylist by long Playlist name
Step6: Delete Playlist
"""
# imports
from strongwind import *

# open the label sample application
try:
  app = launchApp("/usr/bin/banshee-1", "Banshee")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
bFrame = app.findFrame("Banshee Media Player")

# Step1: Create New Playlist from right-click "Music Library". 
musicTreetable = bFrame.findTreeTable("") 
musicTablecell = musicTreetable.findTableCell("Music") 
musicTablecell.mouseClick(3)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the context menu is shown")
 
contextWindow = app.findWindow("")
newPlaylistMenuItem = contextWindow.findMenuItem("New Playlist")
newPlaylistMenuItem.mouseClick() 
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("The new Playlist appears in Music Library ")

# Step2: Create Many Playlists(ten playlists) :New many Playlists by "Ctrl-N".
bFrame.keyCombo("<Ctrl>n")
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("The new Playlist appears in Music Library ")

# Step3: Assert that large Playlists can be created
for i in range(0, 10):
	bFrame.keyCombo("<Ctrl>n")
	sleep(config.SHORT_DELAY)
	procedurelogger.expectedResult("The new Playlist appears in Music Library ")

# Step4: Rename plsylist by 
tableCell = musicTreetable.findTableCell("New Playlist") 
tableCell.mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"New Playlist\" is selected")

tableCell.keyCombo("<F2>")
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"New Playlist\" can be renamed")

tableCell.keyCombo('v', grabFocus=False)
tableCell.keyCombo('v', grabFocus=False)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"New Playlist\" can be renamed")

bFrame.keyCombo("<Enter>")
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"New Playlist\" can be renamed")

# Step5: Rename plsylist by long Playlist name
bFrame.mouseClick()
sleep(config.SHORT_DELAY)
tablecell = musicTreetable.findTableCell("New Playlist") 
tableCell.mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"New Playlist\" is selected")

tableCell.keyCombo("<F2>")
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"New Playlist\" can be renamed")

for i in range(0, 50):
	tableCell.keyCombo('x', grabFocus=False)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"New Playlist\" can be renamed by large name")

bFrame.keyCombo("<Enter>")
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"New Playlist\" can be renamed")

# Step6: Delete Playlist
# Right click the selected menu item
tableCell = musicTreetable.findTableCell("vv")
tableCell.mouseClick(3)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the submenu is shown")

# On the context window, click "delete" menu item
contextWindow = app.findWindow("")
deleteMenuItem = contextWindow.findMenuItem("Delete Playlist")
deleteMenuItem.mouseClick() 
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("The new Playlist appears in Music Library ")

# On the new dialog, select "Delete" button
deleteDialog = app.findDialog("")
deleteButton = deleteDialog.findPushButton("Delete")
deleteButton.mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("The selected menu item is deleted ")
  
# Close the application.
menubar = bFrame.findMenuBar(None)
menubar.select(['Media', 'Quit'])
sleep(config.SHORT_DELAY)
bFrame.assertClosed()

