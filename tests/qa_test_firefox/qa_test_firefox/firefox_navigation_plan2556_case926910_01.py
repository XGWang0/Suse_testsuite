#!/usr/bin/env python
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
# Date:        10/21/2010
# Description: Firefox Navigation Test
##############################################################################

# imports
from strongwind import *
from firefox_frame import *

class PluginError(Exception):
    "Raised when plugin doesn't exist"
    pass

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===Navigation test===
Using either File | Open Web Location , the URL Location: textfield, or the keyboard shortcut (Control+L, Alt+L or Command+L, depending on your platform)
load www.yahoo.com
load www.msn.com
load www.amazon.com
load ftp://ftp.novell.com
load www.cnn.com
load www.google.com
load www.ebay.com
load http://slashdot.org
load www.digg.com
load http://www.wikipedia.org
load www.flickr.com
load www.myspace.com
load www.youtube.com
"""

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

def assertWeb(web_name):
    procedurelogger.expectedResult('Make sure %s is loaded' % web_name)
    fFrame.findDocumentFrame(re.compile('^%s' % web_name))

# Step1: load www.yahoo.com
loadWeb("www.yahoo.com")
assertWeb("Yahoo!")

# Step2: load www.msn.com
loadWeb("www.msn.com")
assertWeb("MSN.com")

# Step3: load www.amazon.com
loadWeb("www.amazon.com")
assertWeb("Amazon.com")

# Step4: load ftp://ftp.novell.com
loadWeb("ftp://ftp.novell.com")
assertWeb("Index of ftp://ftp.novell.com/")

# Step5: load www.cnn.com
loadWeb("www.cnn.com")
assertWeb("CNN.com")

# Step6: load www.google.com
loadWeb("www.google.com")
assertWeb("Google")

# Step7: load www.ebay.com
loadWeb("www.ebay.com")
assertWeb("eBay")

# Step8: load http://slashdot.org
loadWeb("http://slashdot.org")
assertWeb("Slashdot")

# Step9: load www.digg.com
loadWeb("www.digg.com")
assertWeb("Digg")

# Step10: load http://www.wikipedia.org
loadWeb("http://www.wikipedia.org")
assertWeb("Wikipedia")

# Step11: load www.flickr.com
loadWeb("www.flickr.com")
assertWeb("Welcome to Flickr")

# Step12: load www.myspace.com
loadWeb("www.myspace.com")
assertWeb("MySpace.com")

# Step13: load www.youtube.com
loadWeb("www.youtube.com")
assertWeb("YouTube")

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

