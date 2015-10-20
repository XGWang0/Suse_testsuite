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

from  pylib import HostContorller
#REINSTALL_CMD = '/usr/share/qa/tools/install.pl  -p http://147.2.207.1/dist/install/SLP/SLES-11-SP3-GM/x86_64/DVD1/ -t base -B'

def getReportFile(report_file):
    if report_file:
        dirname, base_file = os.path.split(report_file)
        if base_file.split("_")[-1]:
            return (dirname, base_file)
        else:
            return (dirname, base_file + CommonOpt.generateRandomStr())
    else:
        return (PrjPath().getWorkSpace(), CommonOpt.generateRandomStr())

def main():

    host = sys.argv[1]
    report_file = getReportFile(sys.argv[2])[1]
    LOGGER.debug(HOST_STATUS_FILE)
    #HostContorller().getAvailableHost(host, HOST_STATUS_FILE, HostContorller.HOST_FREE, HostContorller.HOST_FREE + ' ALL')
    HostContorller().getAvailableHost(host, HOST_STATUS_FILE, '', HostContorller.HOST_FREE + ' ALL')

if __name__ == '__main__':

    main()
