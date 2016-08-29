#!/usr/bin/python3

import logging
logger = logging.getLogger()
import app
APP = app.APP
from common import (logdir, tenv, perftest)
from common import casesDB
from common.error import *

class SubCmd(app.SubCmd):
    @classmethod
    def init_parser(cls, parser):
        parser.add_argument('-l', dest='logroot', type=str,
                            default='/var/log/qa/ctcs2',
                            help="the logdir")
        parser.add_argument('-u', dest='suite', type=str, default="",
                            help="the test suite")

    @classmethod
    def run(cls, args):
        dynapi = APP.dynapi
        logroot = args.logroot
        target_suite = args.suite
        db = logdir.logDirDB(logroot, target_suite)
        for suite in db:
            try:
                perf_test = perftest.PerfTest(suite.suite, suite.cases, suite.tenv, suite.plan)
                perf_test.compare(dynapi)
            except casesDB.InvalidSuiteError as e:
                logger.error(str(e))
            except NoPlanError as e:
                logger.error(str(e))

app.cmd_init("compare-log", SubCmd)
