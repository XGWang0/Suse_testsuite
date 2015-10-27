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

from urllib2 import urlopen, HTTPError
import json

from constantvars import *
from stringcolor import StringColor
from jsongenerator import JsonGenerator
from urloperation import URLParser
from jenkinsapi import JenkinsAPI
from flowcontroller import HostContorller
from conslaves import ConnSlave
from parameterparser import  RegConfigParser as ParseConfig

class QA_TESTSET(object):

    def __init__(self, product, arch, mach, report, feat_info):
        
        LOGGER.debug("report %s" %report)
        #pc = ParseConfig()
        self.product = product
        self.productv = CommonOpt().convertPrjName(product)
        self.arch = arch
        self.report_tuple = self.getReportFile(report)
        self.report_file = self.report_tuple[1]
        self.report_json_file = self.report_tuple[0] + '.json'
        self.report_pkl_file = self.report_tuple[0] + '.pkl'
        LOGGER.info(self.report_json_file)
        LOGGER.info(self.report_pkl_file)
        self.ins_conslave = ConnSlave(mach,
                                      REINSTALL_MACHINE_USER,
                                      REINSTALL_MACHINE_PASSWD)
        self.prefix_feat_name = feat_info[0]
        self.feat_desc = feat_info[1] + '\n'*2 + 'Test Machine :%s' %self.ins_conslave.slave_addr

        self.start_time = datetime.datetime.now()


    def getRepoLocation(self, prj_name):
        pc = ParseConfig()
        config_productv =  self.product.replace('SLE','SLES')

        if prj_name == 'KOTD':
            configfile = KOTD_REF_TEST_CFG_FILE
            self.larch = pc.convertItem(pc.getItem(configfile, config_productv, 'arch'))
            self.rarch = []
        elif prj_name == 'RT':
            configfile = RT_REF_TEST_CFG_FILE
            self.larch = pc.convertItem(pc.getItem(configfile, config_productv, 'larch'))
            self.rarch = pc.convertItem(pc.getItem(configfile, config_productv, 'rarch'))

        LOGGER.debug("Config file is %s" %configfile)      
        LOGGER.debug("local arch is %s" %'|'.join(self.larch))
        LOGGER.debug("remote arch is %s" %'|'.join(self.rarch))
        

    def getReportFile(self, report_file):
        if report_file:
            dirname, base_file = os.path.split(report_file.strip())
            LOGGER.info("%s %s" %(dirname, base_file))
            sufix1 =  base_file.split("_")[-1]
            if sufix1:
                return (report_file, sufix1)
            else:
                sufix1 = base_file + CommonOpt.generateRandomStr()
                return (os.path.join(dirname, sufix1), sufix1)
        else:
            sufix1 = CommonOpt.generateRandomStr()
            return (os.path.join('/tmp', sufix1), sufix1)

    def executeCMD(self, cmd, chk_posit=True, w_timeout=100, s_timeout=5,
                   title="Execute CMD",chk_reltime=True, times=1):

        for i in range(times):
            rel = self.ins_conslave.getResultFromCMD(cmd, handlespecialchar=True, w_timeout=w_timeout,
                                                     s_timeout=s_timeout, chk_reltime=chk_reltime)
            LOGGER.info("Return info : %s" %rel[1])
            exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())
            
            rel_msg = "\n[CMD] :%s\n" %cmd + '-'*80 + "\n%s" %rel[1]
            if rel[0] == 1 :
                rel1 = self.ins_conslave.getReturnCode()
                if chk_posit is True:
                    if rel1[0] is False:
                        rel1_msg = "Return code is non-zero, $? is [ %s]" %rel1[1]
                        LOGGER.warn(StringColor().printColorString(rel1_msg, StringColor.F_RED))
                        if i == times-1:
                            rel_msg = rel_msg + '\n' + rel1_msg
                            tc_data = self.combineTCData(tc_name='Run shell cmd', tc_status='failed', 
                                                         tc_duration=exec_duration, tc_output=rel_msg)
                            ts_data = self.combineTSData(ts_name=title, ts_tc_list=tc_data)
                            self._exit(ts_data)
                        else:
                            time.sleep(3)
                            continue
                    else:
                        LOGGER.info(
                                    StringColor().printColorString(
                                        "Return code $? is [ %s]" %rel1[1],
                                        StringColor.F_GRE))
                    return (rel1[0], rel[1])
                else:
                    if rel1[0] is False:
                        LOGGER.warn(
                                    StringColor().printColorString(
                                        "Return code is EXPECTED non-zero result , $? is [ %s]" %rel1[1],
                                        StringColor.F_BLU))
                        return (rel1[0], rel[1])
        
                    else:
                        LOGGER.info(
                                    StringColor().printColorString(
                                        "Return code is UNEXPECTED zero result, $? is [ %s]" %rel1[1],
                                        StringColor.F_RED))
                        if i == times-1:
                            tc_data = self.combineTCData(tc_name='Run shell cmd', tc_status='failed', 
                                                         tc_duration=exec_duration, tc_output=rel_msg)
                            ts_data = self.combineTSData(ts_name=title, ts_tc_list=tc_data)
        
                            self._exit(ts_data)
                        else:
                            time.sleep(3)
                            continue
            else:
                rel_msg = "Failed to get normal result when executes cmd %s, status:%d" %(cmd,rel[0])
                LOGGER.info(
                    StringColor().printColorString(rel_msg, StringColor.F_RED))
                if i == times-1:
                    tc_data = self.combineTCData(tc_name='Run shell cmd', tc_status='failed', 
                                                 tc_duration=exec_duration, tc_output=rel_msg)
                    ts_data = self.combineTSData(ts_name=title, ts_tc_list=tc_data)
                    self._exit(ts_data)
                else:
                    time.sleep(3)
                    continue

    def sshSlave(self, try_times=5, interval_time=10, show_kernel_ver=False):
        '''Wrap the re-installation host function
        '''
        LOGGER.info("Attempt to connect slave thru SSH.")

        # First connect slave server.
        status = self.ins_conslave.sshSlave(try_times=try_times, interval_time=interval_time)
        exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())
        if status:
            if show_kernel_ver:
                kernel_ver = self.executeCMD("uname -r")
                rel_msg = ('Successful connect to slave [%s]\n'
                           ' Kerver Version :%s' %(self.ins_conslave.slave_addr,
                                                    kernel_ver[1]))
            else:
                rel_msg = ('Successful connect to slave [%s]' %(self.ins_conslave.slave_addr))

            tc_data = self.combineTCData(tc_name="ssh to slave", tc_status='passed', 
                                         tc_duration=exec_duration, tc_output=rel_msg)
            ts_data = self.combineTSData(ts_name="Connect slave", ts_tc_list=tc_data)
            
            #rel_list = [{'name':"Connect slave", 'status':True, 'output':rel_msg, 'error_msg':None, 'url':None}]
            
            return ts_data
        else:
            rel_msg = "Failed to connect to slave, there is no way to re-install on the one slave"
            LOGGER.error(StringColor().printColorString(rel_msg, StringColor.F_RED | StringColor.HIGLIG))

            tc_data = self.combineTCData(tc_name="ssh to slave", tc_status='failed', 
                                         tc_duration=exec_duration, tc_output=rel_msg)
            ts_data = self.combineTSData(ts_name="Connect slave", ts_tc_list=tc_data)

            #rel_list = [{'name':"Connect slave", 'status':False, 'output':None, 'error_msg':rel_msg, 'url':None}]
            self._exit(ts_data)
            
    def warpTCandTSdata(self, display_msg, tc_name, tc_status, ts_name):
        exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())
        if tc_status == 'passed':
            LOGGER.info(StringColor().printColorString(display_msg, StringColor.F_GRE))
        else:
            LOGGER.info(
                StringColor().printColorString(display_msg, StringColor.F_RED))
        tc_data = self.combineTCData(tc_name=tc_name, tc_status=tc_status, 
                                     tc_duration=exec_duration, tc_output=display_msg)
        ts_data = self.combineTSData(ts_name=ts_name, ts_tc_list=tc_data)
        
        return ts_data

    def getValidURL(self,url):
        tmp_url = url
        if URLParser().checkURLPath(tmp_url, times=3):
            return tmp_url
        else:
            if 'DVD' in tmp_url:
                tmp_url = tmp_url.replace('DVD','dvd')
            elif 'dvd' in tmp_url:
                tmp_url = tmp_url.replace('dvd','DVD')
        if URLParser().checkURLPath(tmp_url, times=3):
            return tmp_url
        else:
            rel_msg = "Re-install tool failure, some repos do not exist!!"
            ts_data = self.warpTCandTSdata(rel_msg, 'Run shell cmd', 'failed', "Check re-installation tools")
            self._exit(ts_data)  

    def installRITools(self):
        #Install re-installation host tools
        chkinstall_tool_cmd = 'test -e /usr/share/qa/tools/install.pl'
        rel = self.ins_conslave.getResultFromCMD(chkinstall_tool_cmd, w_timeout=20, s_timeout=60)

        if rel[0] == 1 :
            rel1 = self.ins_conslave.getReturnCode()
            if rel1[0] is True:
                rel_msg = "Re-installation tool exists on slave"
                ts_data = self.warpTCandTSdata(rel_msg, 'Run shell cmd', 'passed', "Check re-installation tools")
                return ts_data
        else:
            rel_msg = "Failed to get normal result when executes cmd %s, status:%d" %(chkinstall_tool_cmd,rel[0])
            ts_data = self.warpTCandTSdata(rel_msg, 'Run shell cmd', 'failed', "Check re-installation tools")
            self._exit(ts_data)

        rel = self.executeCMD('cat /etc/issue', w_timeout=180, s_timeout=20, title="Get Os Info")
        
        local_os_info = CommonOpt().getOSPrdVerAndArch(rel[1])
        LOGGER.info(("local info ", local_os_info))
        
        qa_head_repo =  os.path.join(PREFIX_QA_HEAD_REPO, local_os_info[0])
                                     #PrjPath().getProductVersion().replace("SLES", "SLE"))
        qa_head_repo_nike = 'qa_head_' + str(random.randint(10000,99999))
        self.addRepo2Host(qa_head_repo, qa_head_repo_nike)

        if local_os_info[1] in self.larch:
            product_sdk_repo = PREFIX_PRODUCT_SDK_L_REPO
        else:
            product_sdk_repo = PREFIX_PRODUCT_SDK_R_REPO

        qa_prd_sdk_repo =  product_sdk_repo %dict(prd_name=local_os_info[0],
                                                  arch=local_os_info[1])
        '''
        qa_prd_sdk_repo =  PREFIX_PRODUCT_SDK_L_REPO %dict(prd_name=local_os_info[0],
                                                           arch=local_os_info[1])
        '''
            #prd_name=PrjPath().getProductVersion().replace("SLES", "SLE"),
            #arch=self.arch)
        qa_prd_sdk_repo_nike = 'qa_prd_sdk_' + str(random.randint(10000,99999))

        vaild_prd_sdk_repo = self.getValidURL(qa_prd_sdk_repo)
        if vaild_prd_sdk_repo:
            self.addRepo2Host(qa_prd_sdk_repo, qa_prd_sdk_repo_nike)       
        else:
            ret_msg = "Failed to get product sdk repo [%s]" %vaild_prd_sdk_repo
            
            ts_data = self.warpTCandTSdata(rel_msg, "Invalid product sdk repo", 'failed', "Add repo")

            self._exit(ts_data)

        self.installPKG(qa_head_repo_nike, 'qa_tools')

        self.executeCMD(chkinstall_tool_cmd, w_timeout=1800, s_timeout=20, title="Check re-installation tools")
        rel_msg = "Re-installation tool has been installed"
        ts_data = self.warpTCandTSdata(rel_msg, 'Run shell cmd', 'passed', "Check re-installation tools")
        return ts_data
        
    def installSlave(self, repo, w_timeout=1800, s_timeout=20):

        LOGGER.debug(URLParser().getValidURL(repo))
        reins_host_cmd = REINSTALL_MACHINE_CMD %dict(repo=self.getValidURL(repo))
        
        # File systerm btrfs is only used on SLE-12 and up version
        if 'SLE-12' in self.product:
            reins_host_cmd = reins_host_cmd + ' -f btrfs'
        
        LOGGER.info(StringColor().printColorString(
                    "Execute reinstallation host cmd. cmd :[%s]" %reins_host_cmd, StringColor.F_BLU))
        self.executeCMD(reins_host_cmd, w_timeout=1800, s_timeout=s_timeout, title="Reinstall slave")

        exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())

        ret_msg = "Successfully execute reinstallation cmd [%s]" %reins_host_cmd
        LOGGER.info(StringColor().printColorString(ret_msg, StringColor.F_BLU))

        tc_data = self.combineTCData(tc_name="Execute reinstallaiont cmd", tc_status='passed', 
                                     tc_duration=exec_duration, tc_output=ret_msg)
        ts_data = self.combineTSData(ts_name="Reinstall slave", ts_tc_list=tc_data)

        #rel_list = [{'name':"Reinstall slave", 'status':True, 'output':ret_msg, 'error_msg':None, 'url':None}]
        return ts_data

    def rebootSlave(self):
        reboot_cmd = "(sleep 3;reboot)&"
        LOGGER.info(StringColor().printColorString("Reboot host.", StringColor.F_BLU))
        self.executeCMD(reboot_cmd, w_timeout=180, s_timeout=20, title="Reboot slave")
        time.sleep(10)

        self.ins_conslave.closeSSH()
        exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())

        ret_msg = "Reboot finished, prepare to install host"
        LOGGER.info(StringColor().printColorString(ret_msg, StringColor.F_BLU))

        tc_data = self.combineTCData(tc_name="Execute reboot cmd", tc_status='passed', 
                                     tc_duration=exec_duration, tc_output=ret_msg)
        ts_data = self.combineTSData(ts_name="Reboot slave", ts_tc_list=tc_data)

        #rel_list = [{'name':"Reboot slave for reinstallation", 'status':True, 'output':ret_msg, 'error_msg':None, 'url':None}]
        return ts_data

    def addRepo2Host(self, qa_repo, repo_nike_name):
        #qa_repo = os.path.join(qa_repo, PrjPath().getProductVersion().replace("SLES", "SLE"))
        repo = self.getValidURL(qa_repo)
        LOGGER.info(StringColor().printColorString("Add repo to slave.", StringColor.F_BLU))
        addrepo_cmd = PREFIX_ADD_REPO_CMD %dict(repo_addr=repo,
                                                repo_nike=repo_nike_name)
        self.executeCMD(addrepo_cmd, w_timeout=1800, s_timeout=20, title='Add Repo')

        # Refresh repo 
        LOGGER.info(StringColor().printColorString("Refresh repo on slave.", StringColor.F_BLU))
        refrepo_cmd = PREFIX_REF_REPO_CMD %dict(repo_nike=repo_nike_name)
        self.executeCMD(refrepo_cmd, w_timeout=1800, s_timeout=20, title='Refresh Repo')

    def installPKG(self, repo_nike_name, package):

        LOGGER.info(StringColor().printColorString("Install package on slave.", StringColor.F_BLU))
        inpackage_cmd = PREFIX_INS_REPO_CMD %dict(#repo_nike=repo_nike_name,
                                                  ts_name=package)
        self.executeCMD(inpackage_cmd, w_timeout=1800, s_timeout=30, title="Install Package")

        # Collect data 
        exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())
        
        ret_msg = "Successfully install package [%s] on slave" %package
        LOGGER.info(StringColor().printColorString(ret_msg, StringColor.F_GRE))

        tc_data = self.combineTCData(tc_name="Install package %s" %package , tc_status='passed', 
                                     tc_duration=exec_duration, tc_output=ret_msg)
        ts_data = self.combineTSData(ts_name="Install Packages", ts_tc_list=tc_data)

        #rel_list = [{'name':"Install package", 'status':True, 'output':ret_msg, 'error_msg':None, 'url':None}]
        return ts_data

    def installPackage(self, qa_repo, package=TS_STRESS_VALID_NAME, times=3):
        
        # Add repo to zypper 
        #self.addRepo2Host(qa_repo)
        #qa_repo = os.path.join(qa_repo, PrjPath().getProductVersion().replace("SLES", "SLE"))
        
        qa_repo = os.path.join(qa_repo, self.productv)
        LOGGER.info(StringColor().printColorString("Add repo to slave.", StringColor.F_BLU))
        addrepo_cmd = PREFIX_ADD_REPO_CMD %dict(repo_addr=qa_repo,
                                                repo_nike=TS_STRESS_VALID_NICK)
        self.executeCMD(addrepo_cmd, w_timeout=1800, s_timeout=20, title='Add Repo')

        # Refresh repo 
        LOGGER.info(StringColor().printColorString("Refresh repo on slave.", StringColor.F_BLU))
        refrepo_cmd = PREFIX_REF_REPO_CMD %dict(repo_nike=TS_STRESS_VALID_NICK)
        self.executeCMD(refrepo_cmd, w_timeout=1800, s_timeout=20, title='Refresh Repo', times=times)

        # Install package
        LOGGER.info(StringColor().printColorString("Install package on slave.", StringColor.F_BLU))
        inpackage_cmd = PREFIX_INS_REPO_CMD %dict(repo_nike=TS_STRESS_VALID_NICK,
                                                  ts_name=package)
        self.executeCMD(inpackage_cmd, w_timeout=1800,
                        s_timeout=30, title="Install Qaset Package", times=times)

        # Collect data 
        exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())
        
        ret_msg = "Successfully install package [%s] on slave" %package
        LOGGER.info(StringColor().printColorString(ret_msg, StringColor.F_GRE))

        tc_data = self.combineTCData(tc_name="Installtestset package", tc_status='passed', 
                                     tc_duration=exec_duration, tc_output=ret_msg)
        ts_data = self.combineTSData(ts_name="Install Packages", ts_tc_list=tc_data)

        #rel_list = [{'name':"Install package", 'status':True, 'output':ret_msg, 'error_msg':None, 'url':None}]
        return ts_data

    def cleanFolder(self, folder, prefix='', postfix=''):
        cln_files_cmd = 'rm -rf %s/*' %(folder)
        LOGGER.info(StringColor().printColorString(
            "Clean files . CMD:[%s]" %cln_files_cmd, StringColor.F_BLU))
        self.executeCMD(cln_files_cmd, w_timeout=1800, s_timeout=20, title='Clean Test Env')
        exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())

        ret_msg = "All files are removed under folder %s successfully" %folder
        LOGGER.info(StringColor().printColorString(ret_msg,  StringColor.F_GRE))

        tc_data = self.combineTCData(tc_name="Execute rm cmd", tc_status='passed', 
                                     tc_duration=exec_duration, tc_output=ret_msg)
        ts_data = self.combineTSData(ts_name="Clean Test Env", ts_tc_list=tc_data)
        
        #rel_list = [{'name':"Execute Test Suite", 'status':True, 'output':ret_msg, 'error_msg':None, 'url':None}]
        return ts_data        

    def genRTConfig(self, testsuites):
        
        gen_rt_cfg_cmd = '''mkdir -p /root/qaset/;echo -e "SQ_TEST_RUN_LIST=(" > /root/qaset/list'''
        self.executeCMD(gen_rt_cfg_cmd, w_timeout=600, s_timeout=30, title="Generate Test Suites")

        self.executeCMD('echo -e "    _reboot_off" >> /root/qaset/list', w_timeout=600,
                        s_timeout=30, title="Generate Test Suites")
        for testsuite in testsuites.split(","):
            add_ts_cmd = '''echo -e "    %s" >> /root/qaset/list''' %testsuite
            self.executeCMD(add_ts_cmd, w_timeout=600, s_timeout=30, title="Generate Test Suites")

        self.executeCMD("echo -e \")\" >> /root/qaset/list", w_timeout=600, s_timeout=30, title="Generate Test Suites")

        exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())

        ret_msg = "Successfully generate special testsuites list."
        LOGGER.info(StringColor().printColorString(ret_msg, StringColor.F_BLU))

        tc_data = self.combineTCData(tc_name="Generate special test suites", tc_status='passed', 
                                     tc_duration=exec_duration, tc_output=ret_msg)
        ts_data = self.combineTSData(ts_name="Generate Test Suites", ts_tc_list=tc_data)

        #rel_list = [{'name':"Reinstall slave", 'status':True, 'output':ret_msg, 'error_msg':None, 'url':None}]
        return ts_data
    
    def executeTS(self, reset_cmd=TS_QASET_RESET_CMD, ts_run=TS_STRESS_VALID_RUN_NAME,
                  flow_file=TS_STRESS_VALID_MONITOR_FILE, timeout=20):

        # Clean unnecessary files
        self.cleanFolder(folder=TS_STRESS_VALID_SUBMISSION_FOLDER)
        self.cleanFolder(folder=TS_STRESS_VALID_RUNS_FOLDER)

        for i in range(0,3):
            # Reset test environment
            LOGGER.info(StringColor().printColorString(
                "Reset running environment. CMD:[%s]" %reset_cmd, StringColor.F_BLU))
            self.executeCMD(reset_cmd, w_timeout=1800, s_timeout=20, title='Reset Test Env')
    
            # Run test suite run
            LOGGER.info(StringColor().printColorString(
                "Execute Test Suite Run. CMD:[%s]" %ts_run, StringColor.F_BLU))
            self.executeCMD(ts_run, w_timeout=1800, s_timeout=20, title="Execute TestSuite")
    
            '''
            # Check test suite process
            chktsproc_cmd = "cat %s" %flow_file
            LOGGER.info(StringColor().printColorString(
                "Monitor testsuite process. CMD:[%s]" %chktsproc_cmd, StringColor.F_BLU))
            self.executeCMD(chktsproc_cmd, w_timeout=1800, s_timeout=20, title="Execute TestSuite")
            '''
            # Check test suite process    
            chktsproc_cmd = "screen -ls"
            LOGGER.info(StringColor().printColorString(
                "Monitor testsuite process. CMD:[%s]" %chktsproc_cmd, StringColor.F_BLU))
            rel = self.executeCMD(chktsproc_cmd, chk_posit=False, w_timeout=1800,
                                  s_timeout=20, title="Check script process")
            
            tc_run_name = os.path.basename(ts_run).split("-")[0]
            exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())
            if re.search(tc_run_name, rel[1]):
                ret_msg = "Test suite [%s] has been running on slave" %ts_run
                tc_status = 'passed'
                break
            else:
                ret_msg = "Test suite [%s] is not run on slave" %ts_run
                tc_status = 'failed'
                LOGGER.info(StringColor().printColorString("Faild to launch up test script, re-try again", StringColor.F_GRE))
        LOGGER.info(StringColor().printColorString(ret_msg,  StringColor.F_GRE))

        tc_data = self.combineTCData(tc_name="Execute testsuite run", tc_status=tc_status, 
                                     tc_duration=exec_duration, tc_output=ret_msg)
        ts_data = self.combineTSData(ts_name="Run TestSuite", ts_tc_list=tc_data)
        
        if tc_status == 'failed':
            self._exit(ts_data)
        else:
        #rel_list = [{'name':"Execute Test Suite", 'status':True, 'output':ret_msg, 'error_msg':None, 'url':None}]
            return ts_data
        '''
        s_time = time.time()
        while time.time() - s_time < timeout:
            rel = self.executeCMD(chktsproc_cmd, w_timeout=1800, s_timeout=20, title='Check TS-run Done')    
            if not rel[1].strip():
                time.sleep(2)
                continue
            else:
                exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())
                ret_msg = "Test suite [%s] has been running on slave" %ts_run
                LOGGER.info(StringColor().printColorString(ret_msg,  StringColor.F_GRE))

                tc_data = self.combineTCData(tc_name="Execute testsuite run", tc_status='passed', 
                                             tc_duration=timeout, tc_output=ret_msg)
                ts_data = self.combineTSData(ts_name="Run TestSuite", ts_tc_list=tc_data)
                
                #rel_list = [{'name':"Execute Test Suite", 'status':True, 'output':ret_msg, 'error_msg':None, 'url':None}]
                return ts_data

        ret_msg = "CMD:[%s] return empty, test suite [%s] is not started normally"  %(chktsproc_cmd, ts_run)
        LOGGER.error(StringColor().printColorString(ret_msg, StringColor.F_RED))

        tc_data = self.combineTCData(tc_name="Execute testsuite run", tc_status='failed', 
                             tc_duration=timeout, tc_output=ret_msg)
        ts_data = self.combineTSData(ts_name="Run TestSuite", ts_tc_list=tc_data)

        #rel_list = [{'name':None, 'status':False, 'output':None, 'error_msg':"", 'url':None}]
        self._exit(ts_data)
        '''

    def checkScreen(self, screen_name, times=3):
        for i in range(times):
            chktsproc_cmd = "screen -ls"
            LOGGER.info(StringColor().printColorString(
                "Monitor testsuite process. CMD:[%s]" %chktsproc_cmd, StringColor.F_BLU))
            rel = self.ins_conslave.getResultFromCMD(chktsproc_cmd, w_timeout=1800, s_timeout=30)
            if rel[0] == 1:
                #tc_run_name = os.path.basename(screen_name).split("-")[0]
                LOGGER.info(rel[1])
                exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())
                if re.search(screen_name, rel[1]):
                    ret_msg = "Test suite is running"
                    tc_status = 'passed'
                    LOGGER.info(StringColor().printColorString(ret_msg,  StringColor.F_GRE))
                    break
                else:
                    LOGGER.info(StringColor().printColorString("This test is dropped down or can not be launched, try again", StringColor.F_GRE))
            time.sleep(60)
        else:
            exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())
            tc_status = 'failed'
            ret_msg = "Test suite is not launched successfully, due to no screen"
            LOGGER.info(StringColor().printColorString(ret_msg,  StringColor.F_GRE))

        tc_data = self.combineTCData(tc_name="Check TestSuite Screen", tc_status=tc_status, 
                                         tc_duration=exec_duration, tc_output=ret_msg)
        ts_data = self.combineTSData(ts_name="Check TestSuite Run", ts_tc_list=tc_data)

        return (tc_status == 'passed' and True or False, ts_data)

    def checkFile(self, ts_run, file_name=TS_STRESS_VALID_DONE_FILE, allow_reboot=True,
                  timeout=10, interval_time=10, ept_times=20):

        exception_times = ept_times
        tc_run_name = os.path.basename(ts_run).split("-")[0]

        chkTSstatus_cmd = "test -e %s" %file_name
        LOGGER.info(StringColor().printColorString(
            "Check test suite running status. CMD:[%s]" %chkTSstatus_cmd, StringColor.F_BLU))

        s_time = time.time()
        while time.time() - s_time < timeout:
            rel = self.checkScreen(tc_run_name)
            if rel[0] is False:
                return rel[1]
            else:
                rel = self.ins_conslave.getResultFromCMD(chkTSstatus_cmd, w_timeout=20, s_timeout=60)
                exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())
                if rel[0] == 1 :
                    rel1 = self.ins_conslave.getReturnCode()
                    if rel1[0] is False:
                        time.sleep(interval_time)
                        continue
                    elif rel1[0] is None:
                        self.sshSlave(try_times=15, interval_time=20)
                    else:
                        ret_msg = "Test suite [%s] done on slave" %TS_STRESS_VALID_RUN_NAME
                        LOGGER.info(StringColor().printColorString(ret_msg, StringColor.F_BLU))
    
                        tc_data = self.combineTCData(tc_name="Inspect testsuite process", tc_status='passed', 
                                                     tc_duration=exec_duration, tc_output=ret_msg)
                        ts_data = self.combineTSData(ts_name="Check testsuite done", ts_tc_list=tc_data)
    
                        #rel_list = [{'name':"Verify result file", 'status':True, 'output':ret_msg, 'error_msg':None, 'url':None}]
                        return ts_data
                elif rel[0] == 0:
                    self.sshSlave(try_times=15, interval_time=20)
                else:
                    if exception_times > 0:
                        time.sleep(interval_time)
                        exception_times = ept_times - 1
                    else:
                        LOGGER.error(StringColor().printColorString(("Failed to get normal result "
                                                                   "when executes cmd %s" %chkTSstatus_cmd),
                                                                    StringColor.F_RED))                
                        tc_data = self.combineTCData(tc_name="Inspect testsuite process", tc_status='failed', 
                                                     tc_duration=exec_duration, tc_output=rel[1])
                        ts_data = self.combineTSData(ts_name="Check testsuite done", ts_tc_list=tc_data)
        
                        #rel_list = [{'name':"Verify result file", 'status':False, 'output':None, 'error_msg':rel[1], 'url':None}]
                        exit(ts_data)
    
        to_msg = "Test suite did not complete whole test within %ds !" %timeout
        LOGGER.error(StringColor().printColorString(to_msg, StringColor.F_RED))

        tc_data = self.combineTCData(tc_name="Inspect testsuite process timeout", tc_status='failed', 
                                     tc_duration=timeout, tc_output=to_msg)
        ts_data = self.combineTSData(ts_name="Check testsuite done timeout", ts_tc_list=tc_data)
        #rel_list = [{'name':"Verify result file", 'status':False, 'output':None, 'error_msg':to_msg, 'url':None}]
        return ts_data
        #exit(ts_data) 

    def getQadbRUL(self, file_name):

        get_submissionid_cmd = TS_GET_SUBMISSION_ID_CMD %file_name
        LOGGER.info(StringColor().printColorString(
            "Get submission id. CMD:[%s]" %get_submissionid_cmd, StringColor.F_BLU))

        rel = self.ins_conslave.getResultFromCMD(get_submissionid_cmd, 
                                                 handlespecialchar=True,
                                                 w_timeout=50, s_timeout=60)
        LOGGER.info(StringColor().printColorString(
            "Submission id is :[%s]" %rel[1], StringColor.F_BLU))        
        rel_msg = "\n[CMD] :%s\n" %get_submissionid_cmd + '-'*80 + "\n%s" %rel[1]
        exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())
        ts_submission_url = ''
        if rel[0] == 1:
            ts_submission_url = rel[1]
        else:
            ret_msg = "Failed to get normal result when executes cmd %s, status:%d" %(get_submissionid_cmd,rel[0])
            LOGGER.info(StringColor().printColorString(ret_msg, StringColor.F_RED))
            tc_data = self.combineTCData(tc_name="Inspect testsuite process", tc_status='failed', 
                                         tc_duration=exec_duration, tc_output=rel_msg)
            ts_data = self.combineTSData(ts_name="Check testsuite done", ts_tc_list=tc_data)
            #rel_list = [{'name':"Get QADB URL", 'status':False, 'output':None, 'error_msg':rel_msg, 'url':None}]
            self._exit(ts_data)

        ts_submission_url = CommonOpt().getSubmissionIDFromString(ts_submission_url)
        return ts_submission_url
    
    def traverseFiles(self, folder=TS_STRESS_VALID_SUBMISSION_FOLDER, postfix="log"):
           
        get_file_cmd = "ls %s*.%s" %(folder, postfix)
        LOGGER.info(StringColor().printColorString(
                        "Get test suite running status. CMD:[%s]" %get_file_cmd,
                        StringColor.F_BLU))
        rel = self.executeCMD(get_file_cmd, w_timeout=1800, s_timeout=20, title='Traverse Log')

        file_list = re.split("\s+", rel[1])
        return file_list

        '''
        for submission_log in submissionlog_list:
            ts_name = CommonOpt().getTSName(submission_log)
            LOGGER.info(StringColor().printColorString(
                "Get Test suite name :[%s]" %ts_name, StringColor.F_BLU))
            ts_submission_url = self.getQadbRUL(submission_log)
            tmp_submission_info = {'name':ts_name, 'status':True, 'output':None, 'error_msg':None, 'url':ts_submission_url}
            tmp_ts_info_list.append(tmp_submission_info)
        
        return tmp_ts_info_list
        '''

    def combineTCData(self, tc_name='tc', step_desc='', tc_status='passed',
                      tc_output=None, tc_url=None, tc_duration=0,):
        tmp_data_map = {}

        tmp_data_map['tc_name'] = tc_name
        tmp_data_map['step_desc'] = step_desc
        tmp_data_map['tc_status'] = tc_status == "timeout" and "failed" or tc_status
        tmp_data_map['tc_output'] = tc_output
        tmp_data_map['tc_url'] = tc_url
        tmp_data_map['tc_duration'] = tc_duration
        
        return [tmp_data_map]

    def combineTSData(self, ts_name='ts', ts_tc_list=[], ts_tags=None, ts_url=None):

        tmp_data_map = {}
        passed_tc_num = failed_tc_num = skipped_tc_num = 0
        tmp_data_map['ts_name'] = ts_name
        tmp_data_map['ts_tc_list'] = ts_tc_list
        tmp_data_map['ts_tags'] = ts_tags
        tmp_data_map['ts_url'] = ts_url
        LOGGER.debug(("TS_list", ts_tc_list))
        if ts_tc_list:
            passed_tc_num = len(filter(lambda x: re.search('passed',x['tc_status'], re.I), ts_tc_list)) / float(len(ts_tc_list))
            failed_tc_num = len(filter(lambda x:re.search('(failed|timeout)',x['tc_status'],re.I), ts_tc_list)) / float(len(ts_tc_list))
            skipped_tc_num = len(filter(lambda x:re.search('skipped', x['tc_status'], re.I), ts_tc_list)) / float(len(ts_tc_list))

        tmp_data_map['ts_rate'] = ('Passed:%0.2f%%,' %(100 * passed_tc_num) + 
                                   'Failed:%0.2f%%,' %(100 * failed_tc_num) +
                                   'Skillped:%0.2f%%,' %(100 * skipped_tc_num))

        return [tmp_data_map]

    def getTestCaseInfo(self, file_name):

        def _convertTime(str_time="0h0m0s"):
            hour_num = min_num = sec_num = 0
            if 'h' in str_time:
                hour_num = re.search("(\d+)h", str_time).groups()[0]
            if 'm' in str_time:
                min_num = re.search("(\d+)m", str_time).groups()[0]
            if 's' in str_time:
                sec_num = re.search("(\d+)s", str_time).groups()[0]
            total_sec = int(hour_num) * 3600 + int(min_num) * 60 + int(sec_num)
            return total_sec

        tc_info_list = []
        
        get_tc_content_cmd = 'sed -n "/Test in progress/,/Test run complete/p" %s | sed "s:36m.*\[K::g\" | cat' %file_name
        #get_tc_content_cmd = 'grep -P "\[\d+/\d+\]\s+\S+\s+" %s' %file_name
        LOGGER.info(StringColor().printColorString(
                        "Get file content. CMD:[%s]" %get_tc_content_cmd,
                        StringColor.F_BLU))
        rel = self.executeCMD(get_tc_content_cmd, w_timeout=18000, s_timeout=60, chk_reltime=False)

        case_cont_compile = re.compile(
            ("(\[\s*\d+/\d+\]\s+\S+).*(passed|failed|skipped|timeout).*\((\S*)\)"),re.I)

        case_result_list = re.findall(case_cont_compile, rel[1])

        for tc in case_result_list:
            tc_duration = _convertTime(tc[2])
            tc_info_list.extend(self.combineTCData(tc_name=tc[0],
                                                   tc_status=tc[1].lower(),
                                                   tc_duration=tc_duration))
        return tc_info_list

    def getTestSuiteInfo(self, rel_folder='/var/log/qaset/runs/', rel_file_postfix='screenlog',
                         sub_mission_prefix='submission-%s.log', sub_mission_folder=TS_STRESS_VALID_SUBMISSION_FOLDER):
        base_name = ''
        ts_name = ''
        sub_tc_info = []
        ts_qadb_url = ''
        ts_info = []

        file_list = self.traverseFiles(folder=rel_folder, postfix=rel_file_postfix)
        for f in file_list:
            base_name = os.path.basename(f)
            ts_name = '-' in base_name and base_name.split("-")[0] or base_name
            submission_file = os.path.join(sub_mission_folder, sub_mission_prefix %(ts_name))
            
            sub_tc_info = self.getTestCaseInfo(f)
            ts_qadb_url = self.getQadbRUL(submission_file)
            ts_info.extend(self.combineTSData(ts_name=ts_name, ts_tc_list=sub_tc_info, ts_url=ts_qadb_url))

        return ts_info

    def chkCurrBuildCause(self):
        build_api_json = PrjPath().getBuildURL() + '/api/json'
        LOGGER.debug(build_api_json)
        try:
            req = urlopen(build_api_json)
            res = req.read()
            data = json.loads(res)
            
            for act in data['actions']:
                if 'causes' in act:
                    for cau in act['causes']:
                        if 'shortDescription' in cau:
                            if re.search('Started by user', cau['shortDescription'], re.I):
                                return True
                            else:
                                return False
        except HTTPError, e:
            LOGGER.warn(StringColor().printColorString(
                                    "Failed to access website ,cause [%s]" %e,
                                    StringColor.F_RED))
            return False
        return False

    def createJsonFile(self, rel, flg='1vn'):

        #scen_data = []
        lastscen_data = []
        # Generate json file for cucumber report
        json_file = os.path.join(PrjPath().getWorkSpace(),
                                 "result.json")
        ins_jg = JsonGenerator(json_file)
        
        #dump_file_name = PREFIX_STORE_FILE_NAME %self.arch
        abs_file_path = self.report_pkl_file
        '''
        abs_file_path = os.path.join(PrjPath().getArchLevelPath(),
                                     dump_file_name)
        '''
        LOGGER.debug("PKL file %s" %abs_file_path)
        # Get dump data file path
        '''
        if self.chkCurrBuildCause() is True:
            os.path.exists(abs_file_path) and os.remove(abs_file_path)
        else:
            lastscen_data = CommonOpt().loadData(abs_file_path)
        '''
        lastscen_data = CommonOpt().loadData(abs_file_path)
        # Analyze data and generate json file
        for i in rel:
            scen_name = i['ts_name']
            scen_step = i['ts_tc_list']
            scen_url = i['ts_url']
            scen_tags = i['ts_tags']
            scen_rate = i['ts_rate']

            for j in scen_step:
                LOGGER.debug(j)
                step_name = j['tc_name']
                step_url = j['tc_url']
                step_status = j['tc_status']
                step_duration = j['tc_duration']
                step_desc = j['step_desc']

                if step_status == 'passed':
                    step_err_msg = None
                    step_output = j['tc_output']
                else:
                    step_err_msg = j['tc_output']
                    step_output = None

                ins_jg.addStep(step_keyword="Test case: ", step_name=step_name, step_url=step_url,
                               step_status=step_status, step_duration=step_duration, step_desc=step_desc,
                               step_err_msg=step_err_msg, step_output=step_output)
            ins_jg.addScenario(scen_name=scen_name, scen_url=scen_url, 
                               scen_tags=scen_tags, scen_step=ins_jg.step_data)
            if flg == '1vn':
                pass
            elif flg == '1v1':
                format_str = '[{0}] - [TSuite: {1:<15}] - Arch:{2} for {3}'
                feat_name = format_str.format(self.prefix_feat_name,
                                              scen_name,
                                              self.arch.upper(),
                                              self.productv)
                                              #PrjPath().getProductVersion())
                feat_desc = self.feat_desc + '\n\nStatus Rate: %s' %scen_rate
                ins_jg.addFeature(feat_name=feat_name, 
                                  feat_desc=feat_desc,
                                  feat_elements=ins_jg.scen_data)
                ins_jg.setEmpty2StepData()
                ins_jg.setEmpty2ScenData()

        #scen_data.extend(ins_jg.scen_data)
        if flg == '1vn':
            format_str = '[{0}] - Arch:{1} for {2}'
            feat_name = format_str.format(self.prefix_feat_name,
                                          self.arch.upper(),
                                          self.productv)
                                          #PrjPath().getProductVersion())

            ins_jg.addFeature(feat_name=feat_name, 
                              feat_desc=self.feat_desc, feat_elements=ins_jg.scen_data)
        lastscen_data.extend(ins_jg.feat_data)
        ins_jg.generateJsonFile(json_file, lastscen_data)
        LOGGER.debug("Json file is %s" %self.report_json_file)
        ins_jg.generateJsonFile(self.report_json_file, lastscen_data)
        
        # Store data  to local disk
    
        CommonOpt().dumpData(abs_file_path, lastscen_data)

    def _exit(self, rel, flg='1vn'):

        return_code = 0
        self.createJsonFile(rel, flg)
       
        #Traverse test case info , "failed" status in any test case, will cause exit with non-zeron value
        for ts in rel:
            for tc in ts['ts_tc_list']:
                if tc['tc_status'] != 'passed':
                    return_code = 1
                    break
            if return_code == 1:
                break
        
        if self.ins_conslave.ssh is not None:
            #LOGGER.debug(self.ins_conslave.ssh.isalive())
            self.ins_conslave.closeSSH()

        if JenkinsAPI().checkCauseType(PrjPath().getBuildURL()) is True:
            LOGGER.debug("This build is caused by other job triggering automatically")
            '''
            if JenkinsAPI().checkDownStreamProject(PrjPath().getJobURL()) is False:
                LOGGER.info("This build\'s downstream job is unexistent or disable")
                HostContorller().freeHost(self.ins_conslave.slave_addr, HOST_STATUS_FILE, self.report_file)
            else:
                LOGGER.info("This build\'s downstream job is enable")
            '''
            if return_code == 1:
                if self.prefix_feat_name not in ['US','KR']:
                    LOGGER.debug('free host')
                    HostContorller().freeHost(self.ins_conslave.slave_addr, HOST_STATUS_FILE, self.report_file)
                else:
                    HostContorller().releaseHost(self.ins_conslave.slave_addr, HOST_STATUS_FILE, self.report_file)
            else:
                HostContorller().releaseHost(self.ins_conslave.slave_addr, HOST_STATUS_FILE, self.report_file)
        else:
            LOGGER.debug("This build is caused by user in manual")
            HostContorller().freeHost(self.ins_conslave.slave_addr, HOST_STATUS_FILE,self.report_file)
            '''
            if return_code == 1:
                if self.prefix_feat_name not in ['US','KR']:
                    HostContorller().releaseHost(self.ins_conslave.slave_addr, HOST_STATUS_FILE, self.report_file)
            '''
        LOGGER.debug("FIle path is %s" %HOST_STATUS_FILE)              

        LOGGER.info(StringColor().printColorString("---------Test End -----------"  ,
                                                   StringColor.HIGLIG))
        sys.exit(return_code)

class Install_Kernel(QA_TESTSET):
    
    def __init__(self, options, feat_info, pkg_name):
        
        self.kotd_productv = options.kotd_productv
        self.kotd_arch = options.kotd_arch
        self.kotd_mach = options.kotd_mach
        self.kotd_report = options.kotd_report
        self.kotd_kelrepo = options.kotd_kernelrepo
        self.kotd_kernel = options.kotd_kernel
        
        super(Install_Kernel, self).__init__(self.kotd_productv, self.kotd_arch, 
                                             self.kotd_mach, self.kotd_report, feat_info)
        self.pkg_name = pkg_name
    
    def getKernelPkgName(self, repo, pkg_prefix="kernel-default", times=3):

        while times -1 > 0:
            try:
                req = urlopen(repo)
                res = req.read()
                ins_s =  re.search('%s-\S+.rpm' %'kernel-default', res)
                
                if ins_s:
                    return ins_s.group().strip().replace('.rpm','')
                else:
                    return pkg_prefix
                
            except HTTPError, e:
                LOGGER.warn(StringColor().printColorString(
                                        "Failed to access website %s ,cause [%s]" %(repo,e),
                                        StringColor.F_RED))

            except Exception, e:
                LOGGER.warn(StringColor().printColorString(
                                    "Failed to get kernel pkg name thru %s ,cause [%s]" %(repo,e),
                                    StringColor.F_RED))
        return pkg_prefix
    
    def checkKernelVer(self, pkg_full_name):
        rel = self.executeCMD("uname -mrsn")
        
        kernel_name = self.pkg_name.replace('kernel-','')
        
        ins_s = re.search("%s-(\S+).rpm" %self.pkg_name, pkg_full_name)
        if ins_s:
            kernel_ver = ins_s.group()
        else:
            kernel_ver =  ''
        
        rel = self.executeCMD("uname -r")
        
        ret_smg = "New Kernel verion :[%s]" %rel[1]
        
        if re.search('%s-%s'%(kernel_ver, kernel_name), rel[1], re.I):
            return (True, ret_smg)
        else:
            return (False, ret_smg)

    def installPackage(self, qa_repo, package=TS_STRESS_VALID_NAME):
        
        # Get Original os version
        org_rel = self.executeCMD("uname -r",  w_timeout=120, s_timeout=20,
                                  title="Get kernel version", chk_reltime=True)
        
        # Add repo to zypper        
        LOGGER.info(StringColor().printColorString("Add repo to slave.", StringColor.F_BLU))
        addrepo_cmd = PREFIX_ADD_REPO_CMD %dict(repo_addr=qa_repo,
                                                repo_nike=KTOD_KERNEL_VALID_NICK)
        self.executeCMD(addrepo_cmd, w_timeout=1800, s_timeout=360, title='Add Repo')

        # Refresh repo 
        LOGGER.info(StringColor().printColorString("Refresh repo on slave.", StringColor.F_BLU))
        refrepo_cmd = PREFIX_REF_REPO_CMD %dict(repo_nike=KTOD_KERNEL_VALID_NICK)
        self.executeCMD(refrepo_cmd, w_timeout=3600, s_timeout=1800, title='Refresh Repo')

        # Install package
        LOGGER.info(StringColor().printColorString("Install package on slave.", StringColor.F_BLU))
        inpackage_cmd = PREFIX_INS_REPO_CMD %dict(repo_nike=KTOD_KERNEL_VALID_NICK,
                                                  ts_name=package)
        rel = self.executeCMD(inpackage_cmd, w_timeout=4800, s_timeout=3600, title="Install Kernel Package")

        # Collect data
        if re.search('The highest available version is already installed', rel[1], re.I):
            rel = self.executeCMD("uname -r",  w_timeout=120, s_timeout=20,
                                  title="Get kernel version", chk_reltime=True)
            ret_msg = "The highest available version is already installed. kerver version is [%s]" %rel[1]
            continue_flg = False
        else:
            ret_msg = "Successfully install package [%s] on slave" %package
            continue_flg = True
        exec_duration = CommonOpt().getDiffTime(self.start_time, datetime.datetime.now())
        
        LOGGER.info(StringColor().printColorString(ret_msg, StringColor.F_GRE))

        tc_data = self.combineTCData(tc_name="Installtestset package", tc_status='passed', 
                                     tc_duration=exec_duration, tc_output=ret_msg)
        ts_data = self.combineTSData(ts_name="Install Packages", ts_tc_list=tc_data)

        #rel_list = [{'name':"Install package", 'status':True, 'output':ret_msg, 'error_msg':None, 'url':None}]
        return (continue_flg, ts_data, org_rel[1])