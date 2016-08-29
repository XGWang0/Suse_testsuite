#!/usr/bin/python3

import app
APP = app.APP
from common import (tenv, plan, perftest, logdb)
from common import casesDB

class SubCmd(app.SubCmd):
    @classmethod
    def query_log(cls, distro, machine, run_id, suite):
        dynapi = APP.dynapi
        logs = logdb.query_log(dynapi, distro, machine, run_id, suite)
        print(machine)
        print(distro)
        print(suite)
        for log in logs:
            print("{0} {1}".format(log["test_date"], log["log_url"]))

    @classmethod
    def query_cases(cls, distro, machine, run_id):
        dynapi = APP.dynapi
        cases = logdb.query_cases(dynapi, distro, machine, run_id)
        print(machine)
        print(distro)
        length = {"testsuite":0, "count":0}
        for case in cases:
            length["testsuite"] = max(length["testsuite"], len(str(case["testsuite"])))
            length["count"] = max(length["count"], len(str(case["count"])))
        fmt = "{{0:{0}}}\t{{1:{1}}}".format(length["testsuite"], length["count"])
        for case in cases:
            print(fmt.format(case["testsuite"], case["count"]))

    @classmethod
    def run(cls, args):
        distro = tenv.OSDistro(args.arch, args.release, args.build, args.kernel)
        machine = tenv.Machine(args.host)
        run_id = args.run_id
        suite = args.suite
        if not suite:
            cls.query_cases(distro, machine, run_id)
        else:
            cls.query_log(distro, machine, run_id, suite)

    @classmethod
    def init_parser(cls, parser):
        parser.add_argument('-a', '--arch', dest='arch', type=str, default="x86_64",
                            help="arch")
        parser.add_argument('-r', '--release', dest='release', type=str,
                            required=True,
                            help="release")
        parser.add_argument('-b', '--build', dest='build', type=str,
                            required=True,
                            help="build")
        parser.add_argument('-k', '--kernel', dest='kernel', type=str,
                            required=True,
                            help="kernel")
        parser.add_argument('-m', '--host', dest='host', type=str,
                            required=True,
                            help="host")
        parser.add_argument('-u', '--suite', dest='suite', type=str, default="",
                            required=False,
                            help="suite")
        parser.add_argument('-n', '--run', dest='run_id', type=str,
                            required=True,
                            help="run ID")

app.cmd_init("log", SubCmd)
