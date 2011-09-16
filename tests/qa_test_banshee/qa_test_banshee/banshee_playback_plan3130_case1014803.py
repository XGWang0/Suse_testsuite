#!/usr/bin/env python

##############################################################################
# Description: Test all of the playback functions of Banshee. 
# Written by:  Felicia Mu<fxmu@novell.com>, David Mulder <dmulder@novell.com>
##############################################################################

# The docstring below is used in the generated log file
"""
Action:
Step1: Play selected file (Spacebar):  Select a song,Touch "Play/Pause" item in Playback menu or Spacebar .
Step2: Stop when finished (Shift-Spacebar)
Step3: Previous file (B)
Step4: Next file (N)
Step5: Seek Forward (Ctrl-Right)
Step6: Seek Backward (Ctrl-Left)
Step7: Seek To (T) ,change progressbar to any position
Step8: Restart Song (R)
"""

# imports
from strongwind import *
from banshee_frame import *
import subprocess
import os, sys
import urllib

# open the label sample application
try:
	app = launchApp("/usr/bin/banshee-1", "Banshee")
except IOError, msg:
	print "ERROR:  %s" % msg
	exit(2)
# just an alias to make things shorter
bFrame = app.findFrame("Banshee Media Player")

# Download audio files for testing (these mp3s are public domain).
blues = "/usr/share/sounds/blues/"
if not os.path.exists(blues) :
	os.mkdir(blues)
	urllib.urlretrieve("http://ia600309.us.archive.org/21/items/MaRainey-SlaveToTheBlues_406/01SlaveToTheBlues.mp3", blues + "SlaveToTheBlues.mp3")
	urllib.urlretrieve("http://ia600403.us.archive.org/20/items/BlindLemonJefferson-oneDimeBlues/BlindLemonJefferson-OneDimeBlues.mp3", blues + "OneDimeBlues.mp3")
	urllib.urlretrieve("http://ia600603.us.archive.org/25/items/TexasAlexander-RangeInMyKitchenBlues/TexasAlexander-RangeInMyKitchenBlues.mp3", blues + "RangeInMyKitchenBlues.mp3")
	urllib.urlretrieve("http://ia600408.us.archive.org/5/items/KansasCityKittyAndGeorgiaTom-howCanYouHaveTheBlues/Kansas_City_Kitty_and_Georgia_Tom--How_Can_You_Have_the_Blues.mp3", blues + "How_Can_You_Have_the_Blues.mp3")

# Step1: Play selected file (Spacebar):  Select a song,Touch "Play/Pause" item in Playback menu or Spacebar .
helpMenu = bFrame.findMenu("Media")
helpMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"Media\"'s submenu is shown")

# Impot a playlist
importMenu= helpMenu.findMenuItem("Import Media...")
importMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)
importDialog = app.findDialog("Import Media to Library")

# on the new dialog select "Local Folders" 
combobox = importDialog.findComboBox("Local Folders")
menu = combobox.findMenu("", checkShowing= False)
combobox.mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"Local Folders\" menu is expanded")

localFoldersItem = menu.findMenuItem("Local Folders")
localFoldersItem.mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"Local Folders\" menu item is selected")
  
# Click "Import Media Source" button
importButton = importDialog.findPushButton("Import Media Source")
importButton.mouseClick()
sleep(config.SHORT_DELAY)
foldersDialog = app.findDialog("Import Folders to Library")
 
# On the "Import Folders to Library" dialog ,click "Type a file name" toggle button
procedurelogger.action("check if the toggle button is pressed")
typeToggleButton = foldersDialog.findToggleButton("Type a file name")
if not typeToggleButton.checked:
	typeToggleButton.mouseClick() 
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the toggle button is toggleed, the text is shown")

# Select "File System" table cell
splitPane = foldersDialog.findSplitPane("")
scrollPane = splitPane.findScrollPane("")
table = scrollPane.findTable("Places")
fileSyletemTableCell = table.findTableCell("File System")
fileSyletemTableCell.mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("\"File System\" is selected")

# Select /usr/share/sounds
fileTable = splitPane.findTable("Files")
fileTable.mouseClick()
typeText(foldersDialog, "usr")
keyPress(foldersDialog, key_name="enter",num=1)
sleep(config.SHORT_DELAY)
typeText(foldersDialog, "share")
keyPress(foldersDialog, key_name="enter", num=1)
sleep(config.SHORT_DELAY)
typeText(foldersDialog, "sounds")
keyPress(foldersDialog, key_name="enter", num=1)
typeText(foldersDialog, "blues")
keyPress(foldersDialog, key_name="enter", num=1)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("\"/usr/share/sounds/blues\" is selected")

# Click "Open" button
openButton = foldersDialog.findPushButton("Open")
openButton.mouseClick()
sleep(config.LONG_DELAY)
procedurelogger.expectedResult("the playlist is loaded")

# Set the sliderStopped value
slider = bFrame.findSlider("")
sliderStopped = slider._accessible.queryValue().currentValue

# Click "Play" button to play the song
playButton = bFrame.findPushButton("Play")
playButton.mouseClick()
sleep(config.SHORT_DELAY)

# Test if the files can be played in banshee
procedurelogger.action("play the new loaded song in banshee")
sliderFirst = slider._accessible.queryValue().currentValue
sleep(config.MEDIUM_DELAY)

sliderSecond = slider._accessible.queryValue().currentValue
assert (sliderFirst != sliderSecond)
procedurelogger.expectedResult("the new loaded song can be played in banshee")

# Pause the song
pauseButton = bFrame.findPushButton("Pause")
pauseButton.mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the new loaded song is pauseed")

# Test if the files can be paused in banshee
procedurelogger.action("pause the new loaded song in banshee")
sliderFirst = slider._accessible.queryValue().currentValue
sleep(config.LONG_DELAY)

sliderSecond = slider._accessible.queryValue().currentValue
assert (sliderFirst == sliderSecond)
procedurelogger.expectedResult("the new loaded song can be pauseed in banshee")

# Play the song again
pauseButton.mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the new loaded song is played")

# Step2: Stop when finished (Shift-Spacebar)
#2.If "stop when finished " is selected,after current song is finished,
#next song should not be played.otherwise, next song should be played automatically.

# Select "Playback" menu
playBackMenu = bFrame.findMenu("Playback")
playBackMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"Playback\"'s submenu is shown")

# Check if the "stop when finished" menu item is selected, if not select it.
procedurelogger.action("Check if the \"Stop When Finished\" menu item is selected.")
stopWhenFinishMenu = playBackMenu.findCheckMenuItem("Stop When Finished")
if not stopWhenFinishMenu.checked:
	stopWhenFinishMenu.mouseClick()
sleep(config.LONG_DELAY)
procedurelogger.expectedResult("The \"Stop When Finished\" menu item is selected.")

# After current song is finished,next song should not be played.
procedurelogger.action("After current song is finished, next song should not be played.")
sliderFirst = slider._accessible.queryValue().currentValue
sleep(config.LONG_DELAY)
sliderSecond = slider._accessible.queryValue().currentValue
while sliderSecond > sliderFirst:
	sliderSecond = slider._accessible.queryValue().currentValue
	sleep(config.SHORT_DELAY)

sliderSecond = slider._accessible.queryValue().currentValue
assert (sliderSecond == sliderStopped)
procedurelogger.expectedResult("After current song is finished, next song is not played.")

# Make the the "stop when finished" menu item unchecked
if stopWhenFinishMenu.checked:
	stopWhenFinishMenu.mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("The \"stop when finished\" menu item is unchecked.")

# Click "Play" button to play the song
playButton = bFrame.findPushButton("Play")
playButton.mouseClick()
sleep(config.LONG_DELAY)

# After current song is finished, Next song should be played automatically.
procedurelogger.action("After current song is finished, next song should be played automatically.")
sliderFirst = slider._accessible.queryValue().currentValue
sleep(config.LONG_DELAY)
sliderSecond = slider._accessible.queryValue().currentValue
while sliderSecond > sliderFirst:
	sliderSecond = slider._accessible.queryValue().currentValue
	sleep(config.SHORT_DELAY)

sliderSecond = slider._accessible.queryValue().currentValue
assert (sliderSecond != sliderStopped)
procedurelogger.expectedResult("After current song is finished, next song is played automatically.")

# Step3: Select the Previous button.
sleep(config.LONG_DELAY)
sliderFirst = slider._accessible.queryValue().currentValue
previousButton = bFrame.findPushButton("Previous")
previousButton.mouseClick()
procedurelogger.expectedResult("the \"previous\" button is selected")
 
# Check if the song is played again
sleep(config.SHORT_DELAY)
sliderSecond = slider._accessible.queryValue().currentValue
assert (sliderSecond < sliderFirst)
procedurelogger.expectedResult("The song is played again")

# Step4: Play the Next song
titleFirst = bFrame.name
nextButton = bFrame.findPushButton("Next")
nextButton.mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the \"next\" button is selected")

# Check if the next song is played 
titleSecond = bFrame.name
assert (titleFirst != titleSecond)
procedurelogger.expectedResult("The next song is played")

# Step5: Seek Forward (Ctrl-Right)
playBackMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("The \"PlayBack\"'s sub menu is shown")

# Click "Seek to..." menu item
seekToMenuItem = playBackMenu.findMenuItem("Seek to...")
seekToMenuItem.mouseClick()
sleep(config.SHORT_DELAY)
seekDialog = app.findDialog("Seek to Position")

# On the "Seek to Position" dialog, forward the song
seekSlider = seekDialog.findSlider("")
seekSliderValue = seekSlider._accessible.queryValue().currentValue
beforeSeek = seekSliderValue
seekSliderValue = seekSliderValue + 20
sleep(config.SHORT_DELAY)
assert (beforeSeek < seekSliderValue)
procedurelogger.expectedResult("The song is skipped forward.")
  
# forward the song again
beforeSeek = seekSliderValue
seekSliderValue = seekSliderValue + 20
sleep(config.SHORT_DELAY)
assert (beforeSeek < seekSliderValue)
procedurelogger.expectedResult("The song is skipped forward.")

# Step6: Seek Backward (Ctrl-Left)
beforeSeek = seekSliderValue
seekSliderValue = seekSliderValue - 20
sleep(config.SHORT_DELAY)
assert (beforeSeek > seekSliderValue)
procedurelogger.expectedResult("The song is skipped backward.")

# backward the song again
beforeSeek = seekSliderValue
seekSliderValue = seekSliderValue - 20
sleep(config.SHORT_DELAY)
assert (beforeSeek > seekSliderValue)
procedurelogger.expectedResult("The song is skipped backward.")

# Close the "Seek to Position" dialog
closeButton = seekDialog.findPushButton("Close")
closeButton.mouseClick()
sleep(config.SHORT_DELAY)
seekDialog.assertClosed()

# Step7: Restart Song (R)
playBackMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("The \"PlayBack\"'s sub menu is shown")

# Click "Restart Song" menu item
titleFirst = bFrame.name
sliderFirst = slider._accessible.queryValue().currentValue
restartSongMenuItem = playBackMenu.findMenuItem("Restart Song")
restartSongMenuItem.mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("The \"Restart Song\" menu item is selected")

# Check if the song is restarted
titleSecond = bFrame.name 
sliderSecond = slider._accessible.queryValue().currentValue
assert (sliderSecond < sliderFirst and titleFirst == titleSecond)
procedurelogger.expectedResult("The next song is restarted")

# Step8: Repeat Single
playBackMenu.mouseClick(log=True)
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("The \"PlayBack\"'s sub menu is shown")

# Click "Repeat" menu 
repeatMenu = playBackMenu.findMenu("Repeat")
repeatMenu.mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("The \"Repeat\"'s sub menu is shown")

# Check the "Repeat Single" check menu item
procedurelogger.action("Check if the \"Repeat Single\" menu item is checked")
repeatSingleMenuItem = repeatMenu.findCheckMenuItem("Repeat Single")
if not repeatSingleMenuItem.checked:
	repeatSingleMenuItem.mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("the  the \"Repeat Single\" menu item is checked")

# Close the application.
menubar = bFrame.findMenuBar(None)
menubar.select(['Media', 'Quit'])
sleep(config.SHORT_DELAY)
bFrame.assertClosed()

