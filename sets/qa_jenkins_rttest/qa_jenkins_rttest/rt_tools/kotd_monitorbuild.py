#!/usr/bin/python
"""
****************************************************************************
Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.

THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
LIABILITY.

SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
****************************************************************************

Tool Brief:
  Description: Execute stree validation test on host machine
"""

from  pylib.constantvars import *
from  pylib import StringColor as StringClor
from  pylib import CMDParamParser as ParseParam
from  pylib import RegConfigParser as ParseConfig
from  pylib import URLParser, HostContorller
from  pylib import JenkinsAPI


class RTBuildChange(object):
    def __init__(self, options):
        
        pc = ParseConfig()
        
        # Get project project name, host list, archs repo and so on
        self.prj_name = options.kotdmb_prj.upper()
        self.hosts = pc.convertItem(pc.getItem(KOTD_REF_TEST_CFG_FILE, self.prj_name, 'host'))

        self.arch = pc.convertItem(pc.getItem(KOTD_REF_TEST_CFG_FILE, self.prj_name, 'arch'))
        self.repo = os.path.join(options.kotdmb_repo, CommonOpt().convertPrjNameI(self.prj_name))
        
        # Get folder contains all relevant files
        self.prj_cfg_path = KOTD_PRJ_CONFIG_PATH

        self.repo_store_path = PrjPath().createFolder(
                                os.path.join(self.prj_cfg_path, 'kotd_repo', self.prj_name))
        self.host_status_file = HOST_STATUS_FILE
        self.rdy_tirgger_job_file = os.path.join(self.prj_cfg_path, KOTD_RDY_TRIGGER_JOB_FILE)

        # Initial jenkins jobs and triggered cmd
        self.jenkins_job = "curl -X POST --user admin:susetesting \"" + os.path.dirname(PrjPath().getJobURL()[:-1])  + "/%(arch)s/buildWithParameters?ARCH=%(arch)s&BUILD_VER=%(build_ver)s&KERNEL_NAME=%(kernel_name)s&REPORT_FILE=%(report_file)s&MACHINE="
        
        self.triggered_arch = ""
        self.return_code = 1
        
        # Instance for url operation and host controller
        self.urlpaser = URLParser()
        self.flowctrller = HostContorller()

    def loopCheckBuildChange(self):
        '''Traverse needed arches and mode for build change
        '''
        for arch in self.arch:
            LOGGER.info("Current arch is  %s" %(arch))
            
            # Get build change information
            bc = self.getBuildChange(arch)
            LOGGER.info(bc)
            if bc[2] == "":
                LOGGER.warn("Can not get build infomation, skip !!")
                continue
            #bc = (True, 'kernel-default-24983947dffdsf.rpm', '>kernel-default-24983947dffdsf.rpm<')
            
            for mode in (arch in self.hosts and self.hosts[arch].keys() or []):
                trigger_job_cmd = ''

                # Get stored data from local file
                cmd_triggerjob_map = CommonOpt().loadData(self.rdy_tirgger_job_file) or {}
                LOGGER.info("Current mode is  %s" %(mode))
                build_version = self.getBuildVersion(bc[2], mode)

                # Check jenkins job if is enable
                #enable_job_name = self.getEnableJenkinsJob(arch, build_version, 'kernel-%s'%(mode))
                key_name_tirgger_job = '%s_%s_%s' %(self.prj_name, arch, mode)
                # If build change is existent, followint operation will be done
                if bc[0] is True:
                    report_file = CommonOpt.generateRandomStr()
                    trigger_job_cmd = self.jenkins_job %dict(arch=arch,
                                                             build_ver=build_version,
                                                             kernel_name='kernel-%s' %(mode),
                                                             report_file=report_file)
                    LOGGER.info("BC:Detect build change")

                    '''
                    if  enable_job_name:
                        trigger_job_cmd = "wget -O - -q \"%s" %enable_job_name
                        cmd_triggerjob_map[key_name_tirgger_job] = ""
                    else:
                        LOGGER.info(StringClor().printColorString(
                                    "There is no enable job for build change triggering",
                                    StringClor.F_GRE))
                        cmd_triggerjob_map[key_name_tirgger_job] = enable_job_name
                    '''
                    #Dump data to local file which it's convenients for next trigger 
                    #CommonOpt().dumpData(self.rdy_tirgger_job_file, cmd_triggerjob_map)
                
                # BUild change is non-existent
                elif bc[0] is False:
                    if key_name_tirgger_job in cmd_triggerjob_map and cmd_triggerjob_map[key_name_tirgger_job]:
                        trigger_job_cmd = cmd_triggerjob_map[key_name_tirgger_job]
                        LOGGER.info(StringClor().printColorString(
                                    "No build change, Try to tirgger last build change with job cmd : %s" %trigger_job_cmd,
                                    StringClor.F_GRE))

                        cmd_triggerjob_map[key_name_tirgger_job]=""
                        CommonOpt().dumpData(self.rdy_tirgger_job_file, cmd_triggerjob_map)
                    else:
                        LOGGER.info(StringClor().printColorString(
                                    "No build change or last build change needs to be triggered",
                                    StringClor.F_GRE))
                    '''
                    if enable_job_name:
                        # If last build change is existent, the job should be tiggered
                        if key_name_tirgger_job in cmd_triggerjob_map and cmd_triggerjob_map[key_name_tirgger_job]:
                            trigger_job_cmd = cmd_triggerjob_map[key_name_tirgger_job]
                            LOGGER.info(StringClor().printColorString(
                                        "No build change, Try to tirgger last build change with job cmd : %s" %trigger_job_cmd,
                                        StringClor.F_GRE))

                            cmd_triggerjob_map[key_name_tirgger_job]=""
                            CommonOpt().dumpData(self.rdy_tirgger_job_file, cmd_triggerjob_map)
                        else:
                            LOGGER.info(StringClor().printColorString(
                                        "No build change or last build change needs to be triggered",
                                        StringClor.F_GRE))
                            
                    else:
                        LOGGER.info(StringClor().printColorString('No enable job to be triggered',
                                    StringClor.F_GRE))
                    '''
                self.triggerJob(arch, mode, trigger_job_cmd, cmd_triggerjob_map)
                LOGGER.info("-"*50)   
    '''
    def getEnableJenkinsJob(self, arch, build_ver, kernel_name):

        for (i, job) in enumerate(self.jenkins_job):
            if JenkinsAPI().checkBuildable(job %dict(arch=arch)) is True:
                break
        else:
            LOGGER.warn("There is not enable job can be triggered")
            return ""
        
        if i == 0:
            return self.jenkins_job_with_param[i] %dict(arch=arch,
                                                        #repo=self.repo,
                                                        build_ver=build_ver,
                                                        kernel_name=kernel_name)
        else:
            return self.jenkins_job_with_param[i] %dict(arch=arch,
                                                        repo=self.repo,
                                                        build_ver=build_ver,
                                                        kernel_name=kernel_name)
    '''
    def triggerJob(self, arch, mode, cmd, reloaded_data):
        key_name_tirgger_job = '%s_%s_%s' %(self.prj_name, arch, mode)
        
        if cmd:
            report_file = re.search('REPORT_FILE=(\S+)&', cmd, re.I).groups()[0]
            
            fh = self.flowctrller.chooseHost(self.hosts[arch][mode], self.host_status_file, report_file, chkssh=True)
                    

            if fh:
                LOGGER.info("Get available host : %s" %fh)
    
                self.return_code = 0
                cmd = cmd + fh + "\""
    
                LOGGER.info("Trigger job %s" %cmd)
                os.system(cmd)
            else:
                LOGGER.info("NO available host %s for triggering, dump data to file" %str(self.hosts[arch][mode]))
                reloaded_data[key_name_tirgger_job]=cmd
                CommonOpt().dumpData(self.rdy_tirgger_job_file, reloaded_data)
        else:
            LOGGER.info("No trigger build")
        #self.triggered_arch = self.triggered_arch and  self.triggered_arch + ',%s' %arch or arch

    def getBuildChange(self, arch):
        url = os.path.join(self.repo, "standard", arch)
        abs_last_file = os.path.join(self.repo_store_path, "last_repo_file_on_%s" %arch)
        return self.checkBuildChange(abs_last_file, url)

    def getBuildVersion(self, build_output, mode='default'):
        rei =  re.search('>%s-(\S+?).rpm<' %'kernel-%s' %mode, build_output, re.I)
        if rei:
            return  rei.groups()[0].strip()
        return "Not-match-build-version-%s" %(time.time())
    
    def checkBuildChange(self, last_file, url):

        last_content = CommonOpt().loadData(last_file)
        curr_content = self.urlpaser.getFileContent(url)
        
        if curr_content.strip() == "":
            return (False, last_content, "")
        else:
            if ''.join(last_content).strip() == curr_content.strip():
                return (False, last_content, curr_content)
            else:
                CommonOpt().dumpData(last_file, curr_content)
                return (True, last_content, curr_content)


def main():
    
    # Get parameters from cmd
    ins_parseparam = ParseParam().parseKOTDMonitorParam()
    options, _args = ins_parseparam.parse_args()
    
    # Get config file of kotd project
    LOGGER.info("start")
    if os.path.exists(KOTD_REF_TEST_CFG_FILE):
        rtbc = RTBuildChange(options)
        rtbc.loopCheckBuildChange()
        sys.exit(rtbc.return_code)
    else:
        LOGGER.error("Config file does not exist.")
        sys.exit(-1)


if __name__ == '__main__':
    main()

