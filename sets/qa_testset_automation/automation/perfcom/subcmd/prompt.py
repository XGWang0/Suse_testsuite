#!/usr/bin/python3

import app

class SubCmd(app.SubCmd):
    @classmethod
    def run(cls, args):
        app.REPL.set_prompt(args.prompt)

    @classmethod
    def init_parser(cls, parser):
        parser.add_argument("-a", dest="prompt", type=str)

app.cmd_init("prompt", SubCmd)
