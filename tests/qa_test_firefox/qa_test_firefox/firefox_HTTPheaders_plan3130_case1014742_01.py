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
# Date:        10/20/2010
# Description: Firefox HTTP headers Test
##############################################################################

# imports
import os
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===HTTP headers test===
Step1: Visit a website.
Step2: Download and install a HTTP Header plug-in(Live HTTP Header) from http://livehttpheaders.mozdev.org/installation.html#
Step3: Check the HTTP header from "Live HTTP Headers" Plugin-->preference.
Step4: Compare the echoed request under HTTP Request & Body to the following (The user agent is the most important thing. The other items may vary):

      GET / HTTP/1.1
Host: google.com
User-Agent: Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100317 SUSE/3.5.9-0.1.1 Firefox/3.5.9
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 300
Connection: keep-alive
Cookie: PREF=ID=a128bd2a846af0fb:U=b7e1a1e03b058805:TM=1273732052:LM=1278579041:S=1rxyPe593x7CGKfA; NID=36=BvBkncDqqecraktGICEyxpjZioWuEQvWn77lc45RHJBvWUNTVp-9JgPcF-ivrA_RvHaBRjhY4fb-ZEX8cJwRmhFTYXY_jmygXh_F3DSOrLAGWBXJObudjJ5CK36FHwyd
"""

# Step1: Visit a website.
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# Step2: make sure HTTP Headers extensions installed, if not just download 
# and install Live HTTP Header from https://addons.mozilla.org/en-US/firefox/addon/3829/
menubar = fFrame.findMenuBar(None)
menubar.select(['Tools', 'Add-ons'])
sleep(config.MEDIUM_DELAY)

try:
    addon_frame = app.findFrame("Add-ons")
except SearchError:
    addon_frame = pyatspi.findAllDescendants(app, lambda x: x.name == "Add-ons Manager")[1]
sleep(config.SHORT_DELAY)

addon_frame.findListItem("Extensions").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('Make sure Live HTTP Header in extensions list')
try:
    flash_plugin = addon_frame.findListItem(re.compile('^Live HTTP headers'))
except SearchError:
    web = "https://addons.mozilla.org/en-US/firefox/addon/3829/"
    closeAddOns(fFrame, addon_frame)
    sleep(config.MEDIUM_DELAY)

    menubar.select(['File', 'Quit'])
    raise Exception, "Live HTTP Header plugin doesn't installed, please install it from %s" % web
    exit(22)
else:
    closeAddOns(fFrame, addon_frame)
    sleep(config.SHORT_DELAY)

# Step3: Check the HTTP header from "Live HTTP Headers" Plugin
menubar.select(['Tools', 'Live HTTP headers'])
sleep(config.MEDIUM_DELAY)

# load http://www.google.com
fFrame.findAutocomplete("Search using Google").mouseClick()
sleep(config.SHORT_DELAY)
fFrame.keyCombo("enter", grabFocus=False)
sleep(config.MEDIUM_DELAY)

# Live HTTP Headers capture headers
live_dialog = app.findDialog("Live HTTP headers")
user_agent = live_dialog.findListItem(re.compile('^User-Agent:'))

# Get the expected User-Agent infomations from system
firefox_vlist = os.popen('rpm -q MozillaFirefox').read().strip('\n').split('-')
firefox_main_version = firefox_vlist[1]
firefox_sub_version = firefox_vlist[2]

if os.path.exists("/usr/lib64/firefox"):
    arch = "lib64"
    distro = "x86_64"
    firefox_sub_version = firefox_sub_version.strip('.x86_64')
else:
    arch = "lib"
    distro = "i686"

firefox_version = "-".join([firefox_main_version, firefox_sub_version])

gecko_version = os.popen('grep MinVersion /usr/%s/firefox/application.ini' % arch).read().strip('\n').split('=')[1]
gecko_build = os.popen('grep BuildID /usr/%s/firefox/application.ini' % arch).read().strip('\n').split('=')[1][:-2]
    
user_agent_name = "User-Agent: Mozilla/5.0 (X11; U; Linux %s; en-US; rv:%s) Gecko/%s SUSE/%s Firefox/%s" % \
               (distro, gecko_version, gecko_build, firefox_version, firefox_main_version)

procedurelogger.expectedResult('User-Agent information is match to the expected %s' % \
                                                                    user_agent_name)
assert user_agent.name == user_agent_name, \
                             "user_agent name expected: %s, actual: %s" % \
                               (user_agent_name, user_agent.name)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
app.assertClosed()

