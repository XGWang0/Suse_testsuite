#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE. All Rights Reserved.
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
# Date:        10/25/2010
# Description: Firefox Online Video Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===Online Video test===
View Web Pages as following, browser video, check if video plays.
Step1: Load http://www.youtube.com/
Step2: Load http://vimeo.com/
Step3: Load http://www.youku.com/
Step4: Load http://www.tudou.com/

NOTE:
Adobe Flash Player is accessibled to a 'Text' role that is hard to ensure the video is playing, the test just to launch the web page.
"""
# imports
import re
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# Launch Firefox.
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

def loadWeb(web_url):
    # focus to URL location
    fFrame.findMenuItem(re.compile('^Open Location'), checkShowing=False).click(log=True)
    sleep(config.SHORT_DELAY)
    # insert web URL
    procedurelogger.action('insert %s' % web_url)
    fFrame.findEntry("Search Bookmarks and History").text = web_url
    sleep(config.SHORT_DELAY)
    # press Enter
    fFrame.keyCombo("enter", grabFocus=False)
    sleep(config.LONG_DELAY)

def assertWeb(web_name, accessible_name=True):
    procedurelogger.expectedResult('Make sure %s is loaded' % web_name)
    if accessible_name:
        fFrame.findDocumentFrame(re.compile('^%s' % web_name))
    else:
        doc_frame = fFrame.findDocumentFrame(None)
        doc = doc_frame._accessible.queryDocument().getAttributeValue('DocURL')
        assert doc == web_name, "DocURL expected:%s,actual: %s" % \
                                                           (web_name, doc)

# Step1: Load http://www.youtube.com/
loadWeb("http://www.youtube.com/watch?v=O7W0DMAx8FY&feature=topvideos")
assertWeb("http://www.youtube.com/watch?v=O7W0DMAx8FY&feature=topvideos", accessible_name=False)

# Step2: Load http://vimeo.com/
loadWeb("http://vimeo.com/")
assertWeb("Vimeo")

# Step3: Load http://www.youku.com/
loadWeb("http://www.youku.com/")
assertWeb("http://www.youku.com/", accessible_name=False)

# Step4: Load http://www.tudou.com/
loadWeb("http://www.tudou.com/")
assertWeb("http://www.tudou.com/", accessible_name=False)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

