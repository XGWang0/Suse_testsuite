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

import ConfigParser
import optparse
from ast import literal_eval

from constantvars import *


class CMDParamParser(optparse.OptionParser):
    """Class which parses command parameters
    """

    def __init__(self):
        
        pass

    def parseMonitorParam(self):
        optparse.OptionParser.__init__(
            self, 
            usage='Usage: %prog [options]',
            epilog="Monitor build ...")

        self.add_option("-l", "--localrepo", action="store", type="string",
                        dest="mbuild_lrepo",
                        help=("Input a local repo address"))
        self.add_option("-r", "--remoterepo", action="store", type="string",
                        dest="mbuild_mrepo",
                        help=("Input a remote repo address."))
        '''
        self.add_option("-j", "--jobname", action="store", type="string",
                        dest="mbuild_jjob",
                        help=("Input jenkins job name that will be triggered"))
        '''
        self.add_option("-p", "--prjname", action="store", type="choice",
                        dest="mbuild_prj", choices=["SLES-11-SP4","SLES-12-SP0","SLES-12-SP1"],
                        help=("Input project name within name \"SLES-11-SP4|SLES-12-SP0|SLES-12-SP1\"."))

        return self

    def parseKOTDMonitorParam(self):
        optparse.OptionParser.__init__(
            self, 
            usage='Usage: %prog [options]',
            epilog="Monitor build ...")

        self.add_option("-r", "--repo", action="store", type="string",
                        dest="kotdmb_repo",
                        help=("Input a repo address"))
        
        self.add_option("-p", "--prjname", action="store", type="choice",
                        dest="kotdmb_prj", choices=["SLES-11-SP4","SLES-12-SP0","SLES-12-SP1"],
                        help=("Input project name within name \"SLES-11-SP4|SLES-12-SP0|SLES-12-SP1\"."))

        return self
    
    def parseReInstParam(self):
        optparse.OptionParser.__init__(
            self, 
            usage='Usage: %prog [options]',
            epilog="Reinstall host ...")

        self.add_option("-P", "--projectname", action="store", type="choice",
                        dest="rinst_project",  choices=["KOTD","RT"],
                        help=("Select one project for re-installation host.(KOTD|RT)"))

        self.add_option("-p", "--productversion", action="store", type="string",
                        dest="rinst_productv",
                        help=("Input a product version for reinstallation"))
        self.add_option("-r", "--repository", action="store", type="string",
                        dest="rinst_repo",
                        help=("Set path of repositroy for reinstallation."))
        
        self.add_option("-m", "--machine", action="store", type="string",
                        dest="rinst_mach",
                        help=("Input one machine ip address which reinstalls product on it."))

        self.add_option("-A", "--architecture", action="store", type="string",
                        dest="rinst_arch",
                        help=("Select one arch to reinstallation.(i586|ia64|ppc|s390|s390x|x86_64)"))
        self.add_option("-f", "--reportfile", action="store", type="string",
                        dest="rinst_report",
                        help=("Input a report file, it will be reloaded and combine with current build result"))
        self.add_option("-b", "--buildversion", action="store", type="string",
                        dest="rinst_buildv",
                        help=("Input build version."))

        return self

    def parseRegTestParam(self):
        optparse.OptionParser.__init__(
            self, 
            usage='Usage: %prog [options]',
            epilog="Regression test ...")

        self.add_option("-T", "--type", action="store", type="choice", default='stress_validation',
                        dest="regre_type", choices=["stress_validation","kernel_regression",'userspace_app'],
                        help=("Test type: (stress_validation|kernel_regression|userspace_app)"))

        self.add_option("-p", "--productversion", action="store", type="string",
                        dest="regre_productv",
                        help=("Input production version."))  

        self.add_option("-m", "--machine", action="store", type="string",
                        dest="regre_mach",
                        help=("Input ip address of machine which does regression test on it."))

        self.add_option("-A", "--architecture", action="store", type="string",
                        dest="regre_arch",
                        help=("Select one arch to do regression.(i586|ia64|ppc|s390|s390x|x86_64)"))        

        self.add_option("-b", "--buildversion", action="store", type="string",
                        dest="regre_buildv",
                        help=("Input build version."))

        self.add_option("-r", "--qa-repository", action="store", type="string",
                        dest="regre_qarepo",
                        help=("Input qa repository."))

        self.add_option("-f", "--reportfile", action="store", type="string",
                        dest="regre_report",
                        help=("Input a report file, it will be reloaded and combine with current build result"))

        self.add_option("-t", "--testsuites", action="store", type="string",
                        dest="regre_ts",
                        help=("Input special testsuites."))        
        
        
        return self

    def parseKOTDParam(self):
        optparse.OptionParser.__init__(
            self, 
            usage='Usage: %prog [options]',
            epilog="KOTD test ...")

        self.add_option("-p", "--productversion", action="store", type="string",
                        dest="kotd_productv",
                        help=("Input production version."))  

        self.add_option("-m", "--machine", action="store", type="string",
                        dest="kotd_mach",
                        help=("Input ip address of machine which does kotd test on it."))

        self.add_option("-A", "--architecture", action="store", type="string",
                        dest="kotd_arch",
                        help=("Select one arch to do regression.(i586|ia64|ppc|s390|s390x|x86_64)"))        

        self.add_option("-b", "--buildversion", action="store", type="string",
                        dest="kotd_buildv",
                        help=("Input kernel build version."))

        self.add_option("-r", "--qa-repository", action="store", type="string",
                        dest="kotd_kernelrepo",default="http://download.suse.de/ibs/Devel:/Kernel:/SLE12-SP1/standard/",
                        help=("Input kernel repository."))

        self.add_option("-f", "--reportfile", action="store", type="string",
                        dest="kotd_report",
                        help=("Input a report file, it will be reloaded and combine with current build result"))
        
        self.add_option("-k", "--kernelname", action="store", type="string",
                        dest="kotd_kernel",
                        help=("Input kernel name which will be installed on machine."))
        return self

class RegConfigParser(object):
    
    def __init__(self):
        
        self.cf = ConfigParser.ConfigParser()

    def getItem(self, file_name, section_name, item_name):

        if os.path.exists(file_name):
            self.cf.read(file_name)
            #print self.cf.sections() 
            #print self.cf.options(section_name)
            if  section_name in self.cf.sections() and item_name in self.cf.options(section_name):
                return self.cf.get(section_name, item_name)
            else:
                LOGGER.warn("Section %s or itme %s does not exist!" %(section_name,item_name))
                return ""
            
            
        else:
            LOGGER.warn("Config file %s does not exist!" %file_name)
            return ""

    def convertItem(self, item):
        try:
            return literal_eval(item)
        except Exception,e:
            LOGGER.error(e)
            sys.exit(-1)

if __name__ == '__main__':
    pc = RegConfigParser()
    w =  literal_eval(pc.getItem('/root/eclipse_ws/RegressionTest/kotd.cfg', 'SLES-12-SP0', 'host'))
    print w
    print w['x86_64']