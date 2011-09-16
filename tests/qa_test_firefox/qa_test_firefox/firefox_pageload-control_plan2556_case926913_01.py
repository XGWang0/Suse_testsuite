#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        10/27/2010
# Description: Firefox Page Load Control Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===Page Load Control test===

Step1: Launch a site:www.novell.com, clink "About Novell", 
click "Products" in page
Step2: Click Back button twice
Step3: Make sure the page is turn to the first page www.novell.com/home
Step4: Click Forward button twice
Step5: Make sure The page is turn to www.novell.com/products/
Step6: Load www.novell.com in the browser again, Click the Stop button before 
the page load is completed
Step7: Page loading and any indication of loading should cease
Step8: Click Reload
Step9: Ensure that the page loads completely
"""
# imports
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

# Step1: Launch a site:www.novell.com, clink "About Novell"
# click "Products" in page
openURL(fFrame, "www.novell.com")

fFrame.findLink(re.compile('^About Novell')).mouseClick()
sleep(config.SHORT_DELAY)

fFrame.findLink("Products").mouseClick()
sleep(config.SHORT_DELAY)

# Make sure the page is turn to products
procedurelogger.expectedResult("Make sure the page is turn to products")
fFrame.findDocumentFrame("Products - Novell")
assert fFrame.findEntry("Search Bookmarks and History").text == \
                                      "http://www.novell.com/products/", \
                                                  "page shouldn't be products"

# Step2: Click Back button twice
fFrame.findPushButton("Back").mouseClick()
sleep(config.SHORT_DELAY)

fFrame.findPushButton("Back").mouseClick()
sleep(config.MEDIUM_DELAY)

# Step3: Make sure the page is turn to the first page www.novell.com/home
procedurelogger.expectedResult("Make sure the page is turn to www.novell.com/home")
fFrame.findDocumentFrame(re.compile('^NOVELL'))
assert fFrame.findEntry("Search Bookmarks and History").text == \
                                             "http://www.novell.com/home/", \
                                              "page shouldn't be home"


# Step4: Click Forward button twice
fFrame.findPushButton("Forward").mouseClick()
sleep(config.SHORT_DELAY)

fFrame.findPushButton("Forward").mouseClick()
sleep(config.MEDIUM_DELAY)

# Step5: Make sure The page is turn to www.novell.com/products/
procedurelogger.expectedResult("Make sure the page is turn to products")
fFrame.findDocumentFrame(re.compile('^Products'))
assert fFrame.findEntry("Search Bookmarks and History").text == \
                                         "http://www.novell.com/products/", \
                                          "page shouldn't be products"

# Step6: Load www.novell.com in the browser again, Click the Stop button
stop_button = fFrame.findPushButton("Stop")

url = "www.novell.com"
procedurelogger.action("Launch %s" % url)
fFrame.findMenu("File").mouseClick()
sleep(config.SHORT_DELAY)
fFrame.findMenuItem(re.compile('^Open Location')).mouseClick()
sleep(config.SHORT_DELAY)

url_entry = fFrame.findEntry("Search Bookmarks and History")
url_entry.text = url
sleep(config.SHORT_DELAY)
url_entry.keyCombo("enter")
sleep(config.SHORT_DELAY)

stop_button.mouseClick()
sleep(config.SHORT_DELAY)

# Step7: Page loading and any indication of loading should cease
procedurelogger.expectedResult("Page loading and any indication of loading should cease")

child_count = fFrame.findDocumentFrame(re.compile('^NOVELL')).childCount
assert child_count == 0 or child_count < 5, \
                                    "Page shouldn't load completely"

# Step8: Click Reload
fFrame.findPushButton("Reload").mouseClick()
sleep(config.LONG_DELAY)

# Step9: Ensure that the page loads completely
sleep(config.MEDIUM_DELAY)
procedurelogger.expectedResult("Ensure that the page loads completely")
child_count = fFrame.findDocumentFrame(re.compile('^NOVELL')).childCount
assert child_count == 5, "Page doesn't load completely"

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()
