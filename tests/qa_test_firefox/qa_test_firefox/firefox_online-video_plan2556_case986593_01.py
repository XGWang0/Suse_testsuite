#!/usr/bin/env python

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
