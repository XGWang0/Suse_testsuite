#!/usr/bin/python3

from .error import *
from . import (main, tenv, plan, direct)

run_parser = main.sub_parsers.add_parser("run")
run_sub_parsers = run_parser.add_subparsers(dest="sub_run")
run_new = run_sub_parsers.add_parser("new")
run_new.add_argument('-a', dest='arch', type=str, default="x86_64",
                     help="arch")
run_new.add_argument('-r', dest='release_pair', type=str, required=True, nargs=2,
                     metavar = ("question_release", "reference_release"), help="release pair")
run_new.add_argument('-b', dest='build_pair', type=str, required=True, nargs=2,
                     metavar = ("question_build", "reference_build"), help="build pair")
run_new.add_argument('-k', dest='kernel_pair', type=str, nargs=2, required=True,
                     metavar = ("question_kernel", "reference_kernel"),help="kernel pair")
run_new.add_argument('-n', dest='run_id_pair', type=str, nargs=2, required=True,
                     metavar = ("question_run_id", "reference_run_id"), help="run ID pair")
run_list = run_sub_parsers.add_parser("list")

def subcmd(args):
    global dynapi
    dynapi = args.dynapi
    if args.sub_run == "new":
        new_run_pair()
    elif args.sub_run == "list":
        list_run_pair()
    else:
        AssertionError("Not Reached")

run_parser.set_defaults(func=subcmd)

def new_run_pair(args):
    question_distro = tenv.OSDistro(args.arch, args.release_pair[0],
                                    args.build_pair[0], args.kernel_pair[0])
    question_run_id = args.run_id_pair[0]

    reference_distro = tenv.OSDistro(args.arch, args.release_pair[1],
                                     args.build_pair[1], args.kernel_pair[1])
    reference_run_id = args.run_id_pair[1]
    run = plan.Run(question_distro, question_run_id)
    run.save_pair(dynapi, reference_distro, reference_run_id)

def list_run_pair():
    SQLs = "select * from distro_plan_pair_view"
    ret = direct.reportdb(dynapi, SQLs)
    print(ret)
    return ret
