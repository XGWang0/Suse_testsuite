#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

def updateCacheEntry(size):
    try:
        cache_entry = preferences_frame.findEntry(re.compile('^Use up to'))
    except SearchError:
        cache_check = preferences_frame.findCheckBox(re.compile('^Override'))
        if not cache_check.checked:
            cache_check.mouseClick()
            sleep(config.SHORT_DELAY)
        cache_entry = preferences_frame.findPanel("Offline Storage").findEntry(None)

    cache_entry.mouseClick(log=False)
    cache_entry.deleteText()
    procedurelogger.action('set cache_size to %s' % size)
    cache_entry.text = size
    sleep(config.SHORT_DELAY)

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

preferences_frame = pyatspi.findDescendant(app, lambda x: x.name == "Firefox Preferences")
preferences_frame.findListItem("Advanced").mouseClick()
sleep(config.SHORT_DELAY)
preferences_frame.findPageTab("Network").mouseClick()
sleep(config.SHORT_DELAY)

updateCacheEntry('0')

preferences_frame.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)

# Remove exist cache files
os.system('rm -fr %s' % cache_path)
sleep(config.SHORT_DELAY)

# Step2: Open http://www.google.com
openURL(fFrame, "http://www.google.com")

# Step3: Make sure no file saved in cache
procedurelogger.expectedResult("Make sure the writing is disabled, no cache exist")
assert not os.path.exists(cache_path), "%s shouldn't exist" % cache_path

# Set cache_size to default 50
menubar.select(['Edit', 'Preferences'])
sleep(config.MEDIUM_DELAY)

preferences_frame = pyatspi.findDescendant(app, lambda x: x.name == "Firefox Preferences")
preferences_frame.findListItem("Advanced").mouseClick()
sleep(config.SHORT_DELAY)
preferences_frame.findPageTab("Network").mouseClick()
sleep(config.SHORT_DELAY)

updateCacheEntry('50')

preferences_frame.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)

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

