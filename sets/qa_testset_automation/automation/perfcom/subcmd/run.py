#!/usr/bin/python3

import app
APP = app.APP
from common import (tenv, plan, direct)

class SubCmd(app.SubCmd):
    @classmethod
    def parser_common(cls, parser, required=True):
        parser.add_argument('-r', dest="release", type=str, required=required,
                            help="release")
        parser.add_argument('-b', dest="build", type=str, required=required,
                            help="build")
    @classmethod
    def parser_common2(cls, parser):
        parser.add_argument('-a', dest="arch", type=str, required=True,
                            help="arch")
        parser.add_argument('-k', dest="kernel", type=str, required=True,
                            help="kernel")
        parser.add_argument('-n', dest="run_id", type=str, required=True,
                            help="run id")

    class RunNew(app.CmdOne):
        def setup(self, parser):
            SubCmd.parser_common(parser)
            SubCmd.parser_common2(parser)

        def run(self, args):
            distro = tenv.OSDistro(args.arch, args.release, args.build, args.kernel)
            run_id = args.run_id
            run = plan.Run(distro, run_id)
            run.new_run(APP.dynapi)

    class RunList(app.CmdOne):
        def setup(self, parser):
            SubCmd.parser_common(parser, required=False)

        def run(self, args):
            self.list_by_build(args.release, args.build)

        def list_by_build(self, release, build):
            if not release: release = ""
            if not build: build = ""
            SQLs = "SELECT * FROM distro_run_view" \
                   " WHERE `release` LIKE '%{0}%' AND `build` LIKE '%{1}%'"
            SQLs = SQLs.format(release, build)
            try:
                r_list = direct.reportdb(APP.dynapi, SQLs)
                if not r_list: r_list = []
            except Exception as e:
                print(e)
                return False
            for r in r_list:
                print("{id}: {arch}/{release}/{build}/{kernel} {run_id}".format(**r))

    class PairNew(app.CmdOne):
        def setup(self, parser):
            parser.add_argument(dest='question', type=int,
                                help="the question distro run id")

            parser.add_argument(dest='reference', type=int,
                                help="the reference distro run id")
        def run(self, args):
            q_distro_run_id = args.question
            r_distro_run_id = args.reference
            plan.new_pair(APP.dynapi, q_distro_run_id, r_distro_run_id)

    class PairList(app.CmdOne):
        def setup(self, parser):
            SubCmd.parser_common(parser, required=False)

        def run(self, args):
            self.list_by_question(args.release, args.build)

        def list_by_question(self, release, build):
            if not release: release = ""
            if not build: build = ""
            SQLs = "SELECT * FROM distro_run_pair_view" \
                   " WHERE `q_release` LIKE '%{0}%' AND `q_build` LIKE '%{1}%'"
            SQLs = SQLs.format(release, build)
            try:
                r_list = direct.reportdb(APP.dynapi, SQLs)
                if not r_list: r_list = []
            except Exception as e:
                print(e)
                return False
            for r in r_list:
                id_str = "{}: ".format(r['id'])
                l = len(id_str)
                print(id_str, end="")
                print("{arch}/{q_release}/{q_build}/{q_kernel} {q_run_id}".format(**r))
                bk = ""
                for i in id_str:
                    bk = bk + " "
                print(bk, end="")
                print("{arch}/{r_release}/{r_build}/{r_kernel} {r_run_id}".format(**r))

    class DefaultQuestionNew(app.CmdOne):
        def setup(self, parser):
            parser.add_argument(dest="run_id", type=int,
                                help="the default distro run id")
        def run(self, args):
            default_distro_run_id = args.run_id
            plan.pair_default_set(APP.dynapi, default_distro_run_id)


    cmds = {"new":RunNew(), "list":RunList(),
            "pair-new":PairNew(), "pair-list":PairList(),
            "set-default":DefaultQuestionNew()}
    @classmethod
    def init_parser(cls, parser):
        subparser_set = parser.add_subparsers(dest="runcmd")
        for cmd_name, cmd_obj in cls.cmds.items():
            subparser = subparser_set.add_parser(cmd_name)
            cmd_obj.setup(subparser)

    @classmethod
    def run(cls, args):
        try:
            cmd_obj = cls.cmds[args.runcmd]
        except KeyError:
            AssertionError("Not Reached")
        else:
            cmd_obj.run(args)

app.cmd_init("run", SubCmd)
