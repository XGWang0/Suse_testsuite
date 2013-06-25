#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Date:        10/14/2010
# Description: Launch Firefox
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===Launch test===
1. Launch the Firefox browser at the first time via Computer->Firefox
2. Click "know your right"
3. Quit the Firefox and restart the Firefox.
"""

# imports
import subprocess
import os
import re

from strongwind import *
from firefox_frame import *

def setValue(file_path, value_old, value_new):
    f = open(file_path, 'r')
    content = f.read()
    f.close()

    content = re.sub(r'\b%s\b' % value_old, value_new, content)

    f = open(file_path, 'w')
    f.write(content)
    f.close()        

# Make sure MozillaFirefox version is expected for the test
checkVersion()

#Reset Firefox to defaults and store the directory of the original profile.
profiles = os.getenv("HOME") + '/.mozilla/firefox/profiles.ini'
old_directory = os.popen("grep Path %s" % profiles).read().strip('\n')

setValue(profiles, value_old="IsRelative=1", value_new="IsRelative=0")

# open the Firefox application
try:
  app = launchApp('/usr/bin/firefox', "Firefox", wait=30)
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)

# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# Clicks the 'Know your rights' button from firefox first run.
rightsbtn = fFrame.findPushButton(re.compile('^Know your rights'))
rightsbtn.mouseClick()
sleep(config.SHORT_DELAY)

# Assert that the Know your rights tab opened.
procedurelogger.expectedResult("about:rights page appears")
assert fFrame.findPageTab('about:rights')
sleep(config.SHORT_DELAY)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
quitMultipleTabs(app)
app.assertClosed()

# Restore previous firefox settings.
new_directory = os.popen("grep Path %s" % profiles).read().strip('\n')
temp_directory = new_directory.split('=')[1]

setValue(profiles, value_old=new_directory, value_new=old_directory)

# Delete the temporary profile
subprocess.Popen('rm -rf ~/.mozilla/' + temp_directory, shell=True)


