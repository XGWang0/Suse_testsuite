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

import datetime
import logging
import os
import pickle
import random
import re
import time
import sys
import glob

from suselogging import LoggerHander

class PrjPath(object):
    def __init__(self):
        pass

    @staticmethod
    def getWorkSpace():
        return os.getenv("WORKSPACE", PrjPath().getScriptPath())

    @staticmethod
    def getJksHome():
        return os.getenv("JENKINS_HOME", PrjPath().getScriptPath())

    @staticmethod
    def createFolder(abs_path):
        if os.path.exists(abs_path):
            pass
        else:
            os.makedirs(abs_path)
        return abs_path

    @staticmethod
    def getPrjCfgPath(prj_name):
        prj_cfg_path = os.path.join(PrjPath().getJksHome(), prj_name)
        PrjPath().createFolder(prj_cfg_path)

        return prj_cfg_path

    @staticmethod
    def getBuildNum():
        return os.getenv("BUILD_TAG", "build_%d" %random.randint(10000,999999))

    @staticmethod
    def getJobName():
        return os.getenv("JOB_NAME", PrjPath().getScriptPath())

    @staticmethod
    def getJobURL():
        return os.getenv("JOB_URL", 'http://127.0.0.1:8080')

    @staticmethod
    def getBuildURL():
        return os.getenv("BUILD_URL", 'http://127.0.0.1:8080')

    @staticmethod
    def getProductVersion():
        job_name = PrjPath().getJobName()
        LOGGER.info(job_name)
        product_v = re.search("(%s.*SLE\S+?%s)" %(os.sep, os.sep), job_name, re.I).groups()[0]
        #product_v =  job_name.split(os.sep)[-3].strip()

        return CommonOpt().convertPrjName(product_v)

    @staticmethod
    def getArchName():
        job_name = PrjPath().getJobName()
        return job_name.split(os.sep)[-2].strip()

    @staticmethod
    def getScriptPath():
        return os.path.dirname(os.path.abspath(sys.argv[0]))

    @staticmethod
    def getArchLevelPath():
        return os.path.dirname(PrjPath().getWorkSpace())


class CommonOpt(object):
    @staticmethod
    def getTSName(file_name):
        tc_name = ""

        file_basename = os.path.basename(file_name)
        if file_basename:
            file_testname = os.path.splitext(file_basename)
            tc_name = re.sub("^.*-", "", file_testname[0])
        else:
            tc_name = ""
        
        return tc_name

    @staticmethod
    def convertPrjName(prj_name):
        print prj_name
        if re.search('SLE\S+12\S+SP0', prj_name, re.I):
            return re.sub('SLE\S+12\S+SP0', 'SLE-12', prj_name)
        elif re.search('SLE\S+12\S+sp1', prj_name, re.I):
            return re.sub('SLE\S+12\S+SP1', 'SLE-12-SP1', prj_name)
        elif re.search('SLE\S+11\S+sp3', prj_name, re.I):
            return re.sub('SLE\S+11\S+sp3', 'SLE-11-SP3', prj_name)
        elif re.search('SLE\S+11\S+sp4', prj_name, re.I):
            return re.sub('SLE\S+11\S+SP4', 'SLE-11-SP4', prj_name)
        else:
            return prj_name        

    @staticmethod
    def convertPrjNameI(prj_name):
        print prj_name
        if re.search('sle\S+12\S+sp0', prj_name, re.I):
            return 'SLE12'
        elif re.search('sle\S+12\S+sp1', prj_name, re.I):
            return 'SLE12-SP1'
        elif re.search('sle\S+11\S+sp3', prj_name, re.I):
            return 'SLE11-SP3'
        elif re.search('sle\S+11\S+sp4', prj_name, re.I):
            return 'SLE11-SP4'
        else:
            return prj_name  

    @staticmethod
    def getDiffTime(start_time, end_time):
        begin_time = time.mktime(datetime.datetime.timetuple(start_time))
        end_time = time.mktime(datetime.datetime.timetuple(end_time))
        return abs(int(end_time - begin_time))

    @staticmethod
    def getSubmissionIDFromString(strings):
        ins_submissionid = re.search("ID\s+\d+:\s+(http://.*submission.php.*submission_id=\d+)", strings, re.S|re.I)
        
        if ins_submissionid:
            return ins_submissionid.groups()[0]
        else:
            return ""

    @staticmethod
    def dumpData(file_name, data):
        with open(file_name, "w+") as f:
            f.truncate()
            pickle.dump(data, f)

    @staticmethod            
    def loadData(file_name):
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                return pickle.load(f)
        else:
            return []
    
    @staticmethod
    def cleanFile(subfix="pkl"):
        path = PrjPath().getWorkSpace()
        files = os.path.join(path, '*.%s' %subfix)
        for f in glob.glob(files):
            os.remove(f)
        
        LOGGER.info("Clean all file with suffix %s in path %s" %(subfix, path))
        
    @staticmethod
    def generateRandomStr():
        const_str = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        return ''.join(random.sample(const_str,30))
    
    @staticmethod
    def generateUUID(string):
        import uuid
        str_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, string))
        LOGGER.debug('UUID : %s' %str_uuid)
        return str_uuid

    @staticmethod
    def getOSPrdVerAndArch(content):
        if 'SUSE Linux Enterprise Server' in content:
            re_compile = re.compile('SUSE Linux Enterprise Server\s+(\d+)\s+([SP]*\d*).*\((\S+)\)\s+-\s+Kernel', re.I)
            re_ser = re_compile.search(content)
            if re_ser:
                p_v, s_v, arch = re_ser.groups()
                p_v = p_v.strip().upper()
                s_v = s_v.strip().upper()
                if p_v and s_v:
                    return ('SLE-%s-%s' %(p_v, s_v), arch)
                elif p_v and not s_v:
                    return ('SLE-%s' %(p_v), arch)
                else:
                    return (None, None)
        elif 'openSUSE' in content:
            re_compile = re.compile('openSUSE\s+(\d+[.]*\d*)\s+.*Kernel', re.I)
            re_ser = re_compile.search(content)
            if re_ser:
                return (re_ser.groups()[0],'x86_64')
            else:
                return (None, None)
    
'''
def getPrjCfgPath(prj_name):
    return PrjPath().getPrjCfgPath(prj_name)
'''




####----------------------- Common Variable start -----------------------------------#
#Project Common constant variables
LOGGER = LoggerHander("sys.log", level=logging.DEBUG)


PREFIX_STORE_FILE_NAME = "pickel_file_%s.pkl"


PREFIX_ADD_REPO_CMD = "zypper --no-gpg-checks -n ar %(repo_addr)s %(repo_nike)s"
PREFIX_REF_REPO_CMD = "zypper --gpg-auto-import-keys ref -r %(repo_nike)s"
#PREFIX_INS_REPO_CMD = "zypper in -y -r %(repo_nike)s %(ts_name)s"
PREFIX_INS_REPO_CMD = "zypper in -y %(ts_name)s"

# Reinstallation constant variables
REINSTALL_MACHINE_USER = 'root'
REINSTALL_MACHINE_PASSWD = 'susetesting'
'''
REINSTALL_MACHINE_CMD = ('/usr/share/qa/tools/install.pl '
                         '-o "console=ttyS0,115200 vnc=1 vncpassword=susetesting"'
                         ' -p %(repo)s -t base -B')

REINSTALL_MACHINE_CMD = ('/usr/share/qa/tools/install.pl '
                         '-o "vnc=1 vncpassword=susetesting"'
                         ' -p %(repo)s -t base -B')
'''

REINSTALL_MACHINE_CMD = ('/usr/share/qa/tools/install.pl '
                         ' -p %(repo)s -t base -B')

REGRESSION_TEST_CFG_PATH = PrjPath().getPrjCfgPath("REGRESSION_TEST_CFG")
HOST_STATUS_FILE = os.path.join(REGRESSION_TEST_CFG_PATH, "HOST_STATUS1.cfg")
####----------------------- Common Variable end  -------------------------------------#

####----------------------- Regression test start  -----------------------------------#

#---- Monitor build variable start ------#
RT_PRJ_CONFIG_PATH = PrjPath().createFolder(os.path.join(REGRESSION_TEST_CFG_PATH,"RT_CFG"))

RT_REF_TEST_CFG_FILE = os.path.join(RT_PRJ_CONFIG_PATH, 'rt.cfg')
RT_RDY_TRIGGER_JOB_FILE = os.path.join(RT_PRJ_CONFIG_PATH, 'READY_TRIGGER_JOB.cfg')

#---- Monitor build variable end --------#


#---- Stress V/Kernel R/UserSpace start ------#
PREFIX_QA_HEAD_REPO = 'http://dist.nue.suse.com/ibs/QA:/Head/'
PREFIX_PRODUCT_SDK_L_REPO = 'http://147.2.207.1/dist/install/SLP/%(prd_name)s-SDK-LATEST/%(arch)s/dvd1/'
PREFIX_PRODUCT_SDK_R_REPO = 'http://dist.suse.de/install/SLP/%(prd_name)s-SDK-LATEST/%(arch)s/DVD1/'
## Test suite common constant variable

TS_QASET_PATH = '/usr/share/qa/qaset/qaset'

TS_QASET_RESET_CMD = TS_QASET_PATH + " reset"

TS_GET_SUBMISSION_ID_CMD = 'grep -E "http://.*/submission.php.*submission_id=[0-9]+" %s'

TS_STRESS_VALID_NAME = 'qa_testset_automation'
TS_STRESS_VALID_NICK = "QA_REPO" + str(random.randint(10000,99999))
TS_STRESS_VALID_RUN_NAME = '/usr/share/qa/qaset/run/regression-run'

TS_STRESS_VALID_DONE_FILE = '/var/log/qaset/control/DONE'
TS_STRESS_VALID_FAILED_FILE = '/root/qaset/list.failed'
TS_STRESS_VALID_MONITOR_FILE = '/var/log/qaset/control/NEXT_RUN'
TS_STRESS_VALID_SUBMISSION_FOLDER = '/var/log/qaset/submission/'
TS_STRESS_VALID_RUNS_FOLDER = '/var/log/qaset/runs/'

#---- Stress V/Kernel R/UserSpace end --------#
####----------------------- Regression test end  -------------------------------------#

####----------------------- KTOD start  ----------------------------------------------#

#---- monitor build start ------------------------#
KOTD_PRJ_CONFIG_PATH = PrjPath().createFolder(os.path.join(REGRESSION_TEST_CFG_PATH,"KOTD_CFG"))

KOTD_REF_TEST_CFG_FILE = os.path.join(KOTD_PRJ_CONFIG_PATH, 'kotd.cfg')
KOTD_RDY_TRIGGER_JOB_FILE = os.path.join(KOTD_PRJ_CONFIG_PATH,'NEEDED_2TRIGGER_JOB.cfg')
#---- monitor build end --------------------------#


#---- KTOD test start ------------------------#
KTOD_KERNEL_VALID_NICK = "KERNEL_REPO" + str(random.randint(10000,99999))
#---- KTOD test end --------------------------#


####----------------------- KTOD end   ----------------------------------------------#

#TS_KERNEL_NAME = ''
#TS_USER_APP_NAME = ''
