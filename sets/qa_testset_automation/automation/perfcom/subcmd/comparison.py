#!/usr/bin/python3

import app
APP = app.APP
from common import comparison

class SubCmd(app.SubCmd):
    @classmethod
    def run(cls, args):
        suite = args.suite
        case = args.case
        question = args.question
        references = args.references
        comp = comparison.Comparison(suite, case)
        comp.set_q_tenv_id(question)
        comp.set_r_tenv_ids(references)
        comp.page(APP.dynapi)

    @classmethod
    def init_parser(cls, parser):
        parser.add_argument("-s", dest="suite", required=True)
        parser.add_argument("-c", dest="case", required=True)
        parser.add_argument("-q", dest="question", required=True)
        parser.add_argument("-l", dest="references", required=True)

app.cmd_init("comparison", SubCmd)
