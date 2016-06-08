#!/usr/bin/python3

import logging
logger = logging.getLogger()
from .error import *
from . import (main, logdir, tenv, perftest)
from . import casesDB

comparelog_parser = main.sub_parsers.add_parser("compare-log")
comparelog_parser.add_argument('-l', '--logroot', dest='logroot', type=str, help="the logdir", default='/var/log/qa/ctcs2')
comparelog_parser.add_argument('-u', '--suite', dest='suite', type=str, help="the test suite", default="")

def subcmd(args):
    global logroot, g_suite, dynapi
    logroot = args.logroot
    g_suite = args.suite
    dynapi = args.dynapi
    comparelog()

comparelog_parser.set_defaults(func=subcmd)

def comparelog():
    db = logdir.logDirDB(logroot, g_suite)
    for suite in db:
        try:
            perf_test = perftest.PerfTest(suite.suite, suite.cases, suite.tenv)
            perf_test.compare(dynapi)
        except casesDB.InvalidSuiteError as e:
            logger.error(str(e))
        except NoPlanError as e:
            logger.error(str(e))
        except HTTPError as e:
            logger.error(str(e))
