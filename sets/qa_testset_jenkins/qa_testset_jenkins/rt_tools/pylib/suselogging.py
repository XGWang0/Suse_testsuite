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

import logging
import os

class LoggerHander(object):
    """Class which support to add five kind of level info to file
    and standard output 
    """
    def __init__(self, logfile, level=logging.DEBUG):
        
        self.logfile = logfile
        abs_logfile = self.chkLogfile()
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] [%(process)d] %(levelname)-6s | %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=abs_logfile,
                            filemode='w')

        console = logging.StreamHandler()
        console.setLevel(level)
        formatter = logging.Formatter('%(asctime)s [%(process)d]: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)

        self.logger = logging.getLogger('')
        self.logger.addHandler(console)

    def debug(self, message):
        """Display debug message
        """
        self.logger.debug(message)

    def info(self, message):
        """Display info message
        """
        self.logger.info(message)

    def warn(self, message):
        """Display warning message
        """
        self.logger.warn(message)

    def error(self, message):
        """Display error message
        """
        self.logger.error(message)

    def crit(self, message):
        """Display Criticall message
        """
        self.logger.critical(message)

    def chkLogfile(self):
        if os.path.exists(self.logfile):
            abs_logname = os.path.abspath(self.logfile)
        else:
            abs_curdir = os.path.abspath(os.curdir)
            abs_logname = os.path.join(abs_curdir, self.logfile)
        return abs_logname