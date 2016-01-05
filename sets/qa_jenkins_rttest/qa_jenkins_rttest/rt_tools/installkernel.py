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
from  pylib import CMDParamParser as ParseParam
from  pylib import StringColor as StringClor
from  pylib import ConnSlave as ConnSlave
from  pylib import Install_Kernel
from  pylib import HostContorller
#REINSTALL_CMD = '/usr/share/qa/tools/install.pl  -p http://147.2.207.1/dist/install/SLP/SLES-11-SP3-GM/x86_64/DVD1/ -t base -B'

def main():

    start_time = datetime.datetime.now()
    # Instance parameters parse function
    ins_parseparam = ParseParam().parseKOTDParam()
    options, _args = ins_parseparam.parse_args()
    
    kotd_data_list = []
    feat_name = 'KTOD'
    feat_desc = ('KTOD Test:\n'
                 'This test is only for KTOD test, '
                 'the test will automatically detect the given kernel version, install kernel and switch to the new kernel env\n'
                 ' then upload output data, verify and analyze result automatically \n'
                 'Test may be last several minutes to finish, Once test pass, '
                 'a mail notification will be send to test owner\n\n'
                 'Kernel Package : %s' %(options.kotd_kernel))


    LOGGER.info(StringClor().printColorString("---------KOTD Test Start -----------",
                                             StringClor.HIGLIG))

    # Initial environment
    CommonOpt().cleanFile(subfix="pkl")
    CommonOpt().cleanFile(subfix="json")

    ins_qaset = Install_Kernel(options, (feat_name, feat_desc), options.kotd_kernel)

    if HostContorller().reserveHost(options.kotd_mach, HOST_STATUS_FILE, ins_qaset.report_file):
        pass
    else:
        rel_msg = "Host %s is busy now, test exit." %options.kotd_mach
        LOGGER.error(rel_msg)
        exec_duration = CommonOpt().getDiffTime(start_time, datetime.datetime.now())
        tc_data = ins_qaset.combineTCData(tc_name='Lock host', tc_status='failed', 
                                 tc_duration=exec_duration, tc_output=rel_msg)
        ts_data = ins_qaset.combineTSData(ts_name="Reserve Host", ts_tc_list=tc_data)
        kotd_data_list.extend(ts_data)
        ins_qaset._exit(kotd_data_list, flg='1vn')

    kotd_data_list.extend(ins_qaset.sshSlave(try_times=60, interval_time=5,show_kernel_ver=True))

    kernel_repo = os.path.join(options.kotd_kernelrepo,
                               CommonOpt().convertPrjNameI(options.kotd_productv),
                               'standard')

    full_pkg_name = ins_qaset.getKernelPkgName(os.path.join(kernel_repo, options.kotd_arch), options.kotd_kernel)

    rel = ins_qaset.installPackage(qa_repo=kernel_repo, package=full_pkg_name)
    
    kotd_data_list.extend(rel[1])
    
    if rel[0] is True:
        rel = ins_qaset.rebootSlave()
    
        rel = ins_qaset.sshSlave(try_times=100, interval_time=60)
    
        rel = ins_qaset.checkKernelVer(full_pkg_name)
        if rel[0] is True:
            tc_status = 'passed'
        else:
            tc_status = 'failed'

        ret_msg = rel[1]

        exec_duration = CommonOpt().getDiffTime(start_time, datetime.datetime.now())
        tc_data = ins_qaset.combineTCData(tc_name='Reboot to latest kervel version', tc_status=tc_status, 
                                     tc_duration=exec_duration, tc_output=ret_msg)
        ts_data = ins_qaset.combineTSData(ts_name="Switch kernel", ts_tc_list=tc_data)
        
        kotd_data_list.extend(ts_data)
    else:
        pass

    ins_qaset.executeCMD("chkconfig sshd on")

    ins_qaset._exit(kotd_data_list, flg='1vn')

if __name__ == '__main__':

    main()
