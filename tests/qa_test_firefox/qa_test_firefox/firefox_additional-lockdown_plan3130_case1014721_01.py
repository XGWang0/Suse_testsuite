#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        11/02/2010
# Description: Firefox Additional Lockdown Features Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===Additional Lockdown Features test===
Step1: Disable writing anything to disk cache by set the Value Edit-->Preferences-->Advanced-->Network-->Offline Stronge to 0
Step2: Open http://www.google.com
Step3: Make sure no file saved in cache
"""

# imports
import os
import glob
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

who = os.getenv("HOME")
profile_path = glob.glob('%s/.mozilla/firefox' % who + os.sep)[0]
default_folder = os.popen("grep Path %s" % profile_path + 'profiles.ini').read().strip().split('=')[1]
default_path = os.path.join(profile_path, default_folder)
cache_path = '%s/Cache' % default_path

# Step1: Disable writing anything to disk cache by set the Value Edit-->Preferences-->Advanced-->Network-->Offline Stronge to 0
menubar = fFrame.findMenuBar(None)
menubar.select(['Edit', 'Preferences'])
sleep(config.SHORT_DELAY)

preferences_frame = app.findFrame("Firefox Preferences")
preferences_frame.findListItem("Advanced").mouseClick()
sleep(config.SHORT_DELAY)
preferences_frame.findPageTab("Network").mouseClick()
sleep(config.SHORT_DELAY)

cache_entry = preferences_frame.findEntry(re.compile('^Use up to'))
cache_entry.mouseClick(log=False)
cache_entry.deleteText()
procedurelogger.action('set cache_size to 0')
cache_entry.text = '0'
sleep(config.SHORT_DELAY)

preferences_frame.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
preferences_frame.assertClosed()

# Remove exist cache files
for i in os.listdir(cache_path):
    os.remove(os.path.join(cache_path,i))
    sleep(config.SHORT_DELAY)

# Step2: Open http://www.google.com
openURL(fFrame, "http://www.google.com")

# Step3: Make sure no file saved in cache
procedurelogger.expectedResult("Make sure the writing is disabled, no cache exist")

cache_list = os.listdir('%s/' % cache_path)

assert cache_list == [], "%s shouldn't exist in %s" % (cache_list, cache_path)

# Set cache_size to default 50
menubar.select(['Edit', 'Preferences'])
sleep(config.SHORT_DELAY)

preferences_frame = app.findFrame("Firefox Preferences")
preferences_frame.findListItem("Advanced").mouseClick()
sleep(config.SHORT_DELAY)
preferences_frame.findPageTab("Network").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.action('set cache_size to 50')
cache_entry = preferences_frame.findEntry(re.compile('^Use up to'))
cache_entry.mouseClick(log=False)
cache_entry.text = '5'
sleep(config.SHORT_DELAY)

preferences_frame.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
preferences_frame.assertClosed()

# Open http://www.suse.com
openURL(fFrame, "http://www.suse.com")

# Make sure a file saved in cache
procedurelogger.expectedResult("Make sure the writing is enabled, a cache exist")

cache_list = os.listdir('%s/' % cache_path)

assert cache_list != [], "%s should exist in %s" % (cache_list, cache_path)

# Close application
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()
