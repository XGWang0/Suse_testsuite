#!/usr/bin/python3

import logging
logger = logging.getLogger()
import os
import re
from datetime import datetime
import subprocess
import json
import tarfile
import tempfile
import shutil
from .error import *
from . import tenv
from . import plan
from . import casesDB

DEFAULT_LOGROOT = "/var/log/qa/ctcs2"
class logDirDB:
    #2016-03-31-13-44-31
    LOG_DIR_PT = re.compile("(.*)-(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})$")
    LOG_ARCHIVE_PT = re.compile("(.*)-([^-]+)-(\d{8})-(\d{8}T\d{6})(\.tar\.bz2)")
    def __init__(self, logroot = DEFAULT_LOGROOT, target_suite = ""):
        self.logroot = logroot
        self.target_suite = target_suite

    def __iter__(self):
        if not "suites" in self.__dict__:
            self.scan_dir()
        return iter(self.suites)

    def scan_dir(self):
        suites = []
        for f in os.listdir(self.logroot):
            path = "{0}/{1}".format(self.logroot, f)
            if os.path.isdir(path):
                m = self.LOG_DIR_PT.match(f)
                if not m:
                    logger.warning("unknown dir {0}".format(f))
                    continue
                else:
                    suite = m.group(1)
                    bziped = False
            elif os.path.isfile(path):
                m = self.LOG_ARCHIVE_PT.match(f)
                if not m:
                    logger.warning("unknown file {0}".format(f))
                    continue
                else:
                    suite = m.group(1)
                    bziped = True
            else:
                raise RuntimeError("what?")

            if self.target_suite and self.target_suite != suite:
                logger.debug("{}: not target_suite {}".format(suite, self.target_suite))
                continue
            try:
                suites.append(ctcs2suite(suite, path, bziped))
            except (FileNotFoundError, InvalidLogError) as e:
                logger.error(str(e))
            #datetime.stratum("%Y-%m-%d-%H-%M-%S", m.group(2))
        if len(suites) == 0:
            logger.warning("not log in logroot {}".format(self.logroot))
        self.suites = suites

class ctcs2suite:
    def __init__(self, suite, logpath, bziped = False):
        self.suite = suite
        self.logpath = logpath
        self._distro = None
        self._component = None
        self._inst = None
        self._machine = None
        self.bziped = bziped
        if self.bziped:
            self.logdir = tempfile.TemporaryDirectory(prefix="qaset-").name
            self.deflate()
        else:
            self.logdir = self.logpath
        self.parse_tenv()

    def __del__(self):
        if self.bziped and self.logdir:
            shutil.rmtree(self.logdir, ignore_errors=True)

    def deflate(self):
        ziplog = tarfile.open(self.logpath)
        logger.debug("extract {0} to {1}".format(self.logpath, self.logdir))
        ziplog.extractall(self.logdir)
        ziplog.close()
        subdirs = os.listdir(self.logdir)
        if len(subdirs) != 1:
            raise InvalidLogError(self.logpath)
        logdir = subdirs[0]
        self.logdir = "{0}/{1}".format(self.logdir, logdir)

    @property
    def cases(self):
        ''' return all the case in the suite'''
        return casesDB.get_cases_by_suite(self.suite)["cases"]

    def parse_tenv(self):
        tenv_txt = "{}/tenv.txt".format(self.logdir)
        logger.debug("parsing {}".format(tenv_txt))
        stream = open(tenv_txt)
        self.tenv_plain = tenv.TenvPlain(stream, name=tenv_txt)
        self.plan = plan.Run(self.distro, self.run_id)
        self.tenv = tenv.Tenv(self.distro, self.component, self.inst, self.machine)

    @property
    def run_id(self):
        ''' return arch, release, build, kernel'''
        ''' return an OSDistro'''
        return self.tenv_plain.run_id

    @property
    def distro(self):
        ''' return arch, release, build, kernel'''
        ''' return an OSDistro'''
        return self.tenv_plain.distro

    @property
    def component(self):
        ''' return category, category_value'''
        ''' return an OSComponent'''
        return self.tenv_plain.component

    @property
    def inst(self):
        ''' return swap_size, rootfs_type, rootfs_size'''
        ''' return an OSInst'''
        return self.tenv_plain.inst

    @property
    def machine(self):
        ''' return hostname'''
        ''' return an machine'''
        return self.tenv_plain.machine

    def submit_report(self, dynapi):
        tenv_id = self.tenv.new_id(dynapi)
        run_id = self.run_id
        #the outer "'" or '"' is removed by remote_qa_db_report.pl
        #So add a extra ' aroud the key to make there is " in qadb
        comment = json.dumps({'"tenv"':tenv_id,'"run"':run_id})
        args = ["/usr/share/qa/tools/remote_qa_db_report.pl", "-b", "-L", "-T", "qaset"]
        args.extend(["-m", self.machine.host])
        args.extend(["-a", self.distro.arch])
        args.extend(["-k", self.distro.kernel])
        #BUG remote_qa_db_report.pl dose not respect the -p and -N
        #leave release and build to it.
        #args.extend(["-p", self.distro.release])
        #args.extend(["-N", self.distro.build])
        args.extend(["-c", comment])
        args.extend(["-P", "ctcs2:{}".format(self.logdir)])
        logger.debug(" ".join(args))
        subprocess.call(args)
