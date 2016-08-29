#!/usr/bin/python3

import logging
logger = logging.getLogger()
import app
APP = app.APP
from common.error import *
from common import (tenv, plan, perftest, logdb)
from common import casesDB

class AllCases:
    def __init__(self, *suite_list):
        self.cases = []
        for suite in suite_list:
            if suite in casesDB.cases:
                self.cases.append((suite, casesDB.cases[suite]))
        if not self.cases:
            self.cases = casesDB.cases.items()
    def __iter__(self):
        return iter(self.cases)

class SubCmd(app.SubCmd):
    @classmethod
    def init_parser(cls, parser):
        parser.add_argument('-a', dest='arch', type=str,
                            default='x86_64',
                            help="arch")
        parser.add_argument('-r', dest='release', type=str,
                            required=True,
                            help="release")
        parser.add_argument('-b', dest='build', type=str,
                            required=True,
                            help="build")
        parser.add_argument('-k', dest='kernel', type=str,
                            required=True,
                            help="kernel")
        parser.add_argument('-m', dest='host', type=str,
                            required=True,
                            help="host")
        parser.add_argument('-u', dest='suite', type=str,
                            required=False)
        parser.add_argument('-n', dest='run_id', type=str,
                            required=True)
    @classmethod
    def run(cls, args):
        dynapi = APP.dynapi
        distro = tenv.OSDistro(args.arch, args.release, args.build, args.kernel)
        machine = tenv.Machine(args.host)
        #current ignore the real OSInst Settings
        inst = tenv.OSInst(tenv.TenvPlain.DEFAULT_SWAP_SIZE,
                           tenv.TenvPlain.DEFAULT_ROOFS_TYPE,
                           tenv.TenvPlain.DEFAULT_ROOFS_SIZE)
        target_suite = args.suite
        run_id = args.run_id
        run = plan.Run(distro, run_id)
        suite_no_log = []
        suite_with_error = []
        for suite, v in AllCases(target_suite):
            try:
                logs = logdb.query_log(dynapi, distro, machine, run_id, suite)
            except:
                continue
            print("{0} {1} {2}".format(str(distro), machine.host, suite))
            if not logs:
                suite_no_log.append(suite)
            else:
                component = tenv.OSComponent(v["category"], v["category_value"])
                t_env = tenv.Tenv(distro, component, inst, machine)
                cases = v["cases"]
                perf_test = perftest.PerfTest(suite, cases, t_env, run)
                try:
                    perf_test.compare(dynapi)
                except HTTPError as e:
                    suite_with_error.append(suite)
                    logger.error(str(e))
        print("suites without logs")
        for suite in suite_no_log: print("\t{}".format(suite))
        print("suites with error")
        for suite in suite_with_error: print("\t{}".format(suite))

app.cmd_init("compare-run", SubCmd)
