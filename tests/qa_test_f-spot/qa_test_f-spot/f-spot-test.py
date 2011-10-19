#!/usr/bin/python
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
# Description: Test case for f-spot
# Written by csxia
##############################################################################


	
usage = """Options:
	-c  --case=testcasename	
	-h --help
	"""


# followings are standard exit code for ctcs2
EXIT_CODE_SUCCESS = 0
EXIT_CODE_FAILED = 1
EXIT_CODE_ERR = 11



import pyatspi
import os
import sys
import commands
from strongwind import *

dir = "/usr/share/qa/qa_test_f-spot/data" 



def not_implemented():
	'''
	for calls which is not in cases
	'''
	print "Call not implemented" 
	sys.exit(EXIT_CODE_ERR)



def setup_test_enviroment():
	''' 
		Launch f-spot for testing
	'''
	global app
	global F_f_spot 
	global exe_line
	try:
		app = launchApp("/usr/bin/f-spot","f-spot")
	except IOError,msg:
		print "Error: %s" %msg
		sys.exit(EXIT_CODE_FAILED)
	if app is None:
		print "Cannot Launch f-spot application, Exit now "
		sys.exit(EXIT_CODE_FAILED)
	F_f_spot = app.findFrame("F-Spot")

def cleanup_test_enviroment():
	'''
	clean up Test 
	close Application
	'''
	#sometime cannot use altF4 to close the window
	#F_f_spot.altF4()
	
	#alternative method
	menubar = F_f_spot.findMenuBar(None)
        menubar.select(["Photo","Quit"])


def case_import_images_2():
	'''
		the main difference between case_import_images_2 and case_import_images is that 
		we use mouse to select path, rather than input path in location inputbox 
		see BNC636530
	'''
	setup_test_enviroment()
	try:
		menubar = F_f_spot.findMenuBar(None)
		menubar.select(["Photo","Import..."])
	except:
		print "Error occurs when select Photo->Import"	
		cleanup_test_enviroment()
		sys.exit(EXIT_CODE_FAILED)
	sleep(config.SHORT_DELAY)
	
	try:
		importDialog = app.findDialog("Import")
	except:
                print "Error occurs when find import dialog"
                sleep(config.SHORT_DELAY)
                cleanup_test_enviroment()
                sys.exit(EXIT_CODE_FAILED)

        selection={"0":"Select Folder"}
        importDialog.selectCombobox(selection)
        sleep(config.SHORT_DELAY)
        dialogs_import = []
        try:
                dialogs_import = app.findAllDialogs('Import')
        except:
		print "Error occurs when find import dialog"
                sleep(config.SHORT_DELAY)
                cleanup_test_enviroment()
                sys.exit(EXIT_CODE_FAILED)
	
	Places = pyatspi.findDescendant(dialogs_import[1],lambda x: x.name == "Places")
	FileSystem_Cell = Places.select("File System")	
	FileSystem_Cell.mouseClick()	
	dir_strs = dir.split('/')
        sleep(config.SHORT_DELAY)
	Usr = pyatspi.findDescendant(dialogs_import[1],lambda x: x.name == "Files")
		
	
	for path_one_step in dir_strs:
		if path_one_step == "":
			continue
		temp = Usr.select(path_one_step)
		temp.select()
		x, y = temp._getAccessibleCenter()
		#use pyatspi to double click item, since activate method of table cell not implement by strongwind 
		pyatspi.Registry.generateMouseEvent(x , y , "b1d")
                sleep(config.SHORT_DELAY)

	
	dialogs_import[1].clickPushButton("Open")
	#sleep so long so that import action can be finished 
	sleep(config.LONG_DELAY)
			
	dialogs_import[0].clickPushButton("Import")
	sleep(config.SHORT_DELAY)
			
	cleanup_test_enviroment()
	sys.exit(EXIT_CODE_SUCCESS)			
		

def case_import_images():
	setup_test_enviroment()
	try:
		menubar = F_f_spot.findMenuBar(None)	
		menubar.select(["Photo","Import..."])
	except:
		print "Error occurs when select Photo->Import"
		cleanup_test_enviroment()
		sys.exit(EXIT_CODE_FAILED)			
		
	sleep(config.SHORT_DELAY)	
	
	try:
		importDialog = app.findDialog("Import")		
	except:
		print "Error occurs when find import dialog"
		sleep(config.SHORT_DELAY)
		cleanup_test_enviroment()
		sys.exit(EXIT_CODE_FAILED)			

	selection={"0":"Select Folder"}
        importDialog.selectCombobox(selection)
	sleep(config.SHORT_DELAY)
	dialogs_import = []
	try:
		dialogs_import = app.findAllDialogs('Import')
		sleep(config.SHORT_DELAY)
	except:
		print "Error when find import dialogs (there should be two dialogs)"
		sleep(config.SHORT_DELAY)
		cleanup_test_enviroment()
		sys.exit(EXIT_CODE_FAILED)			

	path_images = {"0":dir}
	try:
                dialogs_import[1].findText(None, labelledBy="Location:")
		sleep(config.SHORT_DELAY)
        except SearchError:
		dialogs_import[1].findToggleButton("Type a file name").mouseClick()
		sleep(config.SHORT_DELAY)
	try:
		dialogs_import[1].inputItem("Texts",path_images)	
		sleep(config.SHORT_DELAY)
	
		# we have to comment the Open statment since the Open Button has the same key bind 
		# with button "create folder, it should be a f-spot bug"	
		dialogs_import[1].clickItem("PushButton","Cancel")	
		#dialogs_import[1].clickItem("PushButton","Open")	
		sleep(config.SHORT_DELAY)
	except:
		print "Error when import source of image"
		dialogs_import[1].clickItem("PushButton","Cancel")
		sleep(config.SHORT_DELAY)
                dialogs_import[0].clickItem("PushButton","Cancel")
		sleep(config.SHORT_DELAY)
                cleanup_test_enviroment()
		sys.exit(EXIT_CODE_FAILED)			
	
	sleep(config.SHORT_DELAY)
	dialogs_import[0].clickItem("PushButton","Cancel")
	sleep(config.SHORT_DELAY)
	cleanup_test_enviroment()
	sys.exit(EXIT_CODE_SUCCESS)			
	
def case_import_images_first_time():
	'''
	if you launch f-spot for the first time, it will
	show import images dialog automatically
	'''
	setup_test_enviroment()	

	
	try:
		importDialog = app.findDialog("Import")		
		selection={"0":"Select Folder"}
                importDialog.selectCombobox(selection)
	except:
		print "Error occurs when find import dialog"
		sleep(config.SHORT_DELAY)
		cleanup_test_enviroment()
		sys.exit(EXIT_CODE_FAILED)			

	
	sleep(config.SHORT_DELAY)
	dialogs_import = []
	try:
		dialogs_import = app.findAllDialogs('Import')
	except:
		print "Error when find import dialogs (there should be two dialogs)"
		dialogs_import[1].clickItem("PushButton","Cancel")
		sleep(config.SHORT_DELAY)
		dialogs_import[0].clickItem("PushButton","Cancel")
		sleep(config.SHORT_DELAY)
		cleanup_test_enviroment()
		sys.exit(EXIT_CODE_FAILED)			
			
	path_images = {"0":dir}

	dir_strs = dir.split('/')
	try:
		dialogs_import[1].inputItem("Texts",path_images)	
		sleep(config.SHORT_DELAY)
	
		# we have to comment the Open statment since the Open Button has the same key bind 
		# with button "create folder, it should be a f-spot bug"	
		dialogs_import[1].clickItem("PushButton","Cancel")	
		#dialogs_import[1].clickItem("PushButton","Open")	
		sleep(config.SHORT_DELAY)
	except:
		print "Error when import source of image"
		dialogs_import[1].clickItem("PushButton","Cancel")
		sleep(config.SHORT_DELAY)
                dialogs_import[0].clickItem("PushButton","Cancel")
		sleep(config.SHORT_DELAY)
                cleanup_test_enviroment()
		sys.exit(EXIT_CODE_FAILED)			
	
	sleep(config.SHORT_DELAY)
	dialogs_import[0].clickItem("PushButton","Cancel")
	sleep(config.SHORT_DELAY)
	cleanup_test_enviroment()
	sys.exit(EXIT_CODE_SUCCESS)			

	



global dialogs_import
global importDialog

cases = {
	"case_import_images_first_time":case_import_images_first_time,
	"case_import_images":case_import_images,
	"case_import_images_2":case_import_images_2,
	}



if len(sys.argv) < 2:
	print >>sys.stderr,usage
	sys.exit(EXIT_CODE_ERR)

for arg in sys.argv[1:]:
	if arg in ('--help','-h'):
		print >>sys.stderr,usage
		sys.exit(EXIT_CODE_ERR)
	elif arg in ('-c','--case'):
		if len(sys.argv) < 3:
			print >>sys.stderr,usage
			sys.exit(EXIT_CODE_ERR)
		casename = sys.argv[2]
		if casename is None:
			print >>sys.stderr,usage
			sys.exit(EXIT_CODE_ERR)
		cases.get(casename,not_implemented)();		
	else:
		print >>sys.stderr,usage
		sys.exit(EXIT_CODE_ERR)



