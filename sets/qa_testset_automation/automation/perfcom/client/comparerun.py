#!/usr/bin/python3

import logging
logger = logging.getLogger()
import json
from .error import *
from . import (main, tenv, plan, perftest, logdb)
from . import casesDB

compare_run_parser = main.sub_parsers.add_parser("compare-run")
compare_run_parser.add_argument('-a', '--arch', dest='arch', type=str, help="arch", required=True)
compare_run_parser.add_argument('-r', '--release', dest='release', type=str, help="release", required=True)
compare_run_parser.add_argument('-b', '--build', dest='build', type=str, help="build", required=True)
compare_run_parser.add_argument('-k', '--kernel', dest='kernel', type=str, help="kernel", required=True)
compare_run_parser.add_argument('-m', '--host', dest='host', type=str, help="host", required=True)
compare_run_parser.add_argument('-u', '--suite', dest='suite', type=str, help="suite", required=False)

def subcmd(args):
    global distro, machine, inst, dynapi, g_suite
    distro = tenv.OSDistro(args.arch, args.release, args.build, args.kernel)
    machine = tenv.Machine(args.host)
    #current ignore the real OSInst Settings
    inst = tenv.OSInst(tenv.TenvPlain.DEFAULT_SWAP_SIZE,
                       tenv.TenvPlain.DEFAULT_ROOFS_TYPE,
                       tenv.TenvPlain.DEFAULT_ROOFS_SIZE)
    dynapi = args.dynapi
    g_suite = args.suite
    print("g_suite", g_suite)
    compare_run()

compare_run_parser.set_defaults(func=subcmd)

class AllCases:
    def __iter__(self):
        if g_suite and g_suite in casesDB.cases:
            cases = ((g_suite, casesDB.cases[g_suite]),)
        else:
            cases = casesDB.cases.items()
        return iter(cases)

def compare_run():
    suite_no_log = []
    suite_with_error = []
    #directly access the qadb
    try:
        run_id = plan.Run(distro).get_run_id(dynapi)
    except HTTPError as e:
        logger.error(str(e))
        return
    for suite, v in AllCases():
        logs = logdb.query_log(dynapi, distro, machine, run_id, suite)
        print("{0} {1} {2}".format(str(distro), machine.host, suite))
        if not logs:
            logger.warning("No Logs")
            suite_no_log.append(suite)
        else:
            component = tenv.OSComponent(v["category"], v["category_value"])
            t_env = tenv.Tenv(distro, component, inst, machine)
            cases = v["cases"]
            perf_test = perftest.PerfTest(suite, cases, t_env)
            try:
                perf_test.compare(dynapi)
            except HTTPError as e:
                suite_with_error.append(suite)
                logger.error(str(e))
    print("suites without logs")
    for suite in suite_no_log: print("\t{}".format(suite))
    print("suites with error")
    for suite in suite_with_error: print("\t{}".format(suite))
