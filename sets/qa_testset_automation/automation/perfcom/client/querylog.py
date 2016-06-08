#!/usr/bin/python3

import logging
logger = logging.getLogger()
import json
from .error import *
from . import (main, tenv, plan, perftest, logdb)
from . import casesDB

query_log_parser = main.sub_parsers.add_parser("query-log")
query_log_parser.add_argument('-a', '--arch', dest='arch', type=str, help="arch", required=True)
query_log_parser.add_argument('-r', '--release', dest='release', type=str, help="release", required=True)
query_log_parser.add_argument('-b', '--build', dest='build', type=str, help="build", required=True)
query_log_parser.add_argument('-k', '--kernel', dest='kernel', type=str, help="kernel", required=True)
query_log_parser.add_argument('-m', '--host', dest='host', type=str, help="host", required=True)
query_log_parser.add_argument('-u', '--suite', dest='suite', type=str, help="suite", required=False, default="")
query_log_parser.add_argument('-n', dest='run_id', type=str, help="run ID", required=True)

def subcmd(args):
    global distro, machine, dynapi, suite, run_id
    distro = tenv.OSDistro(args.arch, args.release, args.build, args.kernel)
    machine = tenv.Machine(args.host)
    run_id = args.run_id
    dynapi = args.dynapi
    suite = args.suite
    if not suite:
        query_cases()
    else:
        query_log()

query_log_parser.set_defaults(func=subcmd)

def query_log():
    logs = logdb.query_log(dynapi, distro, machine, run_id, suite)
    print(machine)
    print(distro)
    print(suite)
    for log in logs:
        print_log(log)

def print_log(log):
    print("{0} {1}".format(log["test_date"], log["log_url"]))

def query_cases():
    cases = logdb.query_cases(dynapi, distro, machine, run_id)
    print(machine)
    print(distro)
    render_cases(cases)

def render_cases(cases):
    length = {"testsuite":0, "count":0}
    for case in cases:
        length["testsuite"] = max(length["testsuite"], len(str(case["testsuite"])))
        length["count"] = max(length["count"], len(str(case["count"])))
    fmt = "{{0:{0}}}\t{{1:{1}}}".format(length["testsuite"], length["count"])
    for case in cases:
        print(fmt.format(case["testsuite"], case["count"]))
