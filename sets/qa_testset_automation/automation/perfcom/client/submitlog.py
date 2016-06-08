#!/usr/bin/python3

import logging
logger = logging.getLogger()
from .error import *
from . import (main, logdir)

submitlog_parser = main.sub_parsers.add_parser("submit-log")
submitlog_parser.add_argument('-l', '--logroot', dest='logroot', type=str, help="the logdir", default='/var/log/qa/ctcs2')
submitlog_parser.add_argument('-u', '--suite', dest='suite', type=str, help="the test suite", default="")

def subcmd(args):
    global logroot, g_suite, dynapi
    logroot = args.logroot
    g_suite = args.suite
    dynapi = args.dynapi
    submitlog()

submitlog_parser.set_defaults(func=subcmd)

def submitlog():
    db = logdir.logDirDB(logroot, g_suite)
    for suite in db:
        try:
            suite.submit_report(dynapi)
        except HTTPError as e:
            logger.error(e)
